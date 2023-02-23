import csv
import cv2 as cv

import numpy as np
import pyglet
from my_window import MyWindow
from person import Person

frame_rate = 60.0


if __name__ == '__main__':
    # paste_pictures(4, 3, 48, 26, 40)
    # for pers in persons:
    #     print("===============")
    #     print(pers.surname)
    #     nb_ancestors, ancestor = pers.number_of_ancestors()
    #     print(nb_ancestors, str(ancestor.surname), str(ancestor.birth_name))
    #     print(pers.children)
    #     print(pers.mother)
    window = MyWindow(1080, 720, "Genealogy tree", resizable=True)
    pyglet.clock.schedule_interval(window.update, 1 / frame_rate)
    pyglet.app.run()
