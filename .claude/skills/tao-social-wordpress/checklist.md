# Checklist nghiệm thu — Tạo Social WordPress

Chỉ báo "HOÀN THÀNH" khi tất cả các mục dưới đây đạt ✅.

## A. Kết nối & bảo mật
- [ ] `python wp_client.py --test` trả về kết nối thành công.
- [ ] Thông tin đăng nhập chỉ nằm trong `.env` (không có trong code/commit).
- [ ] `.env` đã được liệt kê trong `.gitignore`.

## B. Cào dữ liệu website chính
- [ ] Lấy được `meta description`.
- [ ] Lấy được danh sách danh mục lớn.
- [ ] Mỗi danh mục lấy đúng 3 sản phẩm đầu tiên (tên + ảnh + link).
- [ ] Lấy được danh sách bài viết/blog mới nhất.
- [ ] Lấy được thông tin liên hệ (điện thoại, địa chỉ, email, website).
- [ ] Dữ liệu đã lưu ra `scraped-data.json`.

## C. Trang chủ (Homepage)
- [ ] Có banner placeholder.
- [ ] Có mô tả website.
- [ ] Khối sản phẩm: 3 sp/danh mục, ảnh tải được, link đúng về website chính.
- [ ] Khối bài viết hiển thị blog mới nhất.
- [ ] Footer khối 1: điện thoại, địa chỉ, website chính thức, email.
- [ ] Footer khối 2: bio ngắn + placeholder/link Facebook, TikTok, Pinterest, YouTube.

## D. Trang Giới thiệu
- [ ] Đã tạo page "Về Website Chính Thức" với placeholder nội dung.

## E. Bàn giao
- [ ] Trang tạo ở trạng thái `draft` (trừ khi user yêu cầu publish).
- [ ] Báo cáo dạng bảng: link các trang + danh sách placeholder user cần bổ sung.
