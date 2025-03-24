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

if __name__ == "__main__":
    # _reduced
    with open("data/family.json") as f:
        data = json.load(f)
    
    names = get_names(data, [])
    
    out = {"colors":[]}
    
    for name in names:
        out["colors"].append({
            "name": name,
            "color": "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            })
    
    with open('data/colors.json', 'w') as f:
        json.dump(out, f)