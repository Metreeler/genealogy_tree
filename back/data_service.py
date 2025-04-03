import json
import random

def max_id(json):
    out = json["id"]
    if json["father"]:
        out = max(max_id(json["father"]), out)
    if json["mother"]:
        out = max(max_id(json["mother"]), out)
    return out

def cities(json, city_list):
    if json["father"]:
        city_list = cities(json["father"], city_list)
    if json["mother"]:
        city_list = cities(json["mother"], city_list)
    
    if "birth_city" in json.keys() and json["birth_city"] not in city_list:
        city_list = city_list + [json["birth_city"]]
    if "death_city" in json.keys() and json["death_city"] not in city_list:
        city_list = city_list + [json["death_city"]]
    if "wedding_city" in json.keys() and json["wedding_city"] not in city_list:
        city_list = city_list + [json["wedding_city"]]
    if "address" in json.keys() and json["address"] not in city_list:
        city_list = city_list + [json["address"]]
    
    return city_list

def update_person(data, update_values):
    if (data["id"] == update_values["id"]):
        for k in update_values.keys():
            data[k] = update_values[k]
        return data
    if data["father"]:
        data["father"] = update_person(data["father"], update_values)
    if data["mother"]:
        data["mother"] = update_person(data["mother"], update_values)
    return data

def update_parent_visibility(data, id):
    if (data["id"] == id):
        data["show_parent"] = not data["show_parent"]
        return data
    if data["father"]:
        data["father"] = update_parent_visibility(data["father"], id)
    if data["mother"]:
        data["mother"] = update_parent_visibility(data["mother"], id)
    return data

def delete_person(data, id):
    if (data["id"] == id):
        return {}
    if data["father"]:
        data["father"] = delete_person(data["father"], id)
    if data["mother"]:
        data["mother"] = delete_person(data["mother"], id)
    return data

def add_parent(data, id, parent):
    if (data["id"] == id):
        if parent["gender"] == "M":
            data["father"] = parent
        if parent["gender"] == "F":
            data["mother"] = parent
            return data
    if data["father"]:
        data["father"] = add_parent(data["father"], id, parent)
    if data["mother"]:
        data["mother"] = add_parent(data["mother"], id, parent)
    return data

def get_names(json, name_list):
    if json["father"]:
        name_list = get_names(json["father"], name_list)
    if json["mother"]:
        name_list = get_names(json["mother"], name_list)
    if json["name"] not in name_list:
        return name_list + [json["name"]]
    return name_list

def check_fields(data, fields):
    for k in fields.keys():
        if k not in data.keys():
            data[k] = fields[k]
    if data["father"]:
        data["father"] = check_fields(data["father"], fields)
    if data["mother"]:
        data["mother"] = check_fields(data["mother"], fields)
    return data
    

class DataService:
    def __init__(self, reduced):
        self.reduced_text = ""
        if reduced:
            self.reduced_text = "_reduced"
        
        self.data = {}
        self.colors = {}
        self.cities = []
        
        self.load_local_data()
        
    def check_fields(self, fields):
        check_fields(self.data, fields)
        with open("data/family" + self.reduced_text + ".json", 'w') as f:
            json.dump(self.data, f)
        return "Fields checked"
    
    def get_max_id(self):
        return max_id(self.data)
    
    def get_data(self):
        return self.data
    
    def get_colors(self):
        return self.colors
    
    def get_cities(self):
        return self.cities
    
    def update_person(self, dict: dict):
        self.data = update_person(self.data, dict)
    
        self.save_local_data()
            
        return "Person updated"
    
    def update_parent_visibility(self, id):
        self.data = update_parent_visibility(self.data, id)
        return "Visibility updated"
    
    def add_parent(self, id, dict:dict):
        awaited_keys = ['id', 'surname', 'name', 'gender', 'birth', 'death', 'wedding', 'birth_city', 'wedding_city', 'death_city', 'notes', 'show_parent']
        for k in awaited_keys:
            if k not in dict.keys():
                return "Missing keys"
        if dict["id"] < 0:
            return "Wrong id"
        dict["father"] = {}
        dict["mother"] = {}
        
        self.data = add_parent(self.data, id, dict)
        
        self.save_local_data()
        
        return "parent added"
        
    
    def delete_person(self, id):
        self.data = delete_person(self.data, id)
        
        self.save_local_data()
        
        return "Person deleted"
    
    def load_local_data(self):
        with open("data/family" + self.reduced_text + ".json") as f:
            self.data = json.load(f)
        
        with open("data/colors" + self.reduced_text + ".json") as f:
            self.colors = json.load(f)
        
        self.cities = cities(self.data, [])
        
    def save_local_data(self):
        with open("data/family" + self.reduced_text + ".json", 'w') as f:
            json.dump(self.data, f)
        
        new_names = get_names(self.data, [])
        new_colors = []
        
        for name in new_names:
            new_colors.append(next((color for color in self.colors["colors"] if color["name"] == name), {
                        "name": name,
                        "color": "#"+''.join([random.choice('456789ABCDEF') + random.choice('0123456789ABCDEF') for _ in range(3)])
                    }))
        self.colors["colors"] = new_colors
        
        with open("data/colors" + self.reduced_text + ".json", 'w') as f:
            json.dump(self.colors, f)
        
        self.cities = cities(self.data, [])
        