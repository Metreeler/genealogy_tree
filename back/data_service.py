import json
import random
import csv
from json_manager import *
    

class DataService:
    def __init__(self, reduced):
        self.reduced_text = ""
        if reduced:
            self.reduced_text = "_reduced_new"
        
        self.data_list = []
        self.headers = []
        self.colors = {}
        self.cities = []
        
        self.load_local_data()
        
    def check_fields(self, fields):
        for field in fields:
            if field not in self.headers[0]:
                return "Field : " + field + " not found"
        return "Fields checked"
    
    def get_max_id(self):
        return max_id(self.headers, self.data_list)
    
    def get_data(self):
        return list_to_json(self.data_list, self.headers, 0)
    
    def get_colors(self):
        return self.colors
    
    def get_cities(self):
        return self.cities
    
    def update_person(self, id, dict: dict):
        idx = next((self.data_list.index(x) for x in self.data_list if x[self.headers[0].index("id")] == id), -1)
        if idx >= 0:
            keys = list(dict.keys())
            
            for key in keys:
                if key in self.headers[0]:
                    if key == "notes":
                        self.data_list[idx][self.headers[0].index(key)] = repr(dict[key])
                    else:
                        self.data_list[idx][self.headers[0].index(key)] = eval(self.headers[1][self.headers[0].index(key)])(dict[key])
        
            self.save_local_data()
                
            return "Person updated"
        return "Person id not valid"
    
    def update_parent_visibility(self, id):
        idx = next((self.data_list.index(x) for x in self.data_list if x[self.headers[0].index("id")] == id), -1)
        if idx >= 0:
            try:
                self.data_list[idx][self.headers[0].index("show_parent")] = not self.data_list[idx][self.headers[0].index("show_parent")]
                return "Visibility updated"
            except ValueError as e:
                return "Visibility error : " + e
        
        return "Person id not valid"
    
    def add_parent(self, id, gender):
        idx = next((self.data_list.index(x) for x in self.data_list if x[self.headers[0].index("id")] == id), -1)
        new_id = max_id(self.headers, self.data_list) + 1
        try:
            if idx >= 0:
                parent = []
                for typ in self.headers[1]:
                    parent.append(eval(typ)())
                parent[self.headers[0].index("id")] = new_id
                parent[self.headers[0].index("gender")] = gender
                parent[self.headers[0].index("father")] = -1
                parent[self.headers[0].index("mother")] = -1
                parent[self.headers[0].index("show_parent")] = True
                parent[self.headers[0].index("notes")] = repr("")
                parent[self.headers[0].index("generation")] = self.data_list[idx][self.headers[0].index("generation")] + 1
                if gender == "M":
                    self.data_list[idx][self.headers[0].index("father")] = new_id
                    parent[self.headers[0].index("name")] = self.data_list[idx][self.headers[0].index("name")]
                else:
                    self.data_list[idx][self.headers[0].index("mother")] = new_id
                self.data_list.append(parent)
        except ValueError as e:
            return "Adding parent failed : " + e
        
        self.save_local_data()
        
        return "Parent added"
        
    
    def delete_person(self, id):
        idx = next((self.data_list.index(x) for x in self.data_list if x[self.headers[0].index("id")] == id), -1)
        if idx >= 0:
            to_delete = [idx]
            need_check = True
            parent_pos = [self.headers[0].index(x) for x in self.headers[0] if x in ["mother", "father"]]
            while need_check:
                need_check, to_delete = find_person_to_delete(self.data_list, to_delete, parent_pos)
            to_delete = sorted(to_delete, key=lambda x: x, reverse=True)
            
            for person in to_delete:
                self.data_list.pop(person)
            for i in range(len(self.data_list)):
                for j in parent_pos:
                    if self.data_list[i][j] in to_delete:
                        self.data_list[i][j] = -1
        
        remove_empty_ids(self.data_list, self.headers)
        
        self.save_local_data()
        
        return "Person deleted"
    
    def load_local_data(self):
        self.headers, self.data_list = load_list("data/family" + self.reduced_text + ".csv")
        
        with open("data/colors" + self.reduced_text + ".json") as f:
            self.colors = json.load(f)
        
        self.cities = cities(self.headers, self.data_list)
        
    def save_local_data(self):
        save_csv("data/family" + self.reduced_text + ".csv", self.headers, self.data_list)
        
        new_names = get_names(self.headers[0], self.data_list)
        new_colors = []
        
        for name in new_names:
            new_colors.append(next((color for color in self.colors["colors"] if color["name"] == name), {
                        "name": name,
                        "color": "#"+''.join([random.choice('456789ABCDEF') + random.choice('0123456789ABCDEF') for _ in range(3)])
                    }))
        self.colors["colors"] = new_colors
        
        with open("data/colors" + self.reduced_text + ".json", 'w') as f:
            json.dump(self.colors, f)
        
        self.cities = cities(self.headers, self.data_list)
        