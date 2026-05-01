# main.py - Game loop chính cho Minesweeper
# Xử lý vòng lặp, sự kiện chuột, hover, quản lý thời gian

import sys
import pygame
from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    STATE_PLAYING, STATE_WON, STATE_LOST
)
from board import Board
from ui import init_fonts, draw_game, get_cell_from_mouse


def main():
    """Hàm chính khởi chạy game Minesweeper."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("💣 Minesweeper")
    clock = pygame.time.Clock()

    board = Board()
    fonts = init_fonts()

    # Quản lý thời gian
    start_time = None
    elapsed_time = 0
    timer_running = False

    # Quản lý nút Reset & hover
    smiley_pressed = False
    button_rect = None
    hover_cell = None  # Ô đang hover (row, col)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEMOTION:
                # Cập nhật ô hover
                hover_cell = get_cell_from_mouse(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if button_rect and button_rect.collidepoint(mouse_pos):
                    smiley_pressed = True

                elif event.button == 1:  # Click trái: mở ô
                    cell = get_cell_from_mouse(mouse_pos)
                    if cell and board.game_state == STATE_PLAYING:
                        row, col = cell
                        if not timer_running and not board.mines_placed:
                            start_time = pygame.time.get_ticks()
                            timer_running = True
                        board.reveal_cell(row, col)
                        if board.game_state in (STATE_WON, STATE_LOST):
                            timer_running = False

                elif event.button == 3:  # Click phải: cắm/gỡ cờ
                    cell = get_cell_from_mouse(mouse_pos)
                    if cell and board.game_state == STATE_PLAYING:
                        board.toggle_flag(cell[0], cell[1])

            elif event.type == pygame.MOUSEBUTTONUP:
                if smiley_pressed and event.button == 1:
                    smiley_pressed = False
                    if button_rect and button_rect.collidepoint(event.pos):
                        board.reset()
                        start_time = None
                        elapsed_time = 0
                        timer_running = False

        # Cập nhật đồng hồ
        if timer_running and start_time is not None:
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

        # Vẽ giao diện
        button_rect = draw_game(screen, fonts, board, elapsed_time,
                                smiley_pressed, hover_cell)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
