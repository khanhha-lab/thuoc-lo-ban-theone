#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sinh nội dung Gutenberg BLOCK cho Vinamilk Social:
- Trang chủ (có ảnh sản phẩm thật, thẻ đồng kích thước, KHÔNG footer trong trang)
- Trang giới thiệu
- Footer thương hiệu (dùng để thay template-part footer của theme -> tránh 2 footer)
"""
import json
import html

BRAND = "#00529C"
BANNER = "https://vinamilk76.wordpress.com/wp-content/uploads/2026/06/banner.jpg"
LOGO = "https://vinamilk76.wordpress.com/wp-content/uploads/2026/06/logo.png"
SITE = "https://www.vinamilk.com.vn"

PHONE = "1900 636 979"
ADDRESS = "10 Tân Trào, Phường Tân Mỹ, Thành phố Hồ Chí Minh"
EMAIL = "vinamilk@vinamilk.com.vn"
BIO_SHORT = "Vinamilk - Mang nguồn dinh dưỡng từ sữa chất lượng đến mọi gia đình Việt"
BIO_LONG = ("Thành lập năm 1976, Vinamilk là thương hiệu sữa hàng đầu Việt Nam với đa dạng "
            "sản phẩm như sữa tươi, sữa bột, sữa chua... Vinamilk mang đến nguồn sữa sạch, "
            "chất lượng, hương vị thơm ngon và giá trị dinh dưỡng cho mọi độ tuổi.")
DESC = ("Tại Vinamilk, chúng tôi vun đắp hành trình dinh dưỡng gần 50 năm qua bằng khát vọng "
        "nâng cao tầm vóc Việt với những sản phẩm đạt chuẩn quốc tế, phù hợp mọi lứa tuổi.")

SOCIAL = [
    ("Facebook", "https://www.facebook.com/vinamilkofficial/"),
    ("YouTube", "https://www.youtube.com/@vinamilk"),
    ("Instagram", "https://www.instagram.com/vinamilk/"),
    ("TikTok", "https://www.tiktok.com/@vinamilk.official"),
    ("LinkedIn", "https://www.linkedin.com/company/vinamilk"),
]

CATEGORIES = [
    ("Sữa tươi", [
        ("Sữa tươi thanh trùng nguyên chất Green Farm không đường", "/products/sua-tuoi-thanh-trung-nguyen-chat-vinamilk-green-farm-khong-duong"),
        ("Sữa tươi tiệt trùng Green Farm nguyên chất", "/products/sua-tuoi-tiet-trung-green-farm-nguyen-chat"),
        ("Sữa tươi tiệt trùng hương dâu", "/products/sua-tuoi-tiet-trung-huong-dau"),
    ]),
    ("Sữa chua", [
        ("Sữa chua uống Probi lựu đỏ ít đường", "/products/sua-chua-uong-probi-luu-do-it-duong"),
        ("Sữa chua uống thanh trùng Green Farm", "/products/sua-chua-uong-thanh-trung-green-farm"),
        ("Sữa chua Vinamilk Green Farm ít đường", "/products/sua-chua-vinamilk-green-farm-it-duong"),
    ]),
    ("Sữa hạt", [
        ("Sữa hạt cao đạm Vinamilk", "/products/sua-hat-cao-dam-vinamilk"),
        ("Sữa hạt Vinamilk 9 loại hạt", "/products/sua-hat-vinamilk-9-loai-hat"),
        ("Sữa hạt Vinamilk 9 loại hạt không đường", "/products/sua-hat-vinamilk-9-loai-hat-khong-duong"),
    ]),
    ("Kem", [
        ("Kem Gelato Matcha Vinamilk", "/products/kem-gelato-matcha-vinamilk"),
        ("Kem mịn sầu riêng Vinamilk", "/products/kem-min-sau-rieng-vinamilk"),
        ("Kem mịn Vinamilk dừa", "/products/kem-min-vinamilk-dua"),
    ]),
    ("Nước ép & Trà", [
        ("Nước ép kiwi táo collagen Vinamilk", "/products/nuoc-ep-kiwi-tao-collagen-vinamilk"),
        ("Trà atiso ít đường Vfresh", "/products/tra-atiso-it-duong-vfresh"),
    ]),
]

BLOGS = [
    ("Công thức món ngon", "/blogs/cong-thuc-mon-ngon"),
    ("Đẹp da đẹp dáng", "/blogs/dep-da-dep-dang"),
    ("Góc chuyên gia", "/blogs/goc-chuyen-gia"),
    ("Thông tin dinh dưỡng", "/blogs/thong-tin-dinh-duong"),
]

try:
    PRODUCT_IMG = json.load(open("product-images.json", encoding="utf-8"))
except FileNotFoundError:
    PRODUCT_IMG = {}


def heading(text, level=2, center=False, color=BRAND):
    a_align = '"textAlign":"center",' if center else ''
    attrs = f'{{{a_align}"level":{level}' + (f',"style":{{"color":{{"text":"{color}"}}}}' if color else '') + '}'
    cls = 'wp-block-heading' + (' has-text-align-center' if center else '') + (' has-text-color' if color else '')
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


def image(url, alt, width=None):
    w = f' {{"width":"{width}"}}' if width else ''
    return (f'<!-- wp:image{w} --><figure class="wp-block-image">'
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


def product_card_column(title, path):
    url = SITE + path
    img = PRODUCT_IMG.get(path, "")
    inner = (product_image(img, title) if img else "") \
        + para("<strong>" + html.escape(title) + "</strong>", center=True) \
        + button("Xem sản phẩm →", url)
    return ('<!-- wp:column {"width":"33.33%"} -->'
            '<div class="wp-block-column" style="flex-basis:33.33%">' + inner + '</div>'
            '<!-- /wp:column -->')


def category_block(items):
    cols = "".join(product_card_column(t, p) for t, p in items)
    return ('<!-- wp:columns {"verticalAlignment":"stretch"} -->'
            '<div class="wp-block-columns are-vertically-aligned-stretch">' + cols + '</div>'
            '<!-- /wp:columns -->')


def blog_list():
    items = "".join(
        f'<!-- wp:list-item --><li><a href="{SITE+p}" target="_blank" rel="noreferrer noopener">{html.escape(t)}</a></li><!-- /wp:list-item -->'
        for t, p in BLOGS)
    return f'<!-- wp:list --><ul class="wp-block-list">{items}</ul><!-- /wp:list -->'


def homepage():
    p = []
    p.append(image(BANNER, "Vinamilk banner"))
    p.append(image(LOGO, "Vinamilk logo", width="120px"))
    p.append(heading(BIO_SHORT, level=2, center=True))
    p.append(para(html.escape(DESC), center=True))
    p.append(heading("Sản phẩm nổi bật", level=2))
    for cat, items in CATEGORIES:
        p.append(heading(cat, level=3, color="#1a2b3c"))
        p.append(category_block(items))
    p.append(heading("Bài viết mới nhất", level=2))
    p.append(blog_list())
    # KHÔNG còn footer trong trang -> footer nằm ở template-part của theme
    return "\n".join(p)


def footer_part():
    """Footer thương hiệu, dùng để THAY content của template-part footer (theme)."""
    contact = (heading("Thông tin liên hệ", level=3, color="#ffffff")
               + para(f"☎ Hotline: {PHONE}", white=True)
               + para("📍 " + html.escape(ADDRESS), white=True)
               + para(f'🌐 Website: <a href="{SITE}" target="_blank" rel="noreferrer noopener">vinamilk.com.vn</a>', white=True)
               + para(f"✉ Email: {EMAIL}", white=True))
    socials = " · ".join(f'<a href="{u}" target="_blank" rel="noreferrer noopener">{n}</a>' for n, u in SOCIAL)
    about_col = (heading("Về Vinamilk", level=3, color="#ffffff")
                 + para(html.escape(BIO_LONG), white=True)
                 + para(socials, white=True))
    footer_cols = ('<!-- wp:columns --><div class="wp-block-columns">'
                   '<!-- wp:column --><div class="wp-block-column">' + contact + '</div><!-- /wp:column -->'
                   '<!-- wp:column --><div class="wp-block-column">' + about_col + '</div><!-- /wp:column -->'
                   '</div><!-- /wp:columns -->')
    attrs = ('{"align":"full","style":{"color":{"background":"' + BRAND + '","text":"#ffffff"},'
             '"spacing":{"padding":{"top":"40px","bottom":"30px","left":"24px","right":"24px"}}},'
             '"layout":{"type":"constrained"}}')
    return (f'<!-- wp:group {attrs} -->'
            f'<div class="wp-block-group alignfull has-text-color has-background" '
            f'style="color:#ffffff;background-color:{BRAND};padding-top:40px;padding-bottom:30px;padding-left:24px;padding-right:24px">'
            + footer_cols + '</div><!-- /wp:group -->')


def about():
    return "\n".join([
        image(LOGO, "Vinamilk logo", width="140px"),
        heading("Về Website Chính Thức", level=2),
        para("<em>[NỘI DUNG GIỚI THIỆU — bạn nhập chi tiết sau]</em>"),
        para(html.escape(BIO_LONG)),
        para(f'Website chính thức: <a href="{SITE}" target="_blank" rel="noreferrer noopener">{SITE}</a>'),
    ])


if __name__ == "__main__":
    open("homepage.html", "w", encoding="utf-8").write(homepage())
    open("about.html", "w", encoding="utf-8").write(about())
    open("footer.html", "w", encoding="utf-8").write(footer_part())
    print("✓ Đã tạo homepage.html, about.html, footer.html (block, có ảnh sản phẩm, footer riêng)")
