#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sinh nội dung Gutenberg BLOCK cho Social WordPress — DATA-DRIVEN.

Đọc dữ liệu dự án từ project.json (xem project.example.json để biết cấu trúc),
sinh ra homepage.html, about.html, footer.html ở định dạng block.

Dùng: python build-pages.py [project.json]   (mặc định: project.json)

Lưu ý các bài học đã đúc kết (chi tiết trong SKILL.md):
- Phải dùng block Gutenberg (theme block bỏ qua HTML thuần).
- Layout sản phẩm dùng wp:columns (tự xếp dọc trên mobile), KHÔNG dùng grid
  columnCount (không co lại trên mobile -> vỡ chữ).
- Footer đặt ở template-part của theme, KHÔNG nhét vào trang (tránh 2 footer).
"""
import sys
import json
import html

CFG = sys.argv[1] if len(sys.argv) > 1 else "project.json"
D = json.load(open(CFG, encoding="utf-8"))

BRAND = D.get("brand_color", "#00529C")
SITE = D.get("site", "")
BANNER = D.get("banner", "")
LOGO = D.get("logo", "")
CONTACT = D.get("contact", {})
BIO_SHORT = D.get("bio_short", "")
BIO_LONG = D.get("bio_long", "")
DESC = D.get("description", "")
SOCIAL = D.get("social", [])
CATEGORIES = D.get("categories", [])
BLOG_CAT_ID = D.get("blog_category_id", 0)


def heading(text, level=2, center=False, color=BRAND, align=None):
    parts = []
    if align:
        parts.append(f'"align":"{align}"')
    if center:
        parts.append('"textAlign":"center"')
    parts.append(f'"level":{level}')
    if color:
        parts.append(f'"style":{{"color":{{"text":"{color}"}}}}')
    attrs = '{' + ",".join(parts) + '}'
    cls = 'wp-block-heading' + (f' align{align}' if align else '') + (' has-text-align-center' if center else '') + (' has-text-color' if color else '')
    style = f' style="color:{color}"' if color else ''
    return f'<!-- wp:heading {attrs} --><h{level} class="{cls}"{style}>{html.escape(text)}</h{level}><!-- /wp:heading -->'


def para(text, center=False, white=False):
    align_attr = '"align":"center"' if center else ''
    color_attr = '"style":{"color":{"text":"#ffffff"}}' if white else ''
    inner = ",".join(x for x in [align_attr, color_attr] if x)
    a = f' {{{inner}}}' if inner else ''
    cls = []
    if center:
        cls.append('has-text-align-center')
    if white:
        cls.append('has-text-color')
    cls_attr = f' class="{" ".join(cls)}"' if cls else ''
    style = ' style="color:#ffffff"' if white else ''
    return f'<!-- wp:paragraph{a} --><p{cls_attr}{style}>{text}</p><!-- /wp:paragraph -->'


def image(url, alt, width=None, full=False):
    attrs = {}
    if width:
        attrs['width'] = width
    if full:
        attrs['align'] = 'full'
    a = ' ' + json.dumps(attrs) if attrs else ''
    cls = 'wp-block-image' + (' alignfull' if full else '')
    return (f'<!-- wp:image{a} --><figure class="{cls}">'
            f'<img src="{url}" alt="{html.escape(alt)}"/></figure><!-- /wp:image -->')


def product_image(url, alt):
    return ('<!-- wp:image {"aspectRatio":"1","scale":"contain","sizeSlug":"large"} -->'
            '<figure class="wp-block-image size-large">'
            f'<img src="{url}" alt="{html.escape(alt)}" style="aspect-ratio:1;object-fit:contain"/>'
            '</figure><!-- /wp:image -->')


def button(text, url, center=True):
    a_align = ' {"layout":{"type":"flex","justifyContent":"center"}}' if center else ''
    cls = 'wp-block-buttons' + (' is-content-justification-center' if center else '')
    return (f'<!-- wp:buttons{a_align} --><div class="{cls}">'
            '<!-- wp:button {"style":{"color":{"background":"' + BRAND + '"}}} -->'
            '<div class="wp-block-button"><a class="wp-block-button__link has-background wp-element-button" '
            f'href="{url}" target="_blank" rel="noreferrer noopener" style="background-color:{BRAND}">{html.escape(text)}</a></div>'
            '<!-- /wp:button --></div><!-- /wp:buttons -->')


def product_card(item):
    """1 thẻ sản phẩm = group bo viền; chiều cao tự cân bằng do column stretch."""
    title, path, img = item.get("title", ""), item.get("path", ""), item.get("image", "")
    url = (SITE + path) if path.startswith("/") else path
    inner = (product_image(img, title) if img else "") \
        + para("<strong>" + html.escape(title) + "</strong>", center=True) \
        + button("Xem sản phẩm →", url)
    attrs = ('{"style":{"border":{"radius":"12px","width":"1px","color":"#e3e8ef"},'
             '"spacing":{"padding":{"top":"16px","bottom":"16px","left":"16px","right":"16px"}}},'
             '"backgroundColor":"white","layout":{"type":"flex","orientation":"vertical"}}')
    return (f'<!-- wp:group {attrs} -->'
            '<div class="wp-block-group has-white-background-color has-background has-border-color" '
            'style="border-color:#e3e8ef;border-width:1px;border-radius:12px;'
            'padding-top:16px;padding-bottom:16px;padding-left:16px;padding-right:16px">'
            + inner + '</div><!-- /wp:group -->')


def category_columns(items):
    """wp:columns: desktop chia đều ngang, MOBILE tự xếp dọc. KHÔNG đặt width cột."""
    cols = "".join('<!-- wp:column --><div class="wp-block-column">' + product_card(it) + '</div><!-- /wp:column -->'
                   for it in items)
    attrs = ('{"align":"full","verticalAlignment":"stretch",'
             '"style":{"spacing":{"padding":{"left":"40px","right":"40px"}}}}')
    return (f'<!-- wp:columns {attrs} -->'
            '<div class="wp-block-columns alignfull are-vertically-aligned-stretch" '
            'style="padding-left:40px;padding-right:40px">'
            + cols + '</div><!-- /wp:columns -->')


def latest_posts(cat_id):
    attrs = ('{"postsToShow":5,"order":"desc","orderBy":"date",'
             '"displayPostContent":true,"displayPostContentRadio":"excerpt","excerptLength":22,'
             '"displayPostDate":true,"displayFeaturedImage":true,'
             '"featuredImageSizeSlug":"medium","addLinkToFeaturedImage":true,'
             f'"categories":[{{"id":{cat_id},"value":"{cat_id}"}}],'
             '"align":"wide"}')
    return f'<!-- wp:latest-posts {attrs} /-->'


def homepage():
    p = []
    if BANNER:
        p.append(image(BANNER, "Banner", full=True))
    if LOGO:
        p.append(image(LOGO, "Logo", width="120px"))
    p.append(heading(BIO_SHORT, level=2, center=True, align="wide"))
    p.append(para(html.escape(DESC), center=True))
    p.append(heading("Sản phẩm nổi bật", level=2, align="wide", center=True))
    for cat in CATEGORIES:
        p.append(heading(cat["name"], level=3, color="#1a2b3c", align="wide", center=True))
        p.append(category_columns(cat["items"]))
    if BLOG_CAT_ID:
        p.append(heading("Bài viết mới nhất", level=2, align="wide", center=True))
        p.append(latest_posts(BLOG_CAT_ID))
    return "\n".join(p)


def footer_part():
    """Footer thương hiệu, dùng để THAY content template-part footer của theme."""
    contact = (heading("Thông tin liên hệ", level=3, color="#ffffff")
               + para(f"☎ Hotline: {CONTACT.get('phone','')}", white=True)
               + para("📍 " + html.escape(CONTACT.get('address', '')), white=True)
               + para(f'🌐 Website: <a href="{SITE}" target="_blank" rel="noreferrer noopener">{SITE.replace("https://","").replace("http://","")}</a>', white=True)
               + para(f"✉ Email: {CONTACT.get('email','')}", white=True))
    socials = " · ".join(f'<a href="{u}" target="_blank" rel="noreferrer noopener">{n}</a>' for n, u in SOCIAL)
    about_col = (heading("Giới thiệu", level=3, color="#ffffff")
                 + para(html.escape(BIO_LONG), white=True)
                 + para(socials, white=True))
    footer_cols = ('<!-- wp:columns {"style":{"spacing":{"blockGap":{"left":"60px"}}}} -->'
                   '<div class="wp-block-columns">'
                   '<!-- wp:column {"width":"45%"} --><div class="wp-block-column" style="flex-basis:45%">' + contact + '</div><!-- /wp:column -->'
                   '<!-- wp:column {"width":"55%"} --><div class="wp-block-column" style="flex-basis:55%">' + about_col + '</div><!-- /wp:column -->'
                   '</div><!-- /wp:columns -->')
    attrs = ('{"align":"full","style":{"color":{"background":"' + BRAND + '","text":"#ffffff"},'
             '"spacing":{"padding":{"top":"40px","bottom":"30px","left":"60px","right":"60px"}}},'
             '"layout":{"type":"default"}}')
    return (f'<!-- wp:group {attrs} -->'
            f'<div class="wp-block-group alignfull has-text-color has-background" '
            f'style="color:#ffffff;background-color:{BRAND};padding-top:40px;padding-bottom:30px;padding-left:60px;padding-right:60px">'
            + footer_cols + '</div><!-- /wp:group -->')


def about():
    return "\n".join([
        image(LOGO, "Logo", width="140px") if LOGO else "",
        heading("Về Website Chính Thức", level=2),
        para("<em>[NỘI DUNG GIỚI THIỆU — nhập chi tiết sau]</em>"),
        para(html.escape(BIO_LONG)),
        para(f'Website chính thức: <a href="{SITE}" target="_blank" rel="noreferrer noopener">{SITE}</a>'),
    ])


if __name__ == "__main__":
    open("homepage.html", "w", encoding="utf-8").write(homepage())
    open("about.html", "w", encoding="utf-8").write(about())
    open("footer.html", "w", encoding="utf-8").write(footer_part())
    print(f"✓ Đã sinh homepage.html, about.html, footer.html từ {CFG}")
