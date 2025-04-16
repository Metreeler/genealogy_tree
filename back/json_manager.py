import csv

def max_id(headers, data):
    return data[-1][headers[0].index("id")]

def cities(headers, data):
    out = []
    ids = [headers.index(x) for x in headers if "city" in x or "address" in x]
    
    for row in data:
        for id in ids:
            if row[id] != "":
                out.append(row[id])
    
    return list(set(out))

def find_person_to_delete(data, ids, parent_positions):
    for i in ids:
        for j in parent_positions:
            if data[i][j] >= 0 and data[i][j] not in ids:
                ids.append(data[i][j])
    return False, ids

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

def get_names(headers, data):
    out = []
    id = headers.index("name")
    for row in data:
        if row[id] != "":
            out.append(row[id])
    return out

def list_to_json(person_list, headers, id):
    out = {}
    try:
        for i in range(len(headers[0])):
                if headers[0][i] == "father":
                    out["father"] = list_to_json(person_list, headers, int(person_list[id][i])) if int(person_list[id][i]) >= 0 else {}
                elif headers[0][i] == "mother":
                    out["mother"] = list_to_json(person_list, headers, int(person_list[id][i])) if int(person_list[id][i]) >= 0 else {}
                elif headers[0][i] == "notes":
                    out[headers[0][i]] = eval(person_list[id][i])
                else:
                    out[headers[0][i]] = eval(headers[1][i])(person_list[id][i])
    except ValueError as e:
        print("problem :", e)
    return out

def remove_empty_ids(person_list, headers):
    id_position = headers[0].index("id")
    father_id_position = headers[0].index("father")
    mother_id_position = headers[0].index("mother")
    
    person_list = sorted(person_list, key=lambda x: x[id_position])
        
    for i in range(len(person_list)):
        if i < person_list[i][id_position]:
            diff = i - int(person_list[i][id_position])
            for j in range(len(person_list)):
                for h in [id_position, father_id_position, mother_id_position]:
                    if person_list[j][h] > i:
                        person_list[j][h] += diff
    return person_list

def load_list(file_name):
    try:
        with open(file_name, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            headers = []
            headers.append(csv_reader.__next__())
            headers.append(csv_reader.__next__())
            person_list = []
            for row in csv_reader:
                person_list.append(row)
        
        
        for j in range(len(headers[0])):
            for i in range(len(person_list)):
                if headers[0][i] == "notes":
                    person_list[i][j] = eval(eval(person_list[i][j]))
                else:
                    person_list[i][j] = eval(headers[1][j])(person_list[i][j])
        
        person_list = remove_empty_ids(person_list, headers)
                            
        return headers, person_list
    except ValueError as e:
        print("Main fields missing", e)
        return [], []

def json_to_list(data, headers):
    out = [[]]
    for key in headers:
        if key not in ["father", "mother"]:
            if key != "notes":
                out[0].append(data[key])
            else:
                out[0].append(repr(data[key]))
    
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

def save_csv(file_name, headers, data):
    out = data.copy()
    out.insert(0, headers[1])
    out.insert(0, headers[0])
    with open(file_name, 'w', newline='') as csvfile:
        line_writer = csv.writer(csvfile, delimiter=',')
        line_writer.writerows(out)