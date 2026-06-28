#!/usr/bin/env python3
"""
get-token.py — Đổi 'code' OAuth2 của WordPress.com lấy access token.

Đọc WP_CLIENT_ID, WP_CLIENT_SECRET, WP_REDIRECT_URI, WP_OAUTH_CODE từ .env,
gọi endpoint token của WordPress.com, rồi ghi WP_BEARER_TOKEN trở lại .env.
KHÔNG in ra secret/token đầy đủ.

Dùng: python get-token.py
"""
import os
import json
import urllib.parse
import urllib.request
import urllib.error

ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
TOKEN_URL = "https://public-api.wordpress.com/oauth2/token"


def read_env(path):
    env = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if s and not s.startswith("#") and "=" in s:
                k, v = s.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def write_token(path, token):
    lines = open(path, encoding="utf-8").read().splitlines()
    found = False
    for i, line in enumerate(lines):
        if line.strip().startswith("WP_BEARER_TOKEN="):
            lines[i] = "WP_BEARER_TOKEN=" + token
            found = True
            break
    if not found:
        lines.append("WP_BEARER_TOKEN=" + token)
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")


def main():
    env = read_env(ENV_PATH)
    required = ["WP_CLIENT_ID", "WP_CLIENT_SECRET", "WP_REDIRECT_URI", "WP_OAUTH_CODE"]
    missing = [k for k in required if not env.get(k)]
    if missing:
        raise SystemExit("Thiếu trong .env: " + ", ".join(missing))

    data = urllib.parse.urlencode({
        "client_id": env["WP_CLIENT_ID"],
        "client_secret": env["WP_CLIENT_SECRET"],
        "redirect_uri": env["WP_REDIRECT_URI"],
        "code": env["WP_OAUTH_CODE"],
        "grant_type": "authorization_code",
    }).encode()

    req = urllib.request.Request(TOKEN_URL, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            res = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "ignore")
        raise SystemExit(f"Lỗi {e.code} khi đổi token:\n{detail}")

    token = res.get("access_token")
    if not token:
        raise SystemExit("Không nhận được access_token. Phản hồi: " + json.dumps(res))

    write_token(ENV_PATH, token)
    masked = token[:6] + "..." + token[-4:]
    print("✓ Lấy token thành công và đã lưu vào .env")
    print(f"  Token (ẩn bớt): {masked}")
    print(f"  Site: {res.get('blog_url')}  (blog_id={res.get('blog_id')})")
    print(f"  Scope: {res.get('scope')}")


if __name__ == "__main__":
    main()
