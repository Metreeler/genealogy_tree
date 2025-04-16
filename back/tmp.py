import json
import random
import csv

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

# def absent_id(json):
#     ids = get_id(data, [])
#     absent = []
#     for i in range(max_id(data)):
#         if i not in ids:
#             absent.append(i)
#     print(absent)
    
def add_field(data, field, default_value):
    data[field] = default_value
    if data["father"]:
        data["father"] = add_field(data["father"], field, default_value)
    if data["mother"]:
        data["mother"] = add_field(data["mother"], field, default_value)
    return data

def json_to_list(data, headers):
    out = [[]]
    for key in headers:
        if key not in ["father", "mother"]:
            if key != "notes":
                out[0].append(data[key])
            else:
                out[0].append(repr(data[key]))
    
    print(out)
    
    if data["father"]:
        out[0].append(data["father"]["id"])
        father_list = json_to_list(data["father"], headers)
        for person in father_list:
            out.append(person)
    else:
        out[0].append(-1)
    if data["mother"]:
        out[0].append(data["mother"]["id"])
        mother_list = json_to_list(data["mother"], headers)
        for person in mother_list:
            out.append(person)
    else:
        out[0].append(-1)
    return out

def list_to_json(person_list, headers, id):
    out = {}
    for i in range(len(headers)):
        try:
            if headers[i] == "father":
                out["father"] = list_to_json(person_list, headers, int(person_list[id][i])) if int(person_list[id][i]) >= 0 else {}
            elif headers[i] == "mother":
                out["mother"] = list_to_json(person_list, headers, int(person_list[id][i])) if int(person_list[id][i]) >= 0 else {}
            else:
                out[headers[i]] = int(person_list[id][i])
        except ValueError:
            if i == headers.index("notes"):
                out[headers[i]] = eval(person_list[id][i])
                continue
            out[headers[i]] = person_list[id][i]
    return out

