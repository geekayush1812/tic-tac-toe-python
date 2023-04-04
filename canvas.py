from tkinter import Canvas


class CanvasManager:
    def __init__(self, window, width, height):
        self.__window = window
        self.__width = width
        self.__height = height
        self.__canvas = None

    def mount_canvas(self, bg="white"):
        self.__canvas = Canvas(
            self.__window.get_root(), width=self.__width, height=self.__height, bg=bg,
        )
        self.__canvas.pack()
        self.__window.redraw()

    def get_canvas(self) -> Canvas:
        return self.__canvas

    def get_canvas_root(self):
        return self.__window.get_root()
