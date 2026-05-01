# ui.py - Giao diện Minesweeper phong cách hiện đại (Modern Blue-Gray)
# Vẽ hoàn toàn bằng code, dựa trên bộ asset SVG

import pygame
import math
from settings import *


def init_fonts():
    """Khởi tạo font chữ."""
    return {
        'cell': pygame.font.SysFont('monospace', 20, bold=True),
        'counter': pygame.font.SysFont('monospace', 28, bold=True),
    }


# ==============================
# HÀM VẼ CƠ BẢN
# ==============================

def draw_rounded_rect(surface, color, rect, radius, width=0):
    """Vẽ hình chữ nhật bo góc."""
    pygame.draw.rect(surface, color, rect, width, border_radius=radius)


def _cell_xy(row, col):
    """Tính tọa độ pixel của ô (row, col) có tính gap."""
    x = GRID_ORIGIN_X + col * (CELL_SIZE + CELL_GAP)
    y = GRID_ORIGIN_Y + row * (CELL_SIZE + CELL_GAP)
    return x, y


# ==============================
# VẼ Ô (CELL)
# ==============================

def draw_cell_closed(surface, x, y, hover=False):
    """Vẽ ô chưa mở - layered bevel 3D với bo góc."""
    s = CELL_SIZE
    r = CELL_RADIUS

    if hover:
        bg, border, hl, sh = COLOR_CELL_HOVER_BG, COLOR_CELL_HOVER_BORDER, COLOR_CELL_HOVER_HL, COLOR_CELL_HOVER_SH
    else:
        bg, border, hl, sh = COLOR_CELL_BG, COLOR_CELL_BORDER, COLOR_CELL_HIGHLIGHT, COLOR_CELL_SHADOW

    # Lớp 1: Viền ngoài
    draw_rounded_rect(surface, border, (x, y, s, s), r)
    # Lớp 2: Nền chính (inset 2px)
    draw_rounded_rect(surface, bg, (x+2, y+2, s-4, s-4), r-1)
    # Lớp 3: Highlight trên (thanh sáng ngang)
    pygame.draw.rect(surface, hl, (x+2, y+2, s-6, 5), border_radius=2)
    # Lớp 4: Highlight trái (thanh sáng dọc)
    pygame.draw.rect(surface, hl, (x+2, y+2, 5, s-6), border_radius=2)
    # Lớp 5: Shadow dưới
    pygame.draw.rect(surface, sh, (x+2, y+s-6, s-4, 4), border_radius=2)
    # Lớp 6: Shadow phải
    pygame.draw.rect(surface, sh, (x+s-6, y+2, 4, s-4), border_radius=2)


def draw_cell_open(surface, x, y):
    """Vẽ ô đã mở - phẳng, tối hơn."""
    s = CELL_SIZE
    r = CELL_RADIUS
    draw_rounded_rect(surface, COLOR_CELL_OPEN_BORDER, (x, y, s, s), r)
    draw_rounded_rect(surface, COLOR_CELL_OPEN_BG, (x+1, y+1, s-2, s-2), r-1)


