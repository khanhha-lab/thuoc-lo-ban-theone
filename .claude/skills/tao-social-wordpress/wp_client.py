#!/usr/bin/env python3
"""
wp_client.py — Helper gọi WordPress REST API (không cần cài thư viện ngoài).

Đọc thông tin đăng nhập từ file .env cùng thư mục:
  WP_API_BASE, (WP_USER + WP_APP_PASSWORD) hoặc WP_BEARER_TOKEN

Cách dùng nhanh:
  python wp_client.py --test                 # kiểm tra kết nối
  python wp_client.py --create-page "Tiêu đề" body.html
  python wp_client.py --create-post "Tiêu đề" body.html --category "Tin tức"
  python wp_client.py --upload anh.jpg       # hoặc URL ảnh
"""
import os
import sys
import json
import base64
import argparse
import mimetypes
import urllib.request
import urllib.error
import urllib.parse


def load_env(path=None):
    """Đọc .env đơn giản (KEY=VALUE mỗi dòng)."""
    path = path or os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    env = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    # Ưu tiên biến môi trường hệ thống nếu có
    for k in ("WP_API_BASE", "WP_USER", "WP_APP_PASSWORD", "WP_BEARER_TOKEN"):
        if os.environ.get(k):
            env[k] = os.environ[k]
    return env


def auth_header(env):
    if env.get("WP_BEARER_TOKEN"):
        return {"Authorization": "Bearer " + env["WP_BEARER_TOKEN"]}
    user, pw = env.get("WP_USER"), env.get("WP_APP_PASSWORD")
    if user and pw:
        token = base64.b64encode(f"{user}:{pw}".encode()).decode()
        return {"Authorization": "Basic " + token}
    raise SystemExit("Thiếu thông tin đăng nhập trong .env (token hoặc user+app password).")


def request(env, method, path, data=None, extra_headers=None):
    base = env.get("WP_API_BASE", "").rstrip("/")
    if not base:
        raise SystemExit("Thiếu WP_API_BASE trong .env.")
    url = base + path
    headers = auth_header(env)
    headers["Accept"] = "application/json"
    if extra_headers:
        headers.update(extra_headers)
    body = None
    if data is not None and not isinstance(data, bytes):
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    elif isinstance(data, bytes):
        body = data
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "ignore")
        raise SystemExit(f"Lỗi HTTP {e.code} khi gọi {url}\n{detail}")
    except urllib.error.URLError as e:
        raise SystemExit(f"Không kết nối được tới {url}: {e.reason}")


def test_connection(env):
    me = request(env, "GET", "/users/me?context=edit")
    print(f"✓ Kết nối OK. Đăng nhập với: {me.get('name')} (id={me.get('id')})")
    return True


def get_or_create_category(env, name):
    cats = request(env, "GET", f"/categories?search={urllib.parse.quote(name)}")
    for c in cats:
        if c.get("name", "").lower() == name.lower():
            return c["id"]
    created = request(env, "POST", "/categories", {"name": name})
    return created["id"]


def create_page(env, title, content, status="draft"):
    page = request(env, "POST", "/pages",
                   {"title": title, "content": content, "status": status})
    print(f"✓ Đã tạo trang: {page.get('link')} (status={status})")
    return page


def create_post(env, title, content, category=None, status="draft"):
    payload = {"title": title, "content": content, "status": status}
    if category:
        payload["categories"] = [get_or_create_category(env, category)]
    post = request(env, "POST", "/posts", payload)
    print(f"✓ Đã tạo bài: {post.get('link')} (status={status})")
    return post


def upload_media(env, source):
    """source: đường dẫn file local hoặc URL ảnh."""
    if source.startswith("http"):
        data = urllib.request.urlopen(source, timeout=30).read()
        filename = source.split("/")[-1].split("?")[0] or "image.jpg"
    else:
        with open(source, "rb") as f:
            data = f.read()
        filename = os.path.basename(source)
    ctype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    media = request(env, "POST", "/media", data,
                    extra_headers={"Content-Type": ctype,
                                   "Content-Disposition": f'attachment; filename="{filename}"'})
    print(f"✓ Đã upload ảnh: {media.get('source_url')}")
    return media


def main():
    p = argparse.ArgumentParser(description="WordPress REST API helper")
    p.add_argument("--test", action="store_true")
    p.add_argument("--create-page", nargs=2, metavar=("TITLE", "HTML_FILE"))
    p.add_argument("--create-post", nargs=2, metavar=("TITLE", "HTML_FILE"))
    p.add_argument("--category")
    p.add_argument("--upload", metavar="FILE_OR_URL")
    p.add_argument("--status", default="draft", choices=["draft", "publish"])
    args = p.parse_args()
    env = load_env()

    if args.test:
        test_connection(env)
    elif args.create_page:
        title, html = args.create_page
        create_page(env, title, open(html, encoding="utf-8").read(), args.status)
    elif args.create_post:
        title, html = args.create_post
        create_post(env, title, open(html, encoding="utf-8").read(), args.category, args.status)
    elif args.upload:
        upload_media(env, args.upload)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