def load_list_as_json(file_name):
    
    with open(file_name, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        headers = csv_reader.__next__()
        person_list = []
        for row in csv_reader:
            person_list.append(row)
            
    if "id" in headers and "father" in headers and "mother" in headers and "show_parent" in headers:
        id_position = headers.index("id")
        father_id_position = headers.index("father")
        mother_id_position = headers.index("mother")
        show_parent_id_position = headers.index("show_parent")
        
        for j in [id_position, father_id_position, mother_id_position]:
            for i in range(len(person_list)):
                try:
                    person_list[i][j] = int(person_list[i][j])
                except ValueError:
                    print("wrong id :", i, person_list[i][j])
                    return {}
                
        for i in range(len(person_list)):
            try:
                person_list[i][show_parent_id_position] = eval(person_list[i][show_parent_id_position])
            except ValueError:
                print("wrong show_parent_value :", i, person_list[i][show_parent_id_position])
                return {}
        
        person_list = sorted(person_list, key=lambda x: x[id_position])
        
        for i in range(len(person_list)):
            if i < int(person_list[i][id_position]):
                diff = i - int(person_list[i][id_position])
                for j in range(len(person_list)):
                    for h in [id_position, father_id_position, mother_id_position]:
                        if person_list[j][h] > i:
                            person_list[j][h] += diff
        
        return list_to_json(person_list, headers, 0)
    print("Main fields missing")
    return {}

def save_json_as_csv(file_name, data):
    headers = list(data.keys())
    if "id" in headers and "father" in headers and "mother" in headers and "show_parent" in headers:
        headers.append(headers.pop(headers.index("father")))
        headers.append(headers.pop(headers.index("mother")))
        csv_out = sorted(json_to_list(data, headers), key=lambda x: x[0])
    
        id_position = headers.index("id")
        father_id_position = headers.index("father")
        mother_id_position = headers.index("mother")
        show_parent_id_position = headers.index("show_parent")
        
        for j in [id_position, father_id_position, mother_id_position]:
            for i in range(len(csv_out)):
                try:
                    csv_out[i][j] = int(csv_out[i][j])
                except ValueError:
                    print("wrong id :", i, j)
                
        for i in range(len(csv_out)):
            try:
                csv_out[i][show_parent_id_position] = bool(csv_out[i][show_parent_id_position])
            except ValueError:
                print("wrong show_parent_value :", i, csv_out[i][show_parent_id_position])
                return {}
                    
        for i in range(len(csv_out)):
            if i < int(csv_out[i][id_position]):
                diff = i - int(csv_out[i][id_position])
                for j in range(len(csv_out)):
                    for h in [id_position, father_id_position, mother_id_position]:
                        if csv_out[j][h] > i:
                            csv_out[j][h] += diff
        
        csv_out.insert(0, headers)
        
        with open(file_name, 'w', newline='') as csvfile:
            line_writer = csv.writer(csvfile, delimiter=',')
            line_writer.writerows(csv_out)
    else:
        print("Main fields missing")

if __name__ == "__main__":
    
    # data = load_list_as_json("data/family_reduced.csv")
    with open("data/family.json") as f:
        data = json.load(f)
    save_json_as_csv("data/family.csv", data)
    
    # _reduced
    
    # DATA JSON TO CSV
    
    # with open("data/family.json") as f:
    #     data = json.load(f)
        
    # csv_out = sorted(json_to_list(data), key=lambda x: x[0])
    
    # id_position = 0
    # father_id_position = 13
    # mother_id_position = 14
    
    # for j in [id_position, father_id_position, mother_id_position]:
    #     for i in range(len(csv_out)):
    #         try:
    #             csv_out[i][j] = int(csv_out[i][j])
    #         except ValueError:
    #             print("wrong id")
                
    # for i in range(len(csv_out)):
    #     if i < int(csv_out[i][id_position]):
    #         diff = i - int(csv_out[i][id_position])
    #         for j in range(len(csv_out)):
    #             for h in [id_position, father_id_position, mother_id_position]:
    #                 if csv_out[j][h] > i:
    #                     csv_out[j][h] += diff
    
    # csv_out.insert(0, [
    #     "id",
    #     "surname",
    #     "name",
    #     "gender",
    #     "generation",
    #     "birth",
    #     "wedding",
    #     "death",
    #     "birth_city",
    #     "wedding_city",
    #     "death_city",
    #     "show_parent",
    #     "notes",
    #     "father_id",
    #     "mother_id"
    # ])
    
    # with open('data/family.csv', 'w', newline='') as csvfile:
    #     line_writer = csv.writer(csvfile, delimiter=',')
    #     line_writer.writerows(csv_out)
    
    # DATA CSV TO JSON
    
    # with open('data/family_reduced.csv', 'r', newline='') as csvfile:
    #     csv_reader = csv.reader(csvfile)
    #     headers = csv_reader.__next__()
    #     person_list = []
    #     for row in csv_reader:
    #         person_list.append(row)
    #         # for i in range(len(headers)):
    #         #     try:
    #         #         int(row[i])
    #         #         print(headers[i], int(row[i]))
    #         #     except ValueError:
    #         #         # print(headers[i], row[i])
    #         #         pass
            
    # if "id" in headers and "father_id" in headers and "mother_id" in headers:
    #     id_position = headers.index("id")
    #     father_id_position = headers.index("father_id")
    #     mother_id_position = headers.index("mother_id")
        
    #     for j in [id_position, father_id_position, mother_id_position]:
    #         for i in range(len(person_list)):
    #             try:
    #                 person_list[i][j] = int(person_list[i][j])
    #             except ValueError:
    #                 print("wrong id")
        
    #     person_list = sorted(person_list, key=lambda x: x[id_position])
        
    #     for i in range(len(person_list)):
    #         if i < int(person_list[i][id_position]):
    #             diff = i - int(person_list[i][id_position])
    #             for j in range(len(person_list)):
    #                 for h in [id_position, father_id_position, mother_id_position]:
    #                     if person_list[j][h] > i:
    #                         person_list[j][h] += diff
        
    #     print(list_to_json(person_list, headers, 0))
    
    
    # try:
    #     int("a")
    #     print("a")
    # except ValueError:
    #     pass
    # try:
    #     int("1")
    #     print("1")
    # except ValueError:
    #     pass