import pyglet


def split_by_generation(persons, max_generation):
    generations = []
    for i in range(max_generation + 1):
        generations.append(2000)
    for p in persons:
        if p.birth != "-":
            data = p.birth.split("-")
            if int(data[2]) < generations[p.generation]:
                generations[p.generation] = int(data[2])
    start_span = 2000
    for gen in generations:
        if 100 * int(gen / 100) < start_span:
            start_span = 100 * int(gen / 100)
    centuries = [*range(start_span, 2100, 100)]
    corresponding_generation = []
    for _ in centuries:
        corresponding_generation.append(0)
    for i in range(len(centuries)):
        for j in range(len(generations)):
            if j > corresponding_generation[i] and generations[j] > centuries[i]:
                corresponding_generation[i] = j
    return centuries, corresponding_generation


class CenturiesLine:
    def __init__(self, persons, max_generation):
        self.centuries, self.generations = split_by_generation(persons, max_generation)
        for i in range(len(self.generations)):
            self.generations[i] *= 5
            self.generations[i] += 4

    def show(self, size, width, years):
        for i in range(len(self.generations)):
            if 0 < self.generations[i] < width / size:
                line = pyglet.shapes.Line(0, self.generations[i] * size,
                                          width, self.generations[i] * size,
                                          width=4, color=(200, 200, 200))
                line.draw()
                if years:
                    label = pyglet.text.Label(str(self.centuries[i]),
                                              font_name='Arial',
                                              font_size=size,
                                              x=width - 4 * size,
                                              y=self.generations[i] * size - size,
                                              anchor_x='center',
                                              anchor_y='center',
                                              color=(0, 0, 0, 255),
                                              multiline=True,
                                              width=1)
                    label.draw()

    def update(self, offset):
        for i in range(len(self.generations)):
            self.generations[i] += offset
