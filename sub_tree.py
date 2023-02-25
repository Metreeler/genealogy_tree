import math
import pyglet
import random


class SubTree:
    def __init__(self, person, mother, father, x_pos, y_pos, generation, max_generation, dictionary):
        self.person = person
        self.mother = mother
        self.father = father
        self.width = math.pow(2, max_generation - generation)
        self.father_width = self.width / 2
        self.mother_width = self.width / 2
        if self.person.birth_name not in dictionary.keys():
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            dictionary.update({self.person.birth_name: self.color})
        else:
            self.color = dictionary.get(self.person.birth_name)

        self.x_pos = x_pos
        self.y_pos = y_pos

        self.mother_tree = None
        self.father_tree = None
        if self.father is not None:
            self.father_tree = SubTree(father,
                                       father.mother,
                                       father.father,
                                       x_pos + self.width / 2,
                                       y_pos + 5,
                                       father.generation,
                                       max_generation,
                                       dictionary)
        if self.mother is not None:
            self.mother_tree = SubTree(mother,
                                       mother.mother,
                                       mother.father,
                                       x_pos - self.width / 2,
                                       y_pos + 5,
                                       mother.generation,
                                       max_generation,
                                       dictionary)

    def show(self, size):
        if self.person.person_id > 0:
            if self.father is not None or self.mother is not None:
                if self.father is not None:
                    self.father_width = abs(self.x_pos - self.father_tree.x_pos)
                else:
                    self.father_width = 0
                if self.mother is not None:
                    self.mother_width = abs(self.x_pos - self.mother_tree.x_pos)
                else:
                    self.mother_width = 0
                width = max(size / 10, 2)
                line1 = pyglet.shapes.Line(int((self.x_pos - self.mother_width) * size + size / 2),
                                           int((self.y_pos + 5) * size + size / 2),
                                           int((self.x_pos + self.father_width) * size + size / 2),
                                           int((self.y_pos + 5) * size + size / 2),
                                           width=width,
                                           color=(0, 0, 0))
                line2 = pyglet.shapes.Line(int(self.x_pos * size + size / 2),
                                           int(self.y_pos * size + size / 2),
                                           int(self.x_pos * size + size / 2),
                                           int((self.y_pos + 5) * size + size / 2),
                                           width=width,
                                           color=(0, 0, 0))
                line1.draw()
                line2.draw()
            if self.person.genre == "M":
                square = pyglet.shapes.Rectangle(int(self.x_pos * size),
                                                 int(self.y_pos * size),
                                                 size,
                                                 size,
                                                 color=self.color)
                square.draw()
            else:
                circle = pyglet.shapes.Circle(int(self.x_pos * size + size / 2),
                                              int(self.y_pos * size + size / 2),
                                              size / 2,
                                              color=self.color)
                circle.draw()

            if size >= 30:
                label1 = pyglet.text.Label(self.person.surname + "\n" +
                                           self.person.birth_name + "\n" +
                                           self.person.birth + "\n" +
                                           self.person.wedding + "\n" +
                                           self.person.death,
                                           font_name='Arial',
                                           font_size=size / 4,
                                           x=self.x_pos * size - 3 * size / 8,
                                           y=self.y_pos * size,
                                           anchor_x='left',
                                           anchor_y='top',
                                           color=(0, 0, 0, 255),
                                           multiline=True,
                                           width=10)
                label1.draw()
        else:
            if self.father is not None:
                self.father_width = abs(self.x_pos - self.father_tree.x_pos)
            else:
                self.father_width = 0
            if self.mother is not None:
                self.mother_width = abs(self.x_pos - self.mother_tree.x_pos)
            else:
                self.mother_width = 0
            width = max(size / 10, 2)
            line1 = pyglet.shapes.Line(int((self.x_pos - self.mother_width) * size + size / 2),
                                       int((self.y_pos + 5) * size + size / 2),
                                       int((self.x_pos + self.father_width) * size + size / 2),
                                       int((self.y_pos + 5) * size + size / 2),
                                       width=width,
                                       color=(0, 0, 0))
            line2 = pyglet.shapes.Line(int(self.x_pos * size + size / 2),
                                       int((self.y_pos + 1) * size + size / 2),
                                       int(self.x_pos * size + size / 2),
                                       int((self.y_pos + 5) * size + size / 2),
                                       width=width,
                                       color=(0, 0, 0))
            line3 = pyglet.shapes.Line(int((self.x_pos - 2) * size + size / 2),
                                       int((self.y_pos + 1) * size + size / 2),
                                       int((self.x_pos + 2) * size + size / 2),
                                       int((self.y_pos + 1) * size + size / 2),
                                       width=width,
                                       color=(0, 0, 0))
            line4 = pyglet.shapes.Line(int((self.x_pos - 2) * size + size / 2),
                                       int((self.y_pos + 1) * size + size / 2),
                                       int((self.x_pos - 2) * size + size / 2),
                                       int(self.y_pos * size + size / 2),
                                       width=width,
                                       color=(0, 0, 0))
            line5 = pyglet.shapes.Line(int((self.x_pos + 2) * size + size / 2),
                                       int((self.y_pos + 1) * size + size / 2),
                                       int((self.x_pos + 2) * size + size / 2),
                                       int(self.y_pos * size + size / 2),
                                       width=width,
                                       color=(0, 0, 0))
            line1.draw()
            line2.draw()
            line3.draw()
            line4.draw()
            line5.draw()

            square1 = pyglet.shapes.Rectangle(int((self.x_pos - 2) * size),
                                              int(self.y_pos * size),
                                              size,
                                              size,
                                              color=self.color)
            square2 = pyglet.shapes.Rectangle(int((self.x_pos + 2) * size),
                                              int(self.y_pos * size),
                                              size,
                                              size,
                                              color=self.color)
            square1.draw()
            square2.draw()

            if size >= 30:
                label1 = pyglet.text.Label(self.person.surname + "\n" +
                                           self.person.birth_name + "\n" +
                                           self.person.birth + "\n" +
                                           self.person.wedding + "\n" +
                                           self.person.death,
                                           font_name='Arial',
                                           font_size=size / 4,
                                           x=(self.x_pos + 2) * size - size / 2,
                                           y=self.y_pos * size,
                                           anchor_x='left',
                                           anchor_y='top',
                                           color=(0, 0, 0, 255),
                                           multiline=True,
                                           width=1)
                label2 = pyglet.text.Label("Leo\nHANGRAN\n19-01-2007\n-\n-",
                                           font_name='Arial',
                                           font_size=size / 4,
                                           x=(self.x_pos - 2) * size - size / 2,
                                           y=self.y_pos * size,
                                           anchor_x='left',
                                           anchor_y='top',
                                           color=(0, 0, 0, 255),
                                           multiline=True,
                                           width=1)
                label1.draw()
                label2.draw()
