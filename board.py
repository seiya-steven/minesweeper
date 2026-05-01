# board.py
# Xử lý logic game: mảng 2D, đặt mìn, thuật toán Flood Fill, đếm số

import random
from settings import (
    GRID_ROWS, GRID_COLS, NUM_MINES,
    CELL_HIDDEN, CELL_REVEALED, CELL_FLAGGED,
    MINE_VALUE, STATE_PLAYING, STATE_WON, STATE_LOST
)


class Board:
    """
    Lớp quản lý bảng game Minesweeper.
    
    Attributes:
        rows (int): Số hàng
        cols (int): Số cột
        num_mines (int): Số mìn
        grid (list): Mảng 2D chứa giá trị ô (MINE_VALUE=-1 hoặc số 0-8)
        state_grid (list): Mảng 2D chứa trạng thái ô (HIDDEN/REVEALED/FLAGGED)
        game_state (str): Trạng thái hiện tại (playing/won/lost)
        flags_count (int): Số cờ đã cắm
        mines_placed (bool): Mìn đã được đặt chưa (đặt sau click đầu tiên)
        hit_mine (tuple): Tọa độ (row, col) của mìn bị nổ (nếu thua)
    """

    def __init__(self):
        """Khởi tạo bảng game mới."""
        self.rows = GRID_ROWS
        self.cols = GRID_COLS
        self.num_mines = NUM_MINES
        self.reset()

    def reset(self):
        """
        Reset toàn bộ bảng về trạng thái ban đầu.
        Mìn chưa được đặt - sẽ đặt sau lần click đầu tiên 
        để đảm bảo người chơi không bị nổ ngay.
        """
        # Mảng giá trị: 0 = trống, 1-8 = số mìn xung quanh, -1 = mìn
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        # Mảng trạng thái: HIDDEN / REVEALED / FLAGGED
        self.state_grid = [[CELL_HIDDEN for _ in range(self.cols)] for _ in range(self.rows)]
        
        self.game_state = STATE_PLAYING
        self.flags_count = 0
        self.mines_placed = False
        self.hit_mine = None  # Lưu vị trí mìn bị click (để tô đỏ)

    def place_mines(self, first_row, first_col):
        """
        Thuật toán đặt mìn ngẫu nhiên trên bảng.
        
        Đảm bảo ô đầu tiên người chơi click và 8 ô xung quanh nó
        sẽ KHÔNG chứa mìn (safe zone), giúp trải nghiệm tốt hơn.
        
        Args:
            first_row (int): Hàng của ô được click đầu tiên
            first_col (int): Cột của ô được click đầu tiên
        """
        # Tạo danh sách các ô "an toàn" (ô click đầu + 8 ô xung quanh)
        safe_cells = set()
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                r, c = first_row + dr, first_col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    safe_cells.add((r, c))

        # Tạo danh sách tất cả ô có thể đặt mìn (loại bỏ ô an toàn)
        candidates = [
            (r, c) for r in range(self.rows) for c in range(self.cols)
            if (r, c) not in safe_cells
        ]

        # Chọn ngẫu nhiên NUM_MINES ô để đặt mìn
        mine_positions = random.sample(candidates, min(self.num_mines, len(candidates)))

        # Đặt mìn vào mảng grid
        for r, c in mine_positions:
            self.grid[r][c] = MINE_VALUE

        # Tính số mìn xung quanh cho mỗi ô không phải mìn
        self._calculate_numbers()
        self.mines_placed = True

    def _calculate_numbers(self):
        """
        Tính giá trị số cho mỗi ô (đếm số mìn trong 8 ô lân cận).
        
        Duyệt qua toàn bộ bảng, với mỗi ô KHÔNG phải mìn,
        đếm số mìn trong 8 hướng xung quanh (trên, dưới, trái, phải, 4 góc).
        """
        for r in range(self.rows):
            for c in range(self.cols):
                # Bỏ qua ô mìn
                if self.grid[r][c] == MINE_VALUE:
                    continue
                
                # Đếm mìn trong 8 ô lân cận
                count = 0
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        if dr == 0 and dc == 0:
                            continue  # Bỏ qua chính nó
                        nr, nc = r + dr, c + dc
                        # Kiểm tra biên và đếm mìn
                        if (0 <= nr < self.rows and 0 <= nc < self.cols
                                and self.grid[nr][nc] == MINE_VALUE):
                            count += 1
                
                self.grid[r][c] = count

    def reveal_cell(self, row, col):
        """
        Mở một ô trên bảng (khi click chuột trái).
        
        Logic xử lý:
        1. Nếu chưa đặt mìn -> đặt mìn (lần click đầu tiên)
        2. Nếu ô đã mở hoặc cắm cờ -> bỏ qua
        3. Nếu trúng mìn -> THUA
        4. Nếu ô trống (giá trị 0) -> gọi Flood Fill
        5. Nếu ô có số -> chỉ mở ô đó
        
        Args:
            row (int): Hàng của ô cần mở
            col (int): Cột của ô cần mở
            
        Returns:
            bool: True nếu hành động hợp lệ, False nếu bị bỏ qua
        """
        # Chỉ xử lý khi game đang chơi
        if self.game_state != STATE_PLAYING:
            return False

        # Kiểm tra biên
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False

        # Không mở ô đã mở hoặc đang cắm cờ
        if self.state_grid[row][col] != CELL_HIDDEN:
            return False

        # Lần click đầu tiên -> đặt mìn
        if not self.mines_placed:
            self.place_mines(row, col)

        # TRÚNG MÌN -> THUA
        if self.grid[row][col] == MINE_VALUE:
            self.state_grid[row][col] = CELL_REVEALED
            self.hit_mine = (row, col)
            self.game_state = STATE_LOST
            self._reveal_all_mines()
            return True

        # MỞ Ô
        if self.grid[row][col] == 0:
            # Ô trống -> Flood Fill mở rộng
            self._flood_fill(row, col)
        else:
            # Ô có số -> chỉ mở ô này
            self.state_grid[row][col] = CELL_REVEALED

        # Kiểm tra điều kiện thắng
        self._check_win()
        return True

    def _flood_fill(self, row, col):
        """
        Thuật toán Flood Fill (BFS - Breadth First Search).
        
        Khi người chơi click vào ô trống (giá trị 0), tự động mở
        tất cả các ô trống liền kề và dừng lại ở các ô có số.
        
        Sử dụng hàng đợi (queue) để duyệt theo chiều rộng:
        1. Thêm ô ban đầu vào queue
        2. Lấy ô đầu queue, mở nó
        3. Nếu ô có giá trị 0 -> thêm 8 ô lân cận chưa mở vào queue
        4. Nếu ô có số -> mở nhưng không lan tiếp
        5. Lặp lại cho đến khi queue rỗng
        
        Args:
            row (int): Hàng bắt đầu Flood Fill
            col (int): Cột bắt đầu Flood Fill
        """
        # Hàng đợi BFS
        queue = [(row, col)]
        visited = set()
        visited.add((row, col))

        while queue:
            r, c = queue.pop(0)

            # Bỏ qua ô đã mở hoặc cắm cờ
            if self.state_grid[r][c] == CELL_REVEALED:
                continue

            # Mở ô hiện tại
            self.state_grid[r][c] = CELL_REVEALED

            # Nếu ô trống (0), mở rộng sang 8 ô lân cận
            if self.grid[r][c] == 0:
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        # Kiểm tra: trong biên, chưa thăm, chưa cắm cờ
                        if (0 <= nr < self.rows and 0 <= nc < self.cols
                                and (nr, nc) not in visited
                                and self.state_grid[nr][nc] != CELL_FLAGGED):
                            visited.add((nr, nc))
                            queue.append((nr, nc))

    def toggle_flag(self, row, col):
        """
        Cắm hoặc gỡ cờ trên ô (khi click chuột phải).
        
        Chỉ có thể cắm cờ trên ô chưa mở.
        Cờ dùng để đánh dấu vị trí nghi ngờ có mìn.
        
        Args:
            row (int): Hàng
            col (int): Cột
            
        Returns:
            bool: True nếu hành động hợp lệ
        """
        if self.game_state != STATE_PLAYING:
            return False

        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False

        current_state = self.state_grid[row][col]

        if current_state == CELL_HIDDEN:
            # Cắm cờ
            self.state_grid[row][col] = CELL_FLAGGED
            self.flags_count += 1
            return True
        elif current_state == CELL_FLAGGED:
            # Gỡ cờ
            self.state_grid[row][col] = CELL_HIDDEN
            self.flags_count -= 1
            return True

        return False

    def _reveal_all_mines(self):
        """
        Hiện tất cả mìn khi thua (trừ những ô đã cắm cờ đúng).
        Cũng đánh dấu cờ sai (cắm cờ nhưng không có mìn).
        """
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == MINE_VALUE:
                    # Mìn chưa bị cắm cờ -> hiện ra
                    if self.state_grid[r][c] != CELL_FLAGGED:
                        self.state_grid[r][c] = CELL_REVEALED

    def _check_win(self):
        """
        Kiểm tra điều kiện thắng.
        
        Người chơi thắng khi TẤT CẢ các ô không phải mìn
        đã được mở (REVEALED). Ô mìn có thể ở trạng thái 
        HIDDEN hoặc FLAGGED.
        """
        for r in range(self.rows):
            for c in range(self.cols):
                # Nếu còn ô an toàn chưa mở -> chưa thắng
                if (self.grid[r][c] != MINE_VALUE
                        and self.state_grid[r][c] != CELL_REVEALED):
                    return

        # Tất cả ô an toàn đã mở -> THẮNG!
        self.game_state = STATE_WON
        
        # Tự động cắm cờ lên tất cả mìn khi thắng
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == MINE_VALUE:
                    self.state_grid[r][c] = CELL_FLAGGED
        self.flags_count = self.num_mines

    def get_remaining_mines(self):
        """
        Trả về số mìn còn lại (= tổng mìn - số cờ đã cắm).
        Có thể âm nếu cắm cờ nhiều hơn số mìn.
        
        Returns:
            int: Số mìn còn lại hiển thị trên bộ đếm
        """
        return self.num_mines - self.flags_count

    def is_wrong_flag(self, row, col):
        """
        Kiểm tra ô có phải cờ sai không (cắm cờ nhưng không có mìn).
        Chỉ dùng khi hiển thị sau khi thua.
        
        Args:
            row (int): Hàng
            col (int): Cột
            
        Returns:
            bool: True nếu cờ sai
        """
        return (self.state_grid[row][col] == CELL_FLAGGED
                and self.grid[row][col] != MINE_VALUE)