def draw_cell_number(surface, fonts, x, y, value):
    """Vẽ ô đã mở có số."""
    draw_cell_open(surface, x, y)
    if 1 <= value <= 8:
        color = NUMBER_COLORS.get(value, COLOR_TEXT_DARK)
        txt = fonts['cell'].render(str(value), True, color)
        surface.blit(txt, txt.get_rect(center=(x + CELL_SIZE//2, y + CELL_SIZE//2)))


# ==============================
# VẼ MÌN
# ==============================

def draw_mine_icon(surface, cx, cy, size):
    """Vẽ icon mìn tại tâm (cx, cy) với kích thước tương đối."""
    r = size  # bán kính thân mìn
    line_ext = int(r * 1.8)  # chiều dài đường gạch
    lw = max(2, size // 4)   # độ dày nét

    # 4 đường gạch chéo (hình ngôi sao)
    pygame.draw.line(surface, COLOR_MINE_BODY, (cx, cy - line_ext), (cx, cy + line_ext), lw)
    pygame.draw.line(surface, COLOR_MINE_BODY, (cx - line_ext, cy), (cx + line_ext, cy), lw)
    d = int(line_ext * 0.7)
    pygame.draw.line(surface, COLOR_MINE_BODY, (cx - d, cy - d), (cx + d, cy + d), lw)
    pygame.draw.line(surface, COLOR_MINE_BODY, (cx + d, cy - d), (cx - d, cy + d), lw)

    # Thân mìn (hình tròn)
    pygame.draw.circle(surface, COLOR_MINE_BODY, (cx, cy), r)
    pygame.draw.circle(surface, COLOR_MINE_INNER, (cx, cy), r - 1)

    # Highlight (bóng sáng trên mìn)
    hl_x = cx - r // 3
    hl_y = cy - r // 3
    pygame.draw.ellipse(surface, COLOR_MINE_HIGHLIGHT,
                        (hl_x - r//3, hl_y - r//4, r*2//3, r//2))


def draw_cell_mine(surface, x, y, is_hit=False):
    """Vẽ ô chứa mìn."""
    s = CELL_SIZE
    r = CELL_RADIUS

    if is_hit:
        draw_rounded_rect(surface, COLOR_MINE_HIT_BORDER, (x, y, s, s), r)
        draw_rounded_rect(surface, COLOR_MINE_HIT_BG, (x+1, y+1, s-2, s-2), r-1)
    else:
        draw_cell_open(surface, x, y)

    draw_mine_icon(surface, x + s//2, y + s//2, s//4)


# ==============================
# VẼ CỜ
# ==============================

def draw_cell_flag(surface, x, y):
    """Vẽ ô cắm cờ - nền nổi + cờ tam giác đỏ + cán nâu."""
    draw_cell_closed(surface, x, y)
    s = CELL_SIZE
    cx = x + s // 2 - 2
    cy = y + s // 2

    # Cán cờ (nâu)
    pole_top = cy - s//3
    pole_bot = cy + s//3
    pygame.draw.line(surface, COLOR_FLAG_POLE, (cx, pole_top), (cx, pole_bot), 3)

    # Đế cờ
    base_w = s // 3
    pygame.draw.rect(surface, COLOR_FLAG_POLE,
                     (cx - base_w//2, pole_bot - 2, base_w, 4), border_radius=2)

    # Lá cờ tam giác đỏ
    flag_h = s // 3
    flag_w = int(flag_h * 1.1)
    pts = [(cx, pole_top), (cx, pole_top + flag_h), (cx + flag_w, pole_top + flag_h//2)]
    pygame.draw.polygon(surface, COLOR_FLAG_RED, pts)

    # Highlight trên cờ
    hl_pts = [(cx, pole_top), (cx + flag_w//2, pole_top + flag_h//4), (cx, pole_top + flag_h//2)]
    hl_surf = pygame.Surface((s, s), pygame.SRCALPHA)
    pygame.draw.polygon(hl_surf, (*COLOR_FLAG_RED_HL, 128), 
                        [(p[0]-x, p[1]-y) for p in hl_pts])
    surface.blit(hl_surf, (x, y))


def draw_cell_wrong_flag(surface, x, y):
    """Vẽ cờ sai - cờ mờ + dấu X đỏ."""
    s = CELL_SIZE
    r = CELL_RADIUS
    draw_cell_open(surface, x, y)

    # Cờ mờ
    cx = x + s//2 - 2
    cy = y + s//2
    pole_top = cy - s//3
    pole_bot = cy + s//3

    alpha_surf = pygame.Surface((s, s), pygame.SRCALPHA)
    # Cán mờ
    pygame.draw.line(alpha_surf, (*COLOR_FLAG_POLE, 100),
                     (s//2-2, s//2 - s//3), (s//2-2, s//2 + s//3), 2)
    # Cờ mờ
    flag_h = s//3
    flag_w = int(flag_h * 1.1)
    fpts = [(s//2-2, s//2-s//3), (s//2-2, s//2-s//3+flag_h), (s//2-2+flag_w, s//2-s//3+flag_h//2)]
    pygame.draw.polygon(alpha_surf, (*COLOR_FLAG_RED, 90), fpts)
    surface.blit(alpha_surf, (x, y))

    # Dấu X đỏ to
    m = 6
    pygame.draw.line(surface, COLOR_WRONG_X, (x+m, y+m), (x+s-m, y+s-m), 4)
    pygame.draw.line(surface, COLOR_WRONG_X, (x+s-m, y+m), (x+m, y+s-m), 4)


# ==============================
# VẼ MẶT CƯỜI (FACE BUTTON)
# ==============================

def draw_face_button(surface, game_state, rect, pressed=False):
    """Vẽ nút reset mặt cười - hình tròn vàng lớn với biểu cảm."""
    x, y, w, h = rect
    cx = x + w // 2
    cy = y + h // 2
    outer_r = min(w, h) // 2 - 2
    inner_r = outer_r - 2

    offset = 1 if pressed else 0
    cx += offset
    cy += offset

    # Viền ngoài xám
    pygame.draw.circle(surface, COLOR_FACE_BORDER, (cx, cy), outer_r)
    # Mặt vàng
    pygame.draw.circle(surface, COLOR_FACE_YELLOW, (cx, cy), inner_r)

    # Scale các chi tiết theo kích thước
    sc = inner_r / 26.0  # 26 = bán kính chuẩn trong SVG

    if game_state == STATE_WON:
        _draw_face_win(surface, cx, cy, sc)
    elif game_state == STATE_LOST:
        _draw_face_dead(surface, cx, cy, sc)
    else:
        _draw_face_normal(surface, cx, cy, sc)


def _draw_face_normal(surface, cx, cy, sc):
    """Mặt cười bình thường: 2 mắt tròn + miệng cong."""
    eye_r = max(2, int(4.5 * sc))
    hl_r = max(1, int(1.8 * sc))

    # Mắt trái
    ex1 = cx - int(10 * sc)
    ey = cy - int(6 * sc)
    pygame.draw.circle(surface, COLOR_FACE_OUTLINE, (ex1, ey), eye_r)
    pygame.draw.circle(surface, (255,255,255), (ex1 + 1, ey - 1), hl_r)

    # Mắt phải
    ex2 = cx + int(10 * sc)
    pygame.draw.circle(surface, COLOR_FACE_OUTLINE, (ex2, ey), eye_r)
    pygame.draw.circle(surface, (255,255,255), (ex2 + 1, ey - 1), hl_r)

    # Miệng cười (vẽ bằng arc)
    mouth_w = int(24 * sc)
    mouth_h = int(12 * sc)
    mouth_y = cy + int(2 * sc)
    arc_rect = (cx - mouth_w//2, mouth_y, mouth_w, mouth_h)
    lw = max(2, int(3 * sc))
    pygame.draw.arc(surface, COLOR_FACE_OUTLINE, arc_rect, math.pi + 0.3, 2*math.pi - 0.3, lw)


def _draw_face_dead(surface, cx, cy, sc):
    """Mặt chết: mắt X + miệng mếu."""
    lw = max(2, int(3 * sc))
    eye_sz = int(5 * sc)

    # Mắt X trái
    elx = cx - int(11 * sc)
    ely = cy - int(7 * sc)
    pygame.draw.line(surface, COLOR_FACE_OUTLINE,
                     (elx - eye_sz, ely - eye_sz), (elx + eye_sz, ely + eye_sz), lw)
    pygame.draw.line(surface, COLOR_FACE_OUTLINE,
                     (elx + eye_sz, ely - eye_sz), (elx - eye_sz, ely + eye_sz), lw)

    # Mắt X phải
    erx = cx + int(11 * sc)
    pygame.draw.line(surface, COLOR_FACE_OUTLINE,
                     (erx - eye_sz, ely - eye_sz), (erx + eye_sz, ely + eye_sz), lw)
    pygame.draw.line(surface, COLOR_FACE_OUTLINE,
                     (erx + eye_sz, ely - eye_sz), (erx - eye_sz, ely + eye_sz), lw)

    # Miệng mếu (vòng cung ngược)
    mouth_w = int(24 * sc)
    mouth_h = int(10 * sc)
    mouth_y = cy + int(5 * sc)
    pygame.draw.arc(surface, COLOR_FACE_OUTLINE,
                    (cx - mouth_w//2, mouth_y, mouth_w, mouth_h), 0.3, math.pi - 0.3, lw)


def _draw_face_win(surface, cx, cy, sc):
    """Mặt cool: kính mát xanh + miệng cười rộng."""
    lw = max(2, int(3 * sc))
    gl_w = int(14 * sc)
    gl_h = int(10 * sc)
    gl_r = max(2, int(4 * sc))

    # Kính trái
    gl_x1 = cx - int(18 * sc)
    gl_y = cy - int(10 * sc)
    pygame.draw.rect(surface, COLOR_FACE_GLASSES,
                     (gl_x1, gl_y, gl_w, gl_h), border_radius=gl_r)

    # Kính phải
    gl_x2 = cx + int(4 * sc)
    pygame.draw.rect(surface, COLOR_FACE_GLASSES,
                     (gl_x2, gl_y, gl_w, gl_h), border_radius=gl_r)

    # Gọng kính giữa
    bridge_lw = max(1, int(2.5 * sc))
    pygame.draw.line(surface, COLOR_FACE_GLASSES,
                     (gl_x1 + gl_w, gl_y + gl_h//2),
                     (gl_x2, gl_y + gl_h//2), bridge_lw)

    # Gọng hai bên
    pygame.draw.line(surface, (0x33,0x33,0x33),
                     (gl_x1 - int(4*sc), gl_y + gl_h//2),
                     (gl_x1, gl_y + gl_h//2), bridge_lw)
    pygame.draw.line(surface, (0x33,0x33,0x33),
                     (gl_x2 + gl_w, gl_y + gl_h//2),
                     (gl_x2 + gl_w + int(4*sc), gl_y + gl_h//2), bridge_lw)

    # Highlight kính trái
    hl_w = int(6 * sc)
    hl_h = int(4 * sc)
    hl_surf = pygame.Surface((hl_w, hl_h), pygame.SRCALPHA)
    pygame.draw.rect(hl_surf, (*COLOR_FACE_GLASSES_HL, 128),
                     (0, 0, hl_w, hl_h), border_radius=max(1, int(1.5*sc)))
    surface.blit(hl_surf, (gl_x1 + 1, gl_y + 1))

    # Miệng cười rộng
    mouth_w = int(28 * sc)
    mouth_h = int(14 * sc)
    mouth_y = cy + int(4 * sc)
    pygame.draw.arc(surface, COLOR_FACE_OUTLINE,
                    (cx - mouth_w//2, mouth_y, mouth_w, mouth_h),
                    math.pi + 0.2, 2*math.pi - 0.2, lw)


# ==============================
# VẼ LED COUNTER
# ==============================

def draw_led_counter(surface, fonts, value, x, y, w=90, h=42):
    """Vẽ bộ đếm LED - nền đen bo góc, chữ đỏ."""
    draw_rounded_rect(surface, COLOR_LED_OUTER, (x, y, w, h), 5)
    draw_rounded_rect(surface, COLOR_LED_BG, (x+3, y+3, w-6, h-6), 3)

    display_val = max(-99, min(999, value))
    text_str = f"{display_val:03d}"
    txt = fonts['counter'].render(text_str, True, COLOR_LED_TEXT)
    surface.blit(txt, txt.get_rect(center=(x + w//2, y + h//2)))


# ==============================
# VẼ HEADER
# ==============================

def draw_header(surface, fonts, board, elapsed_time, smiley_pressed=False):
    """Vẽ header: LED counter + Face button + Timer."""
    # Khung header bo góc
    draw_rounded_rect(surface, COLOR_HEADER_BORDER,
                      (HEADER_FRAME_X, HEADER_FRAME_Y, HEADER_FRAME_W, HEADER_FRAME_H),
                      HEADER_RADIUS)
    draw_rounded_rect(surface, COLOR_HEADER_BG,
                      (HEADER_FRAME_X+2, HEADER_FRAME_Y+2, HEADER_FRAME_W-4, HEADER_FRAME_H-4),
                      HEADER_RADIUS - 1)

    hx = HEADER_ORIGIN_X
    hy = HEADER_ORIGIN_Y
    hw = HEADER_FRAME_W - FRAME_PADDING * 2

    # LED đếm mìn (trái)
    led_w, led_h = 90, 42
    led_y = hy + (HEADER_HEIGHT - led_h) // 2
    draw_led_counter(surface, fonts, board.get_remaining_mines(), hx, led_y, led_w, led_h)

    # LED timer (phải)
    timer_val = min(999, elapsed_time)
    draw_led_counter(surface, fonts, timer_val, hx + hw - led_w, led_y, led_w, led_h)

    # Nút mặt cười (giữa)
    btn_size = 48
    btn_x = hx + (hw - btn_size) // 2
    btn_y = hy + (HEADER_HEIGHT - btn_size) // 2
    button_rect = pygame.Rect(btn_x, btn_y, btn_size, btn_size)

    draw_face_button(surface, board.game_state, button_rect, smiley_pressed)

    return button_rect


# ==============================
# VẼ BẢNG LƯỚI
# ==============================

def draw_board(surface, fonts, board, hover_cell=None):
    """Vẽ toàn bộ lưới game."""
    for row in range(board.rows):
        for col in range(board.cols):
            x, y = _cell_xy(row, col)
            state = board.state_grid[row][col]
            value = board.grid[row][col]

            if state == CELL_HIDDEN:
                is_hover = (hover_cell == (row, col) and board.game_state == STATE_PLAYING)
                draw_cell_closed(surface, x, y, hover=is_hover)

            elif state == CELL_FLAGGED:
                if board.game_state == STATE_LOST and board.is_wrong_flag(row, col):
                    draw_cell_wrong_flag(surface, x, y)
                else:
                    draw_cell_flag(surface, x, y)

            elif state == CELL_REVEALED:
                if value == MINE_VALUE:
                    is_hit = board.hit_mine == (row, col)
                    draw_cell_mine(surface, x, y, is_hit=is_hit)
                else:
                    draw_cell_number(surface, fonts, x, y, value)


# ==============================
# VẼ TOÀN BỘ GAME
# ==============================

def draw_game(surface, fonts, board, elapsed_time, smiley_pressed=False, hover_cell=None):
    """Hàm tổng hợp vẽ toàn bộ giao diện game."""
    # 1. Nền cửa sổ
    surface.fill(COLOR_BG)

    # 2. Khung lưới bo góc
    draw_rounded_rect(surface, COLOR_HEADER_BORDER,
                      (GRID_FRAME_X, GRID_FRAME_Y, GRID_FRAME_W, GRID_FRAME_H),
                      HEADER_RADIUS)
    draw_rounded_rect(surface, COLOR_WINDOW_BG,
                      (GRID_FRAME_X+2, GRID_FRAME_Y+2, GRID_FRAME_W-4, GRID_FRAME_H-4),
                      HEADER_RADIUS - 1)

    # 3. Header
    button_rect = draw_header(surface, fonts, board, elapsed_time, smiley_pressed)

    # 4. Lưới game
    draw_board(surface, fonts, board, hover_cell)

    return button_rect


# ==============================
# TIỆN ÍCH
# ==============================

def get_cell_from_mouse(mouse_pos):
    """Chuyển tọa độ chuột sang (row, col), trả về None nếu ngoài lưới."""
    mx, my = mouse_pos
    if not (GRID_ORIGIN_X <= mx < GRID_ORIGIN_X + GRID_PIXEL_WIDTH
            and GRID_ORIGIN_Y <= my < GRID_ORIGIN_Y + GRID_PIXEL_HEIGHT):
        return None

    # Tính col/row có tính gap
    rel_x = mx - GRID_ORIGIN_X
    rel_y = my - GRID_ORIGIN_Y
    col = rel_x // (CELL_SIZE + CELL_GAP)
    row = rel_y // (CELL_SIZE + CELL_GAP)

    # Kiểm tra click vào gap (khoảng trống giữa ô)
    if rel_x % (CELL_SIZE + CELL_GAP) >= CELL_SIZE:
        return None
    if rel_y % (CELL_SIZE + CELL_GAP) >= CELL_SIZE:
        return None

    if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS:
        return (row, col)
    return None
