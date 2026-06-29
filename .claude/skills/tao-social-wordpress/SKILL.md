---
name: tao-social-wordpress
description: >-
  Tự động dựng cấu trúc một website "Social" trên WordPress dựa trên dữ liệu cào
  từ website chính của khách hàng. Dùng khi user muốn tạo nhanh một trang
  WordPress vệ tinh (trang chủ + giới thiệu) lấy nội dung sản phẩm, bài viết và
  thông tin liên hệ từ website gốc. Kích hoạt với 2 tham số: tên social và URL
  website chính.
user-invokable: true
argument-hint: "<ten_social_muon_tao> <url_website_chinh>"
license: MIT
metadata:
  author: "Khanh Ha"
  version: "2.0.0"
  category: "seo-social"
---

# Tạo Social WordPress từ website chính

Skill này nhận `<ten_social_muon_tao>` và `<url_website_chinh>`, cào nội dung từ
website chính rồi dựng cấu trúc cho một site WordPress vệ tinh phục vụ
social/SEO. Áp dụng được cho **mọi dự án** — chỉ cần đổi 2 tham số đầu vào.

## Khi nào dùng skill này
- User muốn tạo một trang WordPress vệ tinh để phân phối nội dung / build social.
- Đã có (hoặc sẽ tạo) một site WordPress trống và một website chính làm nguồn dữ liệu.

## Khi nào KHÔNG dùng
- Chưa có website chính (`<url_website_chinh>`) để cào dữ liệu.
- Muốn tạo site WordPress **hoàn toàn tự động không cần thao tác tay** → bất khả thi
  (xem "Vết xe đổ"). Hãy báo user thực hiện bước tạo site trống trước.

---

## 0. Tiền điều kiện & Kết nối nền tảng ngoài  (tiêu chí: kết nối API)

Skill kết nối WordPress qua **REST API** (`/wp-json/wp/v2/`). Trước khi chạy, kiểm tra:

