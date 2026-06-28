#!/usr/bin/env python3
"""
scrape-site.py — Cào dữ liệu cơ bản từ website chính phục vụ dựng Social WordPress.

Trích xuất: meta description, ảnh OpenGraph, các link sản phẩm/bài viết, và một số
thông tin liên hệ (điện thoại, email) tìm thấy trong trang. Kết quả lưu ra
scraped-data.json để các bước sau dùng lại (không nhồi hết vào context).

Lưu ý: đây là bộ cào tổng quát dựa trên HTML tĩnh. Với website render bằng
JavaScript, kết quả có thể thiếu — khi đó dùng Playwright MCP hoặc nhập tay
(xem mục "Trường hợp ngách" trong SKILL.md).

Cách dùng:
  python scrape-site.py https://website-chinh.vn
"""
import re
import sys
import json
import html
import urllib.request


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (skill-scraper)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        charset = r.headers.get_content_charset() or "utf-8"
        return r.read().decode(charset, "ignore")


def meta(content, prop):
    for pat in (
        rf'<meta[^>]+name=["\']{prop}["\'][^>]+content=["\']([^"\']+)["\']',
        rf'<meta[^>]+property=["\']og:{prop}["\'][^>]+content=["\']([^"\']+)["\']',
        rf'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']{prop}["\']',
    ):
        m = re.search(pat, content, re.I)
        if m:
            return html.unescape(m.group(1).strip())
    return ""


def find_links(content, base):
    links = re.findall(r'<a[^>]+href=["\']([^"\']+)["\']', content, re.I)
    products, posts = set(), set()
    for href in links:
        low = href.lower()
        if any(k in low for k in ("/san-pham", "/product", "/shop", "/danh-muc", "/category")):
            products.add(href)
        if any(k in low for k in ("/tin-tuc", "/blog", "/bai-viet", "/news", "/post")):
            posts.add(href)
    return sorted(products)[:30], sorted(posts)[:30]


def contacts(content):
    phones = re.findall(r'(?:(?:\+?84|0)\d{8,10})', content)
    emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', content)
    return {
        "phones": sorted(set(phones))[:5],
        "emails": sorted(set(e for e in emails if not e.endswith((".png", ".jpg")))) [:5],
    }


def main():
    if len(sys.argv) < 2:
        print("Dùng: python scrape-site.py <url_website_chinh>")
        sys.exit(1)
    url = sys.argv[1]
    content = fetch(url)
    products, posts = find_links(content, url)
    data = {
        "source": url,
        "title": meta(content, "title") or (re.search(r"<title>(.*?)</title>", content, re.I | re.S).group(1).strip() if re.search(r"<title>(.*?)</title>", content, re.I | re.S) else ""),
        "description": meta(content, "description"),
        "og_image": meta(content, "image"),
        "product_links": products,
        "post_links": posts,
        "contacts": contacts(content),
    }
    out = "scraped-data.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✓ Đã lưu {out}")
    print(f"  - Mô tả: {data['description'][:80]}")
    print(f"  - {len(products)} link sản phẩm/danh mục, {len(posts)} link bài viết")
    print(f"  - Liên hệ: {data['contacts']}")
    print("  ! Lưu ý: kiểm tra lại, bổ sung thủ công nếu website dùng JavaScript render.")


if __name__ == "__main__":
    main()
