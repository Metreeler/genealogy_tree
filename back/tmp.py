import json
import random

def get_names(json, name_list):
    if json["father"]:
        name_list = get_names(json["father"], name_list)
    if json["mother"]:
        name_list = get_names(json["mother"], name_list)
    if json["name"] not in name_list:
        return name_list + [json["name"]]
    return name_list

def get_max_id(json):
    out = json["id"]
    if json["father"]:
        out = max(get_max_id(json["father"]), out)
    if json["mother"]:
        out = max(get_max_id(json["mother"]), out)
    return out

def get_id(json, id_list):
    if json["father"]:
        id_list = get_id(json["father"], id_list)
    if json["mother"]:
        id_list = get_id(json["mother"], id_list)
    return id_list + [json["id"]]

def max_id(json):
    out = json["id"]
    if json["father"]:
        out = max(max_id(json["father"]), out)
    if json["mother"]:
        out = max(max_id(json["mother"]), out)
    return out

def check_duplicate(json):
        
    ids = get_id(json, [])
    test = []
    dup = []
    for i in ids:
        if i in test:
            dup.append(i)
        test.append(i)
    print(dup)
    print(max_id(json))

def absent_id(json):
    ids = get_id(data, [])
    absent = []
    for i in range(max_id(data)):
        if i not in ids:
            absent.append(i)
    print(absent)
    
def add_field(data, field, default_value):
    data[field] = default_value
    if data["father"]:
        data["father"] = add_field(data["father"], field, default_value)
    if data["mother"]:
        data["mother"] = add_field(data["mother"], field, default_value)
    return data
    

if __name__ == "__main__":
    # _reduced
    
    # with open("data/family.json") as f:
    #     data = json.load(f)
    
    # data = add_field(data, "address", "") 
    
    # with open('data/family.json', 'w') as f:
    #     json.dump(data, f)
    
    with open("data/colors_reduced.json") as f:
        data = json.load(f)
    
    new_names = ["HANGRAN", "CATHELINE", "TEST"]
    
    new_colors = []
    
    for name in new_names:
        new_colors.append(next((color for color in data["colors"] if color["name"] == name), {
                    "name": name,
                    "color": "#"+''.join([random.choice('0123456789ABCDEF') for _ in range(6)])
                }))
    
    print(new_colors)
    
    # data = add_field(data, "address", "") 
    
    # with open('data/colors_reduced.json', 'w') as f:
    #     json.dump(data, f)
        
        
    # existing_names = next((col for col in self.colors["colors"] if col["name"] not in ))
    # for color in self.colors["colors"]:
    #     if color["name"] not in existing_names:
    #         existing_names.append(color["name"])