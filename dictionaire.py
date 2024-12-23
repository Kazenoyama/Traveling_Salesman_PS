import matplotlib.pyplot as plt

def readFiles(path):
    # Lecture du fichier
    with open(path, 'r') as file:
        data_size = int(file.readline().strip())
        lines = file.readlines()
        if len(lines) != data_size:
            raise ValueError("Le nombre de lignes ne correspond pas à la taille spécifiée")
    return data_size, lines

def count_H_V_occurence(lines):
    word_counts = {"H" : 0, "V" : 0}
    for line in lines:
        parts = line.split()
        if len(parts) < 2:
            continue
        line_type = parts[0]
        if line_type == 'H':
            word_counts["H"] += 1
        else:
            word_counts["V"] += 1
    return word_counts

def tag_count(lines):
    tags = {}
    for line in lines:
        parts = line.split()
        if len(parts) < 3:
            continue
        tags_count = int(parts[1])
        tags_list = parts[2:]
        for tag in tags_list:
            if tag in tags:
                tags[tag] += tags_count
            else:
                tags[tag] = tags_count
    return tags

def average_repition(tags):
    total = 0
    for tag in tags:
        total += tags[tag]
    return total / len(tags)

data_size, lines = readFiles("./hashcode/b_lovely_landscapes.txt")
tags = tag_count(lines)
print(average_repition(tags))
print(tags.__len__())

data_size, lines = readFiles("./hashcode/d_pet_pictures.txt")
tags = tag_count(lines)
print(average_repition(tags))
print(tags.__len__())

data_size, lines = readFiles("./hashcode/e_shiny_selfies.txt")
tags = tag_count(lines)
print(average_repition(tags))
print(tags.__len__())

