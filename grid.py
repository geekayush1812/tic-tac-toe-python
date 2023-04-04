from canvas import CanvasManager
from tkinter import Button, Frame


margin = 15


class Grid:
    def __init__(self, width, height, canvas_manager: CanvasManager):
        self.width = width
        self.height = height
        self.__num_rows = 3
        self.__num_cols = 3
        self.__canvas_manager = canvas_manager
        canvas_manager.get_canvas().configure(cursor="hand1")
        self.cells = {}
        self.player_type = "X"
        self.cross_circle_rect_ids = []
        self.player_moves = {
            "X": 0b000000000,
            "O": 0b000000000
        }
        self.player_match_wins = {
            "X": 0,
            "O": 0
        }
        self.draws = 0
        self.has_winner = False
        self.current_match_winner = None
        self.cell_filled_count = 0
        self.__canvas_item_ids = {}
        self.create_grid()
        self.create_labels()
        self.attach_listeners()

    def create_grid(self):
        for row in range(self.__num_rows):
            for col in range(self.__num_cols):
                x1 = col * self.width / self.__num_cols
                y1 = row * self.height / self.__num_rows
                x2 = self.width / self.__num_cols + col * self.width / self.__num_cols
                y2 = self.height / self.__num_rows + row * self.height / self.__num_rows

                rect_id = self.__canvas_manager.get_canvas().create_rectangle(
                    x1, y1, x2, y2, fill="white", outline="black")

                self.cells[rect_id] = ""

    def update_grid(self):
        for rect_id in self.cross_circle_rect_ids:
            self.__canvas_manager.get_canvas().delete(rect_id)
        self.cross_circle_rect_ids = []

        for rect_id in self.cells:
            self.cells[rect_id] = ""

    def create_labels(self):
        self.__canvas_item_ids['player_type'] = self.create_label(
            f"Current Player: {self.player_type}", 400, 10, "red" if self.player_type == "X" else "blue")
        self.__canvas_item_ids['winner'] = self.create_label(
            f"Current Match Winner: {self.current_match_winner}", 400, 30)

        self.__canvas_item_ids['player_X_score'] = self.create_label(
            f"Player X Score: {self.player_match_wins['X']}", 400, 70)
        self.__canvas_item_ids['player_O_score'] = self.create_label(
            f"Player O Score: {self.player_match_wins['O']}", 400, 90)
        self.__canvas_item_ids['draws'] = self.create_label(
            f"Draws: {self.draws}", 400, 110)

    def update_labels(self):
        self.update_label(
            self.__canvas_item_ids['player_type'], f"Current Player: {self.player_type}", "red" if self.player_type == "X" else "blue")
        self.update_label(
            self.__canvas_item_ids[
                'winner'], f"Current Match Winner: {self.current_match_winner}",
            "green" if self.has_winner else "black"
        )
        self.update_label(
            self.__canvas_item_ids['player_X_score'], text=f"Player X Score: {self.player_match_wins['X']}")
        self.update_label(
            self.__canvas_item_ids['player_O_score'], text=f"Player O Score: {self.player_match_wins['O']}")
        self.update_label(
            self.__canvas_item_ids['draws'], text=f"Draws: {self.draws}")

    def create_label(self, text, x, y, color="black"):
        return self.__canvas_manager.get_canvas().create_text(x, y, anchor="nw", text=text, fill=color, font=("Arial", 12))

    def update_label(self, label, text, color="black"):
        self.__canvas_manager.get_canvas().itemconfig(label, text=text, fill=color)

    def attach_listeners(self):
        for rect_id in self.cells:
            self.__canvas_manager.get_canvas().tag_bind(rect_id, "<Button-1>", self.click)

    def click(self, event):
        if self.has_winner:
            return
        rect_id = event.widget.find_closest(event.x, event.y)[0]
        self.mark_current_cell(rect_id)

    def mark_current_cell(self, rect_id):
        if self.cells[rect_id] != "":
            return
        x1, y1, x2, y2 = self.__canvas_manager.get_canvas().coords(rect_id)
        if self.player_type == "X":
            self.draw_cross(
                x1 + margin, y1 + margin, x2 - margin, y2 - margin)
        else:
            self.draw_circle(x1 + margin, y1 + margin,
                             x2 - margin, y2 - margin)
        self.cells[rect_id] = self.player_type
        self.cell_filled_count += 1
        self.check_for_winner(rect_id)

    def check_for_winner(self, rect_id):
        # for the current cell -> get all the possible winning combinations in bits
        diagnal_bits = (0b100010001, 0b001010100)
        row_bits = (0b111000000, 0b000111000, 0b000000111)
        col_bits = (0b100100100, 0b010010010, 0b001001001)
        # check using bitwise operation if the current player has won

        # change that cell bit to 1 for the current player
        self.player_moves[self.player_type] |= (1 << (9 - rect_id))

        current_player_move = self.player_moves[self.player_type]

        for bits in diagnal_bits:
            if current_player_move & bits == bits:
                self.has_winner = True
        for bits in row_bits:
            if current_player_move & bits == bits:
                self.has_winner = True
        for bits in col_bits:
            if current_player_move & bits == bits:
                self.has_winner = True

        if self.has_winner:
            self.current_match_winner = self.player_type
            self.player_match_wins[self.player_type] += 1
            self.update_labels()
            self.show_popup()
            return

        self.check_draw()
        self.toggle_player_type()

    def toggle_player_type(self):
        if self.player_type == "X":
            self.player_type = "O"
        else:
            self.player_type = "X"

        self.update_labels()

    def check_draw(self):
        if self.cell_filled_count == 9:
            self.draws += 1
            self.update_labels()
            self.show_popup()
            return

    def draw_cross(self, x1, y1, x2, y2):
        line_one = self.__canvas_manager.get_canvas().create_line(
            x1, y1, x2, y2, fill="black", width=3)
        line_two = self.__canvas_manager.get_canvas().create_line(
            x1, y2, x2, y1, fill="black", width=3)
        self.cross_circle_rect_ids.append(line_one)
        self.cross_circle_rect_ids.append(line_two)

    def draw_circle(self, x1, y1, x2, y2):
        circle_id = self.__canvas_manager.get_canvas().create_oval(
            x1, y1, x2, y2, outline="black", width=3)
        self.cross_circle_rect_ids.append(circle_id)

    def show_popup(self):
        button_frame = Frame(
            self.__canvas_manager.get_canvas_root(), bg="black")
        reset_button = Button(
            button_frame, text="Reset Game", command=self.reset_game)
        restart_new_game_button = Button(
            button_frame, text="Restart New Game", command=self.restart_new_game)
        reset_button.pack()
        restart_new_game_button.pack()
        button_frame_window = self.__canvas_manager.get_canvas().create_window(450,
                                                                               180, window=button_frame)

    def reset_game(self):
        if self.current_match_winner == None:
            self.player_type = "X"
        else:
            self.player_type = self.current_match_winner
        self.current_match_winner = None
        self.has_winner = False
        self.cell_filled_count = 0
        self.draws = 0
        self.player_moves = {
            "X": 0,
            "O": 0
        }
        self.player_match_wins = {
            "X": 0,
            "O": 0
        }
        self.update_grid()
        self.update_labels()

    def restart_new_game(self):
        if self.current_match_winner == None:
            self.player_type = "X"
        else:
            self.player_type = self.current_match_winner
        self.current_match_winner = None
        self.has_winner = False
        self.cell_filled_count = 0
        self.player_moves = {
            "X": 0,
            "O": 0
        }
        self.update_grid()
        self.update_labels()
