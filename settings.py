# settings.py
# Chứa toàn bộ các biến cấu hình cho game Minesweeper
# Phong cách đồ họa hiện đại (Modern Blue-Gray Theme)

# ==============================
# CẤU HÌNH LƯỚI (GRID)
# ==============================
GRID_COLS = 10          # Số cột của lưới
GRID_ROWS = 10          # Số hàng của lưới
NUM_MINES = 10          # Số lượng mìn trên bảng

# ==============================
# CẤU HÌNH Ô VUÔNG (CELL)
# ==============================
CELL_SIZE = 36          # Kích thước mỗi ô vuông (pixel) - lớn hơn cho đồ họa đẹp
CELL_GAP = 2            # Khoảng cách giữa các ô (pixel)
CELL_RADIUS = 4         # Bo góc của ô (pixel)

# ==============================
# CẤU HÌNH HEADER
# ==============================
HEADER_HEIGHT = 60      # Chiều cao vùng header
HEADER_PADDING = 12     # Khoảng cách padding trong header
HEADER_RADIUS = 6       # Bo góc header

# ==============================
# CẤU HÌNH VIỀN NGOÀI
# ==============================
OUTER_PADDING = 16      # Padding ngoài cùng của cửa sổ
GRID_HEADER_GAP = 12    # Khoảng cách giữa header và lưới

# ==============================
# TÍNH TOÁN KÍCH THƯỚC
# ==============================
# Tổng kích thước lưới (bao gồm khoảng cách giữa ô)
GRID_PIXEL_WIDTH = GRID_COLS * CELL_SIZE + (GRID_COLS - 1) * CELL_GAP
GRID_PIXEL_HEIGHT = GRID_ROWS * CELL_SIZE + (GRID_ROWS - 1) * CELL_GAP

# Padding bên trong khung lưới và header
FRAME_PADDING = 8

# Chiều rộng cửa sổ
WINDOW_WIDTH = OUTER_PADDING * 2 + GRID_PIXEL_WIDTH + FRAME_PADDING * 2
# Chiều cao cửa sổ
WINDOW_HEIGHT = (OUTER_PADDING * 2 + HEADER_HEIGHT + FRAME_PADDING * 2
                 + GRID_HEADER_GAP + GRID_PIXEL_HEIGHT + FRAME_PADDING * 2)

# Tọa độ bắt đầu vẽ header (bên trong frame)
HEADER_FRAME_X = OUTER_PADDING
HEADER_FRAME_Y = OUTER_PADDING
HEADER_FRAME_W = WINDOW_WIDTH - OUTER_PADDING * 2
HEADER_FRAME_H = HEADER_HEIGHT + FRAME_PADDING * 2

HEADER_ORIGIN_X = HEADER_FRAME_X + FRAME_PADDING
HEADER_ORIGIN_Y = HEADER_FRAME_Y + FRAME_PADDING

# Tọa độ bắt đầu vẽ lưới (bên trong frame)
GRID_FRAME_X = OUTER_PADDING
GRID_FRAME_Y = HEADER_FRAME_Y + HEADER_FRAME_H + GRID_HEADER_GAP
GRID_FRAME_W = GRID_PIXEL_WIDTH + FRAME_PADDING * 2
GRID_FRAME_H = GRID_PIXEL_HEIGHT + FRAME_PADDING * 2

GRID_ORIGIN_X = GRID_FRAME_X + FRAME_PADDING
GRID_ORIGIN_Y = GRID_FRAME_Y + FRAME_PADDING

# Compat (cho main.py dùng)
GRID_WIDTH = GRID_PIXEL_WIDTH
GRID_HEIGHT = GRID_PIXEL_HEIGHT

# ==============================
# FPS (Frames Per Second)
# ==============================
FPS = 60    # 60 FPS cho animation mượt mà hơn

# ==============================
# BẢNG MÀU HIỆN ĐẠI (Modern Blue-Gray Theme)
# Lấy từ bộ asset SVG
# ==============================

# --- Nền chính ---
COLOR_BG = (0xE8, 0xEE, 0xF4)              # #E8EEF4 - Nền cửa sổ (xanh xám rất nhạt)
COLOR_WINDOW_BG = (0xD8, 0xE2, 0xEC)       # #D8E2EC - Nền bên trong cửa sổ

# --- Ô chưa mở (Cell/Closed) ---
COLOR_CELL_BG = (0xD8, 0xE2, 0xEC)         # #D8E2EC - Nền chính ô chưa mở
COLOR_CELL_BORDER = (0xBF, 0xC8, 0xD4)     # #BFC8D4 - Viền ngoài ô
COLOR_CELL_HIGHLIGHT = (0xEB, 0xF2, 0xFA)  # #EBF2FA - Highlight trên/trái (sáng)
COLOR_CELL_SHADOW = (0xA8, 0xB5, 0xC2)     # #A8B5C2 - Shadow dưới/phải (tối)

