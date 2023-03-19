import math
import pandas as pd
import pyglet
import csv
import cv2 as cv
import numpy as np
from pyglet.window import key
from person import Person
from sub_tree import SubTree
from centuries_line import CenturiesLine


def fill_blanks():
    df = pd.read_csv("data/family.csv")
    max_idx = max(df["id"])
    missing_values = []
    for i in range(max_idx + 1):
        if i not in df["id"].values:
            missing_values.append(i)
    missing_values = missing_values[::-1]
    for i in missing_values:
        df.loc[df["id"] > i, ["id"]] -= 1
        df.loc[df["mother_id"] > i, ["mother_id"]] -= 1
        df.loc[df["father_id"] > i, ["father_id"]] -= 1
    df.to_csv("data/family.csv", index=False)


def load():
    p = []
    with open("data/family.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        next(csv_reader, None)
        for line in csv_reader:
            p.append(Person(line[0], line[1], line[2], line[3], line[4], line[5],
                            line[6], line[7], line[8], None, None, line[9],
                            line[10], line[11], line[12]))
    for person in p:
        if person.mother_id != "-":
            for mother in p:
                if str(mother.person_id) == person.mother_id:
                    person.mother = mother
                    break
        if person.father_id != "-":
            for father in p:
                if str(father.person_id) == person.father_id:
                    person.father = father
                    break
    csv_file.close()

    max_generation = 0
    for person in p:
        if person.generation > max_generation:
            max_generation = person.generation
    root = p[0]
    return p, max_generation, root


# def get_offset(generation, max_generation):
#     if generation > 0:
#         return get_offset(generation - 1, max_generation) + math.pow(2, max_generation - generation - 1)
#     else:
#         return 0


def draw_tree(tree, size, downloading, on_screen_x, on_screen_y):
    if downloading:
        if -tree.width < tree.x_pos < on_screen_x + tree.width and -6 < tree.y_pos < on_screen_y + 6:
            tree.show(size)
        if tree.mother_tree is not None:
            draw_tree(tree.mother_tree, size, downloading, on_screen_x, on_screen_y)
        if tree.father_tree is not None:
            draw_tree(tree.father_tree, size, downloading, on_screen_x, on_screen_y)
    else:
        if 0 < tree.x_pos < on_screen_x and 0 < tree.y_pos < on_screen_y:
            tree.show(size)
        if tree.mother_tree is not None:
            draw_tree(tree.mother_tree, size, downloading, on_screen_x, on_screen_y)
        if tree.father_tree is not None:
            draw_tree(tree.father_tree, size, downloading, on_screen_x, on_screen_y)


def update_tree_pos(tree, x_change, y_change):
    tree.x_pos += x_change
    tree.y_pos += y_change
    if tree.mother_tree is not None:
        update_tree_pos(tree.mother_tree, x_change, y_change)
    if tree.father_tree is not None:
        update_tree_pos(tree.father_tree, x_change, y_change)


def grow_tree(person, x_pos, max_generation, dictionary):
    return SubTree(person,
                   person.mother,
                   person.father,
                   x_pos,
                   2 * person.generation + 1,
                   0,
                   max_generation,
                   dictionary)


def get_number_of_upper_generation(tree):
    if tree.mother_tree is not None:
        mother_gen = get_number_of_upper_generation(tree.mother_tree) + 1
    else:
        mother_gen = 0
    if tree.father_tree is not None:
        father_gen = get_number_of_upper_generation(tree.father_tree) + 1
    else:
        father_gen = 0
    return max(mother_gen, father_gen)


def set_x_pos_sub_trees(tree, threshold, offset):
    if tree.x_pos > threshold:
        tree.x_pos -= offset
    if tree.mother_tree is not None:
        set_x_pos_sub_trees(tree.mother_tree, threshold, offset)
    if tree.father_tree is not None:
        set_x_pos_sub_trees(tree.father_tree, threshold, offset)


def remove_empty_spaces(tree, positions):
    index = len(positions) - 1
    while index > 0:
        index -= 1
        offset = abs(positions[index] - positions[index + 1]) - 1
        if offset > 0:
            set_x_pos_sub_trees(tree, positions[index], offset)


# def split_list(list_x_pos):
#     positive, negative = [], []
#     for elem in list_x_pos:
#         if elem > 0:
#             positive.append(elem)
#         elif elem < 0:
#             negative.append(elem)
#         else:
#             positive.append(elem)
#             negative.append(elem)
#     return positive, negative


def get_tree_positions(tree, positions):
    positions.append(tree.x_pos)
    if tree.mother_tree is not None:
        get_tree_positions(tree.mother_tree, positions)
    if tree.father_tree is not None:
        get_tree_positions(tree.father_tree, positions)
    return positions


def get_borders(tree):
    if tree.mother_tree is not None and tree.father_tree is not None:
        x_mother_min, y_mother_min, x_mother_max, y_mother_max = get_borders(tree.mother_tree)
        x_father_min, y_father_min, x_father_max, y_father_max = get_borders(tree.father_tree)
        return min(x_mother_min, x_father_min, tree.x_pos), \
            min(y_mother_min, y_father_min, tree.y_pos), \
            max(x_mother_max, x_father_max, tree.x_pos), \
            max(y_mother_max, y_father_max, tree.y_pos)
    if tree.mother_tree is not None:
        x_mother_min, y_mother_min, x_mother_max, y_mother_max = get_borders(tree.mother_tree)
        return min(x_mother_min, tree.x_pos), \
            min(y_mother_min, tree.y_pos), \
            max(x_mother_max, tree.x_pos), \
            max(y_mother_max, tree.y_pos)
    if tree.father_tree is not None:
        x_father_min, y_father_min, x_father_max, y_father_max = get_borders(tree.father_tree)
        return min(x_father_min, tree.x_pos), \
            min(y_father_min, tree.y_pos), \
            max(x_father_max, tree.x_pos), \
            max(y_father_max, tree.y_pos)
    return tree.x_pos, tree.y_pos, tree.x_pos, tree.y_pos


def paste_pictures(x_span, y_span, width, height, size):
    new_width = size * int(width / size)
    new_height = size * int(height / size)
    images = []
    for i in range(x_span * y_span):
        images.append(
            cv.imread("data/image_parts/" + str(i) + ".png")[0:new_height, 0:new_width])
    tmp = []
    for i in range(y_span):
        tmp.append(np.concatenate((images[(i * x_span):(i * x_span + x_span)]), axis=1))
    tmp = np.flip(np.array(tmp), axis=0)
    res = np.concatenate(tmp[0:y_span], axis=0)
    cv.imwrite("res.png", res)


def initialization(tree):
    x_positions = get_tree_positions(tree, [])
    update_tree_pos(tree, -min(x_positions), 0)
    x_positions = get_tree_positions(tree, [])
    x_positions.sort()
    remove_empty_spaces(tree, x_positions)


class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fill_blanks()
        self.set_minimum_size(400, 300)
        self.background = pyglet.shapes.Rectangle(0, 0, 3000, 1200, [255, 255, 255])
        self.persons, self.max_generation, self.root = load()
        self.centuries_line = CenturiesLine(self.persons, self.max_generation)
        self.width, self.height = self.get_framebuffer_size()
        self.last_size = (self.width, self.height)
        self.person_size = 29
        self.tree = grow_tree(self.root, 0, self.max_generation, {})
        initialization(self.tree)
        x_pos = int(self.width / self.person_size / 2) - self.tree.x_pos
        update_tree_pos(self.tree, x_pos, 0)

        self.scroll_up = False
        self.scroll_down = False
        self.scroll_right = False
        self.scroll_left = False
        self.need_update = False
        self.downloading = False
        self.merging = False
        self.merge_1 = None
        self.merge_2 = None
        self.downloading_i = 0
        self.downloading_j = 0
        self.downloading_x = 1
        self.downloading_y = 1
        self.on_screen_x = int(self.width / self.person_size)
        self.on_screen_y = int(self.height / self.person_size)
        self.time_to_wait = 4
        self.time_remaining = self.time_to_wait - 1

    def on_draw(self):
        self.background.draw()
        if self.downloading and self.downloading_i < self.downloading_x:
            self.centuries_line.show(self.person_size, self.width, False)
        else:
            self.centuries_line.show(self.person_size, self.width, True)
        draw_tree(self.tree, self.person_size, self.downloading, self.on_screen_x, self.on_screen_y)

    def update(self, dt):
        self.check_size()
        self.scrolling()
        self.updating()
        if self.downloading:
            self.downloading_process()
        if self.merging and self.merge_1 is not None and self.merge_2 is not None:
            self.merge()

    def on_key_press(self, symbol, modifiers):
        if not self.downloading:
            if symbol == key.M:
                self.merging = True
            if symbol == key.S:
                self.person_size = 40
                self.on_screen_x = int(self.width / self.person_size)
                self.on_screen_y = int(self.height / self.person_size)
                print(self.on_screen_x, self.on_screen_y)
                x_min, y_min, x_max, y_max = get_borders(self.tree)
                update_tree_pos(self.tree, -x_min + 1, -y_min + 2)
                self.centuries_line.update(-y_min + 1)
                self.downloading_x = int((x_max - x_min) / self.on_screen_x)
                self.downloading_y = int((y_max - y_min) / self.on_screen_y)
                self.downloading = True
            if symbol == key.Q:
                update_tree_pos(self.tree, self.on_screen_x, 0)
            elif symbol == key.D:
                update_tree_pos(self.tree, -self.on_screen_x, 0)
            if symbol == key.UP:
                self.scroll_up = True
            elif symbol == key.DOWN:
                self.scroll_down = True
            if symbol == key.RIGHT:
                self.scroll_right = True
            elif symbol == key.LEFT:
                self.scroll_left = True

    def on_key_release(self, symbol, modifiers):
        if not self.downloading:
            if symbol == key.UP:
                self.scroll_up = False
            elif symbol == key.DOWN:
                self.scroll_down = False
            if symbol == key.RIGHT:
                self.scroll_right = False
            elif symbol == key.LEFT:
                self.scroll_left = False

    def on_mouse_press(self, x, y, button, modifiers):
        if self.merging:
            if self.merge_1 is None:
                self.merge_1 = self.check_person(self.tree, x, y)
            elif self.merge_2 is None:
                self.merge_2 = self.check_person(self.tree, x, y)
        elif not self.downloading:
            self.get_person(self.tree, x, y)

    def check_person(self, tree, x, y):
        if tree.x_pos * self.person_size < x < (tree.x_pos + 1) * self.person_size and \
                tree.y_pos * self.person_size < y < (tree.y_pos + 1) * self.person_size:
            return tree.person
        elif tree.mother_tree is not None and tree.father_tree is not None:
            if self.check_person(tree.mother_tree, x, y) is not None:
                return self.check_person(tree.mother_tree, x, y)
            if self.check_person(tree.father_tree, x, y) is not None:
                return self.check_person(tree.father_tree, x, y)
        elif tree.mother_tree is not None:
            if self.check_person(tree.mother_tree, x, y) is not None:
                return self.check_person(tree.mother_tree, x, y)
        elif tree.father_tree is not None:
            if self.check_person(tree.father_tree, x, y) is not None:
                return self.check_person(tree.father_tree, x, y)
        return None

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if not self.downloading:
            if self.person_size + scroll_y > 0:
                self.person_size += scroll_y
                self.on_screen_x = int(self.width / self.person_size)
                self.on_screen_y = int(self.height / self.person_size)

    def get_person(self, tree, x, y):
        if tree.x_pos * self.person_size < x < (tree.x_pos + 1) * self.person_size and \
                tree.y_pos * self.person_size < y < (tree.y_pos + 1) * self.person_size:
            self.minimize()
            print(tree.x_pos)
            print(tree.person)

            action = ""
            while action not in ["m", "f", "e", "mo"]:
                action = input("add a (f)ather, a (m)other or (mo)dify the current person or (e)xit : ")
            if action == "m":
                if tree.mother_tree is None:
                    df = pd.read_csv("data/family.csv")
                    mother_id = max(df["id"]) + 1
                    surname = input("Enter surname : ")
                    birth_name = input("Enter birth name : ")
                    birth = input("Enter birth date DD-MM-YYYY or - : ")
                    wedding = input("Enter wedding date DD-MM-YYYY or - : ")
                    death = input("Enter death date DD-MM-YYYY or - : ")
                    birth_city = input("Enter birth city or - : ")
                    wedding_city = input("Enter wedding city or - : ")
                    death_city = input("Enter death city or - : ")
                    generation = tree.person.generation + 1
                    new_row = pd.DataFrame({"id": mother_id,
                                            "surname": surname,
                                            "birth_name": birth_name,
                                            "genre": "F",
                                            "birth": birth,
                                            "death": death,
                                            "wedding_date": wedding,
                                            "father_id": -1,
                                            "mother_id": -1,
                                            "generation": generation,
                                            "birth_city": birth_city,
                                            "wedding_city": wedding_city,
                                            "death_city": death_city,
                                            "notes": ""}, index=[0])
                    df = pd.concat([df.loc[:], new_row]).reset_index(drop=True)
                    df.loc[df["id"] == tree.person.person_id, ["mother_id"]] = mother_id
                    df.to_csv("data/family.csv", index=False)
                    self.need_update = True
                else:
                    print("Already have a mother")
            elif action == "f":
                if tree.father_tree is None:
                    df = pd.read_csv("data/family.csv")
                    father_id = max(df["id"]) + 1
                    surname = input("Enter surname : ")
                    birth_name = input("Enter birth name : ")
                    birth = input("Enter birth date DD-MM-YYYY or - : ")
                    wedding = input("Enter wedding date DD-MM-YYYY or - : ")
                    death = input("Enter death date DD-MM-YYYY or - : ")
                    birth_city = input("Enter birth city or - : ")
                    wedding_city = input("Enter wedding city or - : ")
                    death_city = input("Enter death city or - : ")
                    generation = tree.person.generation + 1
                    new_row = pd.DataFrame({"id": father_id,
                                            "surname": surname,
                                            "birth_name": birth_name,
                                            "genre": "M",
                                            "birth": birth,
                                            "death": death,
                                            "wedding_date": wedding,
                                            "father_id": -1,
                                            "mother_id": -1,
                                            "generation": generation,
                                            "birth_city": birth_city,
                                            "wedding_city": wedding_city,
                                            "death_city": death_city,
                                            "notes": ""}, index=[0])
                    df = pd.concat([df.loc[:], new_row]).reset_index(drop=True)
                    df.loc[df["id"] == tree.person.person_id, ["father_id"]] = father_id
                    df.to_csv("data/family.csv", index=False)
                    self.need_update = True
                else:
                    print("Already have a father")
            elif action == "mo":
                df = pd.read_csv("data/family.csv")
                field = ""
                available_fields = ["surname", "birth_name", "birth", "death", "wedding_date", "birth_city",
                                    "wedding_city", "death_city", "c", "notes"]
                print("=" * 10)
                print("List of fields : ")
                for f in available_fields:
                    print("-", f)
                print("=" * 10)
                while field not in available_fields:
                    field = input("Field to modify : ")
                if field == "c":
                    birth_city = input("Birth city : ")
                    wedding_city = input("Wedding city : ")
                    death_city = input("Death city : ")
                    df.loc[df["id"] == tree.person.person_id, ["birth_city"]] = birth_city
                    df.loc[df["id"] == tree.person.person_id, ["wedding_city"]] = wedding_city
                    df.loc[df["id"] == tree.person.person_id, ["death_city"]] = death_city
                    df.to_csv("data/family.csv", index=False)
                    self.need_update = True
                else:
                    value = input("New value : ")
                    df.loc[df["id"] == tree.person.person_id, [field]] = value
                    df.to_csv("data/family.csv", index=False)
                    self.need_update = True
            print("Done !")
            self.maximize()
        elif tree.mother_tree is not None and tree.father_tree is not None:
            self.get_person(tree.mother_tree, x, y)
            self.get_person(tree.father_tree, x, y)
        elif tree.mother_tree is not None:
            self.get_person(tree.mother_tree, x, y)
        elif tree.father_tree is not None:
            self.get_person(tree.father_tree, x, y)

    def check_size(self):
        if self.last_size != (self.width, self.height):
            self.on_screen_x = int(self.width / self.person_size)
            self.on_screen_y = int(self.height / self.person_size)
            self.last_size = (self.width, self.height)

    def scrolling(self):
        scroll_speed = max(15 - self.person_size, 1)
        if self.scroll_up:
            update_tree_pos(self.tree, 0, -scroll_speed)
            self.centuries_line.update(-scroll_speed)
        elif self.scroll_down:
            update_tree_pos(self.tree, 0, scroll_speed)
            self.centuries_line.update(scroll_speed)
        if self.scroll_right:
            update_tree_pos(self.tree, -scroll_speed, 0)
        elif self.scroll_left:
            update_tree_pos(self.tree, scroll_speed, 0)

    def updating(self):
        if self.need_update:
            self.persons, self.max_generation, self.root = load()
            temporary_offset_x, temporary_offset_y = self.tree.x_pos, self.tree.y_pos
            self.tree = grow_tree(self.root, 0, self.max_generation, {})
            initialization(self.tree)
            x_pos = temporary_offset_x - self.tree.x_pos
            update_tree_pos(self.tree, x_pos, temporary_offset_y)
            self.need_update = False

    def downloading_process(self):
        if self.time_remaining == 0:
            print(self.downloading_j, self.downloading_i)
            pyglet.image.get_buffer_manager().get_color_buffer() \
                .save("data/image_parts/" + str(self.downloading_j *
                                                (self.downloading_x + 1) + self.downloading_i) + ".png")
            if self.downloading_i == self.downloading_x and self.downloading_j == self.downloading_y:
                self.downloading = False
                paste_pictures(self.downloading_x + 1, self.downloading_y + 1, self.width, self.height,
                               self.person_size)
                self.minimize()
                print("Done !")
            elif self.downloading_i == self.downloading_x:
                self.downloading_i = 0
                self.downloading_j += 1
                update_tree_pos(self.tree, self.on_screen_x * (self.downloading_x + 1), -self.on_screen_y)
                self.centuries_line.update(-self.on_screen_y)
            else:
                self.downloading_i += 1
            self.time_remaining = self.time_to_wait
        elif self.time_remaining == self.time_to_wait:
            update_tree_pos(self.tree, -self.on_screen_x, 0)
            self.time_remaining -= 1
        else:
            self.time_remaining -= 1

    def merge(self):
        self.minimize()
        if self.merge_1.person_id == self.merge_2.person_id:
            print("Already the same person !")
        else:
            confirm = input(f"Do you really want to merge {self.merge_1.surname} {self.merge_1.birth_name} and "
                            f"{self.merge_2.surname} {self.merge_2.birth_name} y/[n] : ")
            if confirm == "y":
                to_be_kept = ""
                while to_be_kept not in ["1", "2"]:
                    to_be_kept = input(f"Do you want to keep 1 : {self.merge_1.person_id} {self.merge_1.surname} "
                                       f"{self.merge_1.birth_name} or 2 : {self.merge_2.person_id} {self.merge_2.surname} "
                                       f"{self.merge_2.birth_name} 1/2 : ")
                df = pd.read_csv("data/family.csv")
                if to_be_kept == "1":
                    to_be_deleted = self.get_person_to_delete(self.merge_2)
                    df.loc[df["mother_id"] == self.merge_2.person_id, ["mother_id"]] = self.merge_1.person_id
                    df.loc[df["father_id"] == self.merge_2.person_id, ["father_id"]] = self.merge_1.person_id
                else:
                    to_be_deleted = self.get_person_to_delete(self.merge_1)
                    df.loc[df["mother_id"] == self.merge_1.person_id, ["mother_id"]] = self.merge_2.person_id
                    df.loc[df["father_id"] == self.merge_1.person_id, ["father_id"]] = self.merge_2.person_id
                for p_id in to_be_deleted:
                    df = df.drop(df[df["id"] == p_id].index)
                df.to_csv("data/family.csv", index=False)
                fill_blanks()
                self.need_update = True
            self.maximize()
        self.merging = False
        self.merge_1 = None
        self.merge_2 = None

    def get_person_to_delete(self, person):
        if person.father is not None and person.mother is not None:
            return self.get_person_to_delete(person.father) \
                + self.get_person_to_delete(person.mother) \
                + [person.person_id]
        elif person.father is not None:
            return self.get_person_to_delete(person.father) + [person.person_id]
        elif person.mother is not None:
            return self.get_person_to_delete(person.mother) + [person.person_id]
        return [person.person_id]
