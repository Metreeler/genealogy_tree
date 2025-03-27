import json

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
    
    if json["birth_city"] not in city_list:
        city_list = city_list + [json["birth_city"]]
    if json["death_city"] not in city_list:
        city_list = city_list + [json["death_city"]]
    if json["wedding_city"] not in city_list:
        city_list = city_list + [json["wedding_city"]]
    
    return city_list

def update_person(data, update_values):
    if (data["id"] == update_values["id"]):
        data["surname"] = update_values["surname"]
        data["name"] = update_values["name"]
        data["gender"] = update_values["gender"]
        data["birth"] = update_values["birth"]
        data["wedding"] = update_values["wedding"]
        data["death"] = update_values["death"]
        data["birth_city"] = update_values["birth_city"]
        data["wedding_city"] = update_values["wedding_city"]
        data["death_city"] = update_values["death_city"]
        data["notes"] = update_values["notes"]
        return data
    if data["father"]:
        data["father"] = update_person(data["father"], update_values)
    if data["mother"]:
        data["mother"] = update_person(data["mother"], update_values)
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
    

class DataService:
    def __init__(self, reduced):
        self.reduced_text = ""
        if reduced:
            self.reduced_text = "_reduced"
        
        self.data = {}
        self.colors = {}
        self.cities = []
        
        self.load_local_data()
    
    def get_max_id(self):
        return max_id(self.data)
    
    def get_data(self):
        return self.data
    
    def get_colors(self):
        return self.colors
    
    def get_cities(self):
        return self.cities
    
    def update_person(self, dict: dict):
        awaited_keys = ['id', 'surname', 'name', 'gender', 'birth', 'death', 'wedding', 'birth_city', 'wedding_city', 'death_city', 'notes']
        for k in awaited_keys:
            if k not in dict.keys():
                return "Missing keys"
        if dict["id"] < 0:
            return "Wrong id"
        self.data = update_person(self.data, dict)
    
        self.save_local_data()
            
        return "Person updated"
    
    def add_parent(self, id, dict:dict):
        awaited_keys = ['id', 'surname', 'name', 'gender', 'birth', 'death', 'wedding', 'birth_city', 'wedding_city', 'death_city', 'notes']
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
        
        self.cities = cities(self.data, [])
        