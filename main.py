from canvas import CanvasManager
from grid import Grid
from window import Window


def main():
    screen_size = 600
    canvas_size = 600
    grid_size = 300
    window = Window(screen_size, screen_size)
    window.redraw()
    canvas_manager = CanvasManager(window, canvas_size, canvas_size)
    canvas_manager.mount_canvas()
    grid = Grid(grid_size, grid_size, canvas_manager)
    window.wait_for_close()


if __name__ == '__main__':
    main()
