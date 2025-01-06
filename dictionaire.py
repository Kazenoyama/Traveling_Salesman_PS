from collections import defaultdict
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

def tags_repition_distrubition():
    to_plot = []
    data_size, lines = readFiles("./hashcode/b_lovely_landscapes.txt")
    tags = tag_count(lines)
    print(average_repition(tags))
    print(tags.__len__())
    to_plot.append([tags.__len__(), average_repition(tags)])

    data_size, lines = readFiles("./hashcode/d_pet_pictures.txt")
    tags = tag_count(lines)
    print(average_repition(tags))
    print(tags.__len__())
    to_plot.append([tags.__len__(), average_repition(tags)])

    data_size, lines = readFiles("./hashcode/e_shiny_selfies.txt")
    tags = tag_count(lines)
    print(average_repition(tags))
    print(tags.__len__())
    to_plot.append([tags.__len__(), average_repition(tags)])


    X = [x[0] for x in to_plot]
    labels = ['b_lovely_landscapes', 'd_pet_pictures', 'e_shiny_selfies']
    plt.bar(labels, X)
    plt.scatter(labels, X)
    plt.title('Number of Tags per File')
    plt.show()

    Y = [x[1] for x in to_plot]
    plt.bar(labels, Y)
    plt.scatter(labels, Y)
    plt.title('Average Repetition per Tag')
    plt.show()


input_file = "./hyper_parameter/res_hyper_d50000-0.txt"

def plot_hyper_parameters(input_file):
    file_plot = []
    with open(input_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            lines = line.strip().split()
            H_merge = int(lines[0])
            V_merge = int(lines[1])
            Number_of_checks_greedy_H = int(lines[2])
            Number_of_checks_greedy_V = int(lines[3])
            score_total = int(lines[4])
            total_time = lines[5]
            minutes, seconds, milliseconds = total_time.split(":")
            file_plot.append([H_merge, V_merge, Number_of_checks_greedy_H, Number_of_checks_greedy_V, score_total, int(minutes)*60 + int(seconds) + int(milliseconds)/1000])
    return file_plot

file_plot = plot_hyper_parameters(input_file)

# # Organizing data by Number_of_checks
# data_by_checks = {}
# for entry in file_plot:
#     checks = entry[2]  # Number_of_checks_greedy_H (or V)
#     if checks not in data_by_checks:
#         data_by_checks[checks] = []
#     data_by_checks[checks].append(entry)

# # Plotting H_merge vs. score_total for each Number_of_checks
# plt.figure(figsize=(10, 6))

# for checks, data in data_by_checks.items():
#     H_merges = [d[0] for d in data]
#     scores = [d[4] for d in data]
#     plt.plot(H_merges, scores, marker='o', label=f'Checks = {checks}')

# plt.xlabel('H_merge')
# plt.ylabel('Score Total')
# plt.title('H_merge and Score Total for Different Numbers of Checks file b')
# plt.legend()
# plt.grid(True)
# plt.show()

# # Plotting H_merge vs. time (in seconds) for each Number_of_checks
# plt.figure(figsize=(10, 6))

# for checks, data in data_by_checks.items():
#     H_merges = [d[0] for d in data]
#     times = [d[5] for d in data]
#     plt.plot(H_merges, times, marker='o', label=f'Checks = {checks}')

# plt.xlabel('H_merge')
# plt.ylabel('Time (seconds)')
# plt.title('H_merge and total time for Different Numbers of Checks file b')
# plt.legend()
# plt.grid(True)
# plt.show()



data_by_checks = defaultdict(list)
for entry in file_plot:
    H_check = entry[2]  # Number_of_checks_greedy_H
    V_check = entry[3]  # Number_of_checks_greedy_V
    data_by_checks[(H_check, V_check)].append(entry)

# Plotting H_merge vs. score_total for each (H_check, V_check)
plt.figure(figsize=(10, 6))

for (H_check, V_check), data in data_by_checks.items():
    H_merges = [d[1] for d in data]
    scores = [d[4] for d in data]
    label = f'H_check = {H_check}, V_check = {V_check}'
    plt.plot(H_merges, scores, marker='o', label=label)

plt.xlabel('H_merge')
plt.ylabel('Score Total')
plt.title('H_merge vs. Score Total for Different H_check and V_check')
plt.legend()
plt.grid(True)
plt.show()

# Plotting H_merge vs. time (in seconds) for each (H_check, V_check)
plt.figure(figsize=(10, 6))

for (H_check, V_check), data in data_by_checks.items():
    H_merges = [d[1] for d in data]
    times = [d[5] for d in data]
    label = f'H_check = {H_check}, V_check = {V_check}'
    plt.plot(H_merges, times, marker='o', label=label)

plt.xlabel('H_merge')
plt.ylabel('Time (seconds)')
plt.title('H_merge vs. Time for Different H_check and V_check')
plt.legend()
plt.grid(True)
plt.show()

# # Organizing data by Number_of_checks
# data_by_checks = {}
# for entry in file_plot:
#     checks = entry[3]  # Number_of_checks_greedy_H (or V)
#     if checks not in data_by_checks:
#         data_by_checks[checks] = []
#     data_by_checks[checks].append(entry)

# # Plotting H_merge vs. score_total for each Number_of_checks
# plt.figure(figsize=(10, 6))

# for checks, data in data_by_checks.items():
#     V_merges = [d[1] for d in data]
#     scores = [d[4] for d in data]
#     plt.plot(V_merges, scores, marker='o', label=f'Checks = {checks}')

# plt.xlabel('V_merge')
# plt.ylabel('Score Total')
# plt.title('V_merge and Score Total for Different Numbers of Checks file e')
# plt.legend()
# plt.grid(True)
# plt.show()

# # Plotting H_merge vs. time (in seconds) for each Number_of_checks
# plt.figure(figsize=(10, 6))

# for checks, data in data_by_checks.items():
#     V_merges = [d[1] for d in data]
#     times = [d[5] for d in data]
#     plt.plot(V_merges, times, marker='o', label=f'Checks = {checks}')

# plt.xlabel('V_merge')
# plt.ylabel('Time (seconds)')
# plt.title('V_merge and total time for Different Numbers of Checks file e')
# plt.legend()
# plt.grid(True)
# plt.show()
