import pyglet
from my_window import MyWindow

frame_rate = 60.0

if __name__ == '__main__':
    window = MyWindow(1080, 720, "Genealogy tree", resizable=True)
    pyglet.clock.schedule_interval(window.update, 1 / frame_rate)
    pyglet.app.run()
