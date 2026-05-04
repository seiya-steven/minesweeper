# 💣 Minesweeper

Tựa game **Dò mìn (Minesweeper)** kinh điển, được viết bằng Python và Pygame với giao diện đồ họa hiện đại.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green?logo=pygame)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Tính năng

- 🎨 **Giao diện hiện đại** — Thiết kế blue-gray với bo góc, layered bevel 3D, hiệu ứng hover
- 😊 **Mặt cười biểu cảm** — 3 trạng thái: cười (đang chơi), kính mát (thắng), X_X (thua)
- 🚩 **Cắm cờ** — Click chuột phải để đánh dấu vị trí nghi ngờ có mìn
- ⏱️ **Đồng hồ & Bộ đếm LED** — Hiển thị thời gian chơi và số mìn còn lại
- 💥 **Flood Fill** — Tự động mở các ô trống liền kề khi click vào ô không có mìn xung quanh
- 🛡️ **Safe First Click** — Lần click đầu tiên luôn an toàn, không bao giờ trúng mìn

## 📁 Cấu trúc dự án

```
minesweeper/
├── main.py           # Game loop chính, xử lý sự kiện chuột
├── settings.py       # Cấu hình: kích thước lưới, màu sắc, hằng số
├── board.py          # Logic game: đặt mìn, Flood Fill, thắng/thua
├── ui.py             # Vẽ giao diện: ô, mìn, cờ, mặt cười, LED
├── requirements.txt  # Thư viện cần cài đặt
└── README.md
```

## 🚀 Cài đặt & Chạy game

### Yêu cầu hệ thống

- **Python** 3.8 trở lên
- Hệ điều hành: Windows, macOS, hoặc Linux

### Bước 1: Clone repository

```bash
git clone https://github.com/seiya-steven/minesweeper.git
cd minesweeper
```

### Bước 2: Tạo môi trường ảo

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### Bước 3: Cài đặt thư viện

```bash
# Window
python -m pip install -r requirements.txt

# macOS / Linux
pip install -r requirements.txt
```

### Bước 4: Chạy game

```bash
python main.py
```

## 🎮 Hướng dẫn chơi

| Thao tác | Hành động |
|---|---|
| **Click chuột trái** | Mở ô |
| **Click chuột phải** | Cắm / gỡ cờ 🚩 |
| **Click nút mặt cười** | Bắt đầu ván mới |

### Luật chơi

1. Bảng gồm **10×10 ô** với **10 quả mìn** ẩn bên dưới
2. Click vào ô để mở — số hiện ra cho biết có bao nhiêu mìn xung quanh (8 ô kề)
3. Nếu ô không có mìn xung quanh (số 0), các ô trống liền kề sẽ tự động mở
4. Click chuột phải để cắm cờ đánh dấu vị trí bạn nghĩ có mìn
5. **Thắng** khi mở hết tất cả ô an toàn 🎉
6. **Thua** khi click trúng mìn 💥

### Ý nghĩa màu số

| Số | Màu | Ý nghĩa |
|---|---|---|
| 1 | 🔵 Xanh dương | 1 mìn xung quanh |
| 2 | 🟢 Xanh lá | 2 mìn xung quanh |
| 3 | 🔴 Đỏ | 3 mìn xung quanh |
| 4 | 🔵 Xanh đậm | 4 mìn xung quanh |
| 5 | 🟤 Hồng đậm | 5 mìn xung quanh |
| 6 | 🟢 Xanh ngọc | 6 mìn xung quanh |
| 7 | ⚫ Đen | 7 mìn xung quanh |
| 8 | ⚪ Xám | 8 mìn xung quanh |

## ⚙️ Tùy chỉnh

Bạn có thể thay đổi cấu hình game trong file `settings.py`:

```python
GRID_COLS = 10    # Số cột
GRID_ROWS = 10    # Số hàng
NUM_MINES = 10    # Số mìn
CELL_SIZE = 36    # Kích thước ô (pixel)
```

## 📄 License

Dự án này được phát hành theo giấy phép [MIT](LICENSE).