# --- Ô đã mở (Cell/Open) ---
COLOR_CELL_OPEN_BG = (0xC0, 0xCC, 0xDA)    # #C0CCDA - Nền ô đã mở
COLOR_CELL_OPEN_BORDER = (0x9B, 0xAA, 0xBA) # #9BAABA - Viền ô đã mở

# --- Ô hover ---
COLOR_CELL_HOVER_BG = (0xC5, 0xD4, 0xE3)   # #C5D4E3 - Nền hover
COLOR_CELL_HOVER_BORDER = (0xA8, 0xB5, 0xC2) # #A8B5C2
COLOR_CELL_HOVER_HL = (0xD8, 0xE6, 0xF3)   # #D8E6F3 - Highlight hover
COLOR_CELL_HOVER_SH = (0x88, 0x99, 0xAA)   # #8899AA - Shadow hover

# --- Ô mìn nổ (Cell/Mine-Hit) ---
COLOR_MINE_HIT_BG = (0xE0, 0x40, 0x40)     # #E04040 - Nền đỏ mìn nổ
COLOR_MINE_HIT_BORDER = (0xA0, 0x20, 0x20) # #A02020 - Viền đỏ đậm

# --- Mìn ---
COLOR_MINE_BODY = (0x1A, 0x1A, 0x1A)       # #1A1A1A - Thân mìn đen
COLOR_MINE_INNER = (0x22, 0x22, 0x22)       # #222222 - Trong mìn
COLOR_MINE_HIGHLIGHT = (0x55, 0x55, 0x55)   # #555555 - Highlight mìn

# --- LED Counter ---
COLOR_LED_OUTER = (0x1A, 0x1A, 0x1A)       # #1A1A1A - Viền ngoài LED
COLOR_LED_BG = (0x0D, 0x0D, 0x0D)          # #0D0D0D - Nền LED
COLOR_LED_TEXT = (0xFF, 0x22, 0x22)         # #FF2222 - Chữ LED đỏ

# --- Mặt cười (Face) ---
COLOR_FACE_YELLOW = (0xF5, 0xE6, 0x42)     # #F5E642 - Mặt vàng
COLOR_FACE_BORDER = (0xBF, 0xC8, 0xD4)     # #BFC8D4 - Viền ngoài mặt
COLOR_FACE_OUTLINE = (0x22, 0x22, 0x22)    # #222222 - Nét vẽ mắt, miệng
COLOR_FACE_GLASSES = (0x15, 0x65, 0xC0)    # #1565C0 - Kính mát (khi thắng)
COLOR_FACE_GLASSES_HL = (0x55, 0x99, 0xEE) # #5599EE - Highlight kính

# --- Cờ (Flag) ---
COLOR_FLAG_RED = (0xD3, 0x2F, 0x2F)        # #D32F2F - Lá cờ đỏ
COLOR_FLAG_RED_HL = (0xEF, 0x53, 0x50)     # #EF5350 - Highlight cờ
COLOR_FLAG_POLE = (0x5A, 0x38, 0x20)       # #5A3820 - Cán cờ nâu

# --- Dấu X sai cờ ---
COLOR_WRONG_X = (0xE0, 0x30, 0x30)         # #E03030 - Dấu X đỏ

# --- Header toolbar ---
COLOR_HEADER_BG = (0xD8, 0xE2, 0xEC)       # #D8E2EC - Nền header
COLOR_HEADER_BORDER = (0xBF, 0xC8, 0xD4)   # #BFC8D4 - Viền header

# --- Màu text chung ---
COLOR_TEXT_DARK = (0x11, 0x11, 0x11)        # #111111
COLOR_TEXT_LABEL = (0x88, 0x99, 0xAA)       # #8899AA

# ==============================
# MÀU SỐ TRÊN Ô ĐÃ MỞ (1-8)
# Material Design inspired - từ bộ asset SVG
# ==============================
NUMBER_COLORS = {
    1: (0x15, 0x65, 0xC0),   # #1565C0 - Xanh dương (Blue)
    2: (0x2E, 0x7D, 0x32),   # #2E7D32 - Xanh lá (Green)
    3: (0xC6, 0x28, 0x28),   # #C62828 - Đỏ (Red)
    4: (0x1A, 0x23, 0x7E),   # #1A237E - Xanh dương đậm (Dark Blue)
    5: (0x88, 0x0E, 0x4F),   # #880E4F - Hồng đậm (Dark Pink)
    6: (0x00, 0x69, 0x5C),   # #00695C - Xanh ngọc (Teal)
    7: (0x21, 0x21, 0x21),   # #212121 - Gần đen (Dark)
    8: (0x75, 0x75, 0x75),   # #757575 - Xám (Gray)
}

# ==============================
# TRẠNG THÁI GAME
# ==============================
STATE_PLAYING = "playing"
STATE_WON = "won"
STATE_LOST = "lost"

# ==============================
# TRẠNG THÁI Ô
# ==============================
CELL_HIDDEN = 0       # Ô chưa mở
CELL_REVEALED = 1     # Ô đã mở
CELL_FLAGGED = 2      # Ô đã cắm cờ

# Giá trị đặc biệt cho ô mìn
MINE_VALUE = -1
