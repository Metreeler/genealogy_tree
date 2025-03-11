

class Person:
    def __init__(self, person_id, surname, birth_name, genre, birth, death, wedding,
                 father_id, mother_id, father, mother, generation, birth_city, wedding_city, death_city):
        self.person_id = int(person_id)
        self.surname = surname
        self.birth_name = birth_name
        self.genre = genre
        self.birth = birth
        self.death = death
        self.wedding = wedding
        self.father = father
        self.mother = mother
        self.father_id = father_id
        self.mother_id = mother_id
        self.generation = int(generation)
        self.birth_city = birth_city
        self.wedding_city = wedding_city
        self.death_city = death_city

    def has_parent(self):
        if self.father is not None or self.mother is not None:
            return True
        return False

    def number_of_ancestors(self):
        if self.has_parent():
            if self.father is None:
                nb_of_ancestors_mother, ancestor_mother = self.mother.number_of_ancestors()
                return nb_of_ancestors_mother + 1, ancestor_mother
            elif self.mother is None:
                nb_of_ancestors_father, ancestor_father = self.father.number_of_ancestors()
                return nb_of_ancestors_father + 1, ancestor_father
            nb_of_ancestors_mother, ancestor_mother = self.mother.number_of_ancestors()
            nb_of_ancestors_father, ancestor_father = self.father.number_of_ancestors()
            if nb_of_ancestors_father > nb_of_ancestors_mother:
                return nb_of_ancestors_father + 1, ancestor_father
            else:
                return nb_of_ancestors_mother + 1, ancestor_mother
        return 0, self

    def __str__(self):
        if self.father is not None:
            father_name = self.father.surname + " " + self.father.birth_name
        else:
            father_name = "Unknown"
        if self.mother is not None:
            mother_name = self.mother.surname + " " + self.mother.birth_name
        else:
            mother_name = "Unknown"
        return "id : " + str(self.person_id) + \
            "\nname : " + self.surname + " " + self.birth_name + \
            "\nbirth date : " + self.birth + \
            "\nwedding date : " + self.wedding + \
            "\ndeath date : " + self.death + \
            "\nbirth city : " + self.birth_city + \
            "\nwedding city : " + self.wedding_city + \
            "\ndeath city : " + self.death_city + \
            "\nfather : " + father_name + \
            "\nmother : " + mother_name