1. **Site đích đã tồn tại chưa.** Nếu chưa, hướng dẫn user tạo 1 lần (xem Vết xe đổ #1).
2. **File `.env` đã có thông tin đăng nhập chưa.** Cần các biến (xem `.env.example`):
   - `WP_API_BASE` — vd `https://<ten_social>.wordpress.com/wp-json/wp/v2`
   - `WP_USER` + `WP_APP_PASSWORD` (self-hosted / Application Password) **HOẶC**
   - `WP_BEARER_TOKEN` (WordPress.com OAuth2)
3. **Bảo mật (bắt buộc):** key chỉ nằm trong `.env`. TUYỆT ĐỐI không hardcode vào code
   hay commit lên GitHub. Đảm bảo `.env` đã nằm trong `.gitignore`.
4. **Test kết nối trước khi làm gì khác:** chạy `python wp_client.py --test`. Nếu fail,
   dừng lại và báo user, KHÔNG tiếp tục dựng trang.

---

## 1. Quy trình thực thi từng bước  (tiêu chí: framework)

### Bước 1 — Cào & phân tích website chính
- Truy cập `<url_website_chinh>`, trích xuất:
  - `meta description` (dùng cho mô tả website).
  - **Sản phẩm:** mỗi danh mục lớn lấy đúng **3 sản phẩm đầu tiên** (tên, ảnh, link).
  - **Bài viết:** danh sách blog mới nhất (tiêu đề, ảnh, link).
  - **Thông tin liên hệ:** điện thoại, địa chỉ, email, website chính thức.
- Dùng helper `scrape-site.py` hoặc WebFetch. Ghi kết quả ra `scraped-data.json` để bước
  sau dùng lại (load on-demand, không nhồi hết vào context).

### Bước 2 — Dựng Trang chủ (Homepage)
Tạo qua API theo bố cục:
- **Banner:** chèn placeholder (`[BANNER — user cung cấp ảnh sau]`).
- **Mô tả website:** dùng mô tả user cung cấp, nếu không có thì lấy `meta description` đã cào.
- **Khối sản phẩm:** 3 sản phẩm/danh mục, kèm ảnh + link về website chính.
- **Khối bài viết:** danh sách blog mới nhất đã cào.
- **Footer 2 khối:**
  - *Khối 1 — Giới thiệu:* điện thoại, địa chỉ, website chính thức, email.
  - *Khối 2 — Social & Bio:* đoạn bio ngắn + link Facebook, TikTok, Pinterest, YouTube
    (để placeholder nếu user chưa cung cấp link).

### Bước 3 — Dựng Trang "Giới thiệu"
- Tạo page template trống với tiêu đề "Về Website Chính Thức".
- Chèn placeholder `[NỘI DUNG GIỚI THIỆU — user nhập sau]`. Không tự bịa nội dung.

### Bước 4 — Nghiệm thu
- Đối chiếu toàn bộ với `checklist.md`. Chỉ báo "hoàn thành" khi mọi mục đạt.

---

## 2. Tiêu chí chất lượng  (tiêu chí: chuẩn đánh giá)
- Trang chủ có đủ 5 khối: banner, mô tả, sản phẩm, bài viết, footer 2 cột.
- Mỗi danh mục hiển thị đúng 3 sản phẩm (không nhiều/ít hơn), ảnh tải được.
- Mọi link sản phẩm/bài viết trỏ đúng về `<url_website_chinh>`.
- Không có dữ liệu bịa: thiếu thông tin → để placeholder, không tự đặt số liệu.
- `.env` không bị commit; không có key nào lộ trong code.

## 3. Mức độ tự tin & trường hợp ngách  (tiêu chí: ca khó)
- **Cào không ra danh mục/sản phẩm** (site dùng JS render động): báo user, đề xuất
  user cung cấp danh sách thủ công hoặc dùng Playwright MCP để render.
- **Không tìm thấy meta description:** hỏi user mô tả, KHÔNG tự viết thay.
- **Site có >5 danh mục:** xác nhận với user nên hiển thị danh mục nào lên trang chủ.
- **Không chắc đâu là "danh mục lớn":** liệt kê các danh mục tìm được cho user chọn,
  không tự suy đoán.

## 4. Định dạng output  (tiêu chí: format)
Kết thúc, báo cáo bằng bảng Markdown gồm:
| Hạng mục | Kết quả | Link |
- Link trang chủ + trang giới thiệu đã tạo.
- Danh sách sản phẩm/bài viết đã đẩy lên.
- Các placeholder user cần bổ sung sau (banner, bio, link social, nội dung giới thiệu).

---

## 5. Vết xe đổ — TRÁNH các lỗi sau  (tiêu chí: pitfalls)
1. **KHÔNG thể tạo site WordPress.com 100% tự động** (cần xác minh email + captcha).
   → Hướng dẫn user tạo site trống 1 lần rồi skill lo phần còn lại.
2. **Gói FREE KHÔNG có Application Password.** Phải dùng **OAuth2**: tạo app tại
   developer.wordpress.com/apps → lấy Client ID/Secret → xin `code` (scope=global) →
   đổi lấy `access_token` (xem `get-token.py`). Redirect URL **không được chứa chữ
   "wordpress"** (dùng `https://example.com`). API base:
   `https://public-api.wordpress.com/wp/v2/sites/<site>`.
3. **‼ Nội dung phải ở định dạng GUTENBERG BLOCK** (`<!-- wp:... -->`). Theme block của
   WordPress.com sẽ **bỏ qua HTML `<div>` + inline CSS thuần** khi render ra ngoài
   (dù API vẫn lưu). Luôn sinh block (heading/paragraph/image/columns/group/buttons).
4. **‼ Site mới mặc định ở chế độ "Coming Soon"** → khách vãng lai chỉ thấy trang
   "sẽ đến sớm", còn API (đã đăng nhập) vẫn thấy nội dung → rất dễ tưởng nhầm là lỗi.
   Phải **launch site**: POST `/rest/v1.1/sites/<site>/launch` và set
   `wpcom_coming_soon=0`, `wpcom_public_coming_soon=0`, `blog_public=1`.
5. **Trang chủ tĩnh:** publish page rồi set `show_on_front=page` + `page_on_front=<id>`
   để trang hiện ngay tại domain gốc (không phải `/trang-chu/`).
6. **Kiểm tra render ở FRONT-END** (fetch URL công khai), đừng chỉ tin field `rendered`
   của API — hai nơi có thể khác nhau (do block bị lọc hoặc coming-soon).
7. **Đừng hardcode key** — chỉ để trong `.env` (đã .gitignore).
8. **Đừng đăng publish khi chưa hỏi** — mặc định `draft`; chỉ publish khi user đồng ý.
9. **Đừng cào quá nhiều** rồi nhồi vào context — lưu `scraped-data.json`, đọc on-demand.
10. **Đừng bịa thông tin** (liên hệ, mô tả) — thiếu thì để placeholder.
11. **Ảnh Google Drive** phải ở chế độ public + đổi link `uc?export=download&id=<ID>`;
    nên tải về rồi upload qua API (file quá nhỏ/sai định dạng sẽ bị từ chối).
12. **Tránh 2 footer:** theme block đã có footer riêng (template-part `area=footer`).
    Đừng nhét footer vào nội dung trang (sẽ thành 2 footer). Thay vào đó **cập nhật
    content của template-part footer** qua `POST /template-parts/<id>` (URL-encode `id`,
    vd `pub/assembler//footer`).
13. **Ảnh sản phẩm:** trang cào tĩnh thường không có ảnh; lấy ảnh thật bằng cách fetch
    từng trang sản phẩm rồi đọc thẻ `og:image`. Dùng block image `aspectRatio`+`scale`
    để các thẻ đồng kích thước.
14. **Layout sản phẩm — dùng `wp:columns`, KHÔNG dùng grid:**
    - ĐỪNG đặt `width`/`flex-basis` cho `wp:column` (cộng gap > 100% → wrap → dọc trên desktop).
    - ĐỪNG dùng `grid` + `columnCount` (cố định, **không co lại trên mobile** → cột quá hẹp,
      chữ trong nút vỡ mỗi dòng 1 ký tự).
    - ✅ Dùng `wp:columns` KHÔNG đặt width: desktop chia đều ngang (flex), **mobile tự xếp dọc**
      (isStackedOnMobile mặc định). Thêm `verticalAlignment:stretch` để các thẻ cao bằng nhau,
      `align:"full"` để dàn rộng. Mỗi thẻ là 1 group bo viền bên trong column.
15. **Logo header:** theme hiện chữ qua `<!-- wp:site-title /-->`. Thay logo bằng cách set
    option `site_logo=<media_id>` và đổi block đó thành `<!-- wp:site-logo {"width":150} /-->`
    trong template-part `header`.
16. **Blog "3 bài mới nhất 1 category":** site mới chưa có bài → tạo category + ≥3 post
    (publish) rồi dùng `wp:latest-posts {"postsToShow":3,"categories":[{"id":<id>,"value":"<id>"}]}`.
    (Block này chỉ hiển thị bài của CHÍNH site, không kéo được bài từ web ngoài.)

---

## 6. File bổ trợ (load on-demand — chỉ đọc khi cần)
- `get-token.py` — đổi `code` OAuth2 → `access_token`, lưu vào `.env` (cho gói free).
- `scrape-site.py` — cào meta, sản phẩm, bài viết, liên hệ từ website chính → `scraped-data.json`.
- `build-pages.py` — **data-driven**: đọc `project.json` → sinh `homepage.html`,
  `about.html`, `footer.html` (định dạng Gutenberg block). Dùng: `python build-pages.py project.json`.
- `project.example.json` — **mẫu dữ liệu dự án** (Vinamilk): màu thương hiệu, logo/banner,
  liên hệ, bio, social, danh mục + sản phẩm (kèm ảnh), `blog_category_id`. Sao chép thành
  `project.json` rồi điền cho dự án mới.
- `wp_client.py` — gọi WordPress REST API: test kết nối, tạo page/post, upload ảnh, tạo category.
- `checklist.md` — bảng nghiệm thu trước khi báo hoàn thành.
- `.env.example` — mẫu khai báo thông tin đăng nhập (sao chép thành `.env` rồi điền).

> **Quy trình gọn:** điền `.env` (key) + `project.json` (dữ liệu) → `python wp_client.py --test`
> → `python build-pages.py project.json` → đẩy `homepage.html`/`about.html` qua API, thay
> `footer.html` vào template-part footer → launch site → set trang chủ tĩnh → nghiệm thu.

## 7. Giao diện mẫu tham khảo
Bám phong cách layout của:
- Mẫu 1: https://bissportvietnam.wordpress.com/
- Mẫu 2: https://decathlonvietnam.wordpress.com/
