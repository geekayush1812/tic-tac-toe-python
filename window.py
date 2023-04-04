from tkinter import Tk


class Window:
    def __init__(self, height, width):
        self.__height = height
        self.__width = width
        self.__root = Tk()
        self.__root.title("Tic Tac Toe")
        self.__root.geometry(f"{self.__width}x{self.__height}")
        self.__root.resizable(False, False)
        self.__root.protocol("WM_DELETE_WINDOW", self.__on_close)

    def get_root(self):
        return self.__root

    def get_root_width(self):
        return self.__root.winfo_width()

    def get_root_height(self):
        return self.__root.winfo_height()

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__root.mainloop()

    def __on_close(self):
        self.__root.destroy()
