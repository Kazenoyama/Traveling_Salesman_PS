# plt.pie(word_counts.values(), labels=word_counts.keys(), labeldistance=1.15, autopct='%1.1f%%')
# plt.title("b_lovely_landscapes")
# plt.show()

# data_size, lines = readFiles("./hashcode/d_pet_pictures.txt")
# word_counts = count_H_V_occurence(lines)
# print(word_counts)
# plt.pie(word_counts.values(), labels=word_counts.keys(), labeldistance=1.15,wedgeprops={"linewidth": 3, "edgecolor": "white"}, autopct='%1.1f%%')
# plt.title("d_pet_pictures")
# plt.show()

# data_size, lines = readFiles("./hashcode/e_shiny_selfies.txt")
# word_counts = count_H_V_occurence(lines)
# print(word_counts)
# plt.pie(word_counts.values(), labels=word_counts.keys(), labeldistance=1.15,wedgeprops={"linewidth": 3, "edgecolor": "white"}, autopct='%1.1f%%')
# plt.title("e_shiny_selfies")
# plt.show()

# average = []
# for i in range(0,6):
#     if i == 0:
#         file = "./test/d00100-"
#     elif i == 1:
#         file = "./test/d01000-"
#     elif i == 2:
#         file = "./test/d05000-"
#     elif i == 3:
#         file = "./test/d10000-"
#     elif i == 4:
#         file = "./test/d25000-"
#     else:
#         file = "./test/d50000-"
    
#     make_average =[]
#     for j in range(0,5):
#         pathFile = file + str(j) + ".txt"
#         data_size, lines = readFiles(pathFile)
#         word_counts = count_H_V_occurence(lines)
#         make_average.append(word_counts)
#     avg_H = sum(d['H'] for d in make_average) / len(make_average)
#     avg_V = sum(d['V'] for d in make_average) / len(make_average)
#     average.append({"H": avg_H, "V": avg_V})

# print(average)

# labels = ['100', '1000', '5000', '10000', '25000', '50000']
# avg_H_values = [d['H'] for d in average]
# avg_V_values = [d['V'] for d in average]

# x = range(len(labels))

# fig, ax = plt.subplots()
# bar_width = 0.35
# bar1 = ax.bar(x, avg_H_values, bar_width, label='H')
# bar2 = ax.bar([p + bar_width for p in x], avg_V_values, bar_width, label='V')

# ax.set_xlabel('File size')
# ax.set_ylabel('Number of occurence')
# ax.set_title('Average H and V Counts by File Size')
# ax.set_xticks([p + bar_width / 2 for p in x])
# ax.set_xticklabels(labels)
# ax.legend()
# plt.show()


# # Calculate percentages
# avg_H_percentages = [d['H'] / (d['H'] + d['V']) * 100 for d in average]
# avg_V_percentages = [d['V'] / (d['H'] + d['V']) * 100 for d in average]

# fig, ax = plt.subplots()
# bar_width = 0.35
# bar1 = ax.bar(x, avg_H_percentages, bar_width, label='H %')
# bar2 = ax.bar([p + bar_width for p in x], avg_V_percentages, bar_width, label='V %')

# ax.set_xlabel('File size')
# ax.set_ylabel('Percentage')
# ax.set_title('Average H and V Percentages by File Size')
# ax.set_xticks([p + bar_width / 2 for p in x])
# ax.set_xticklabels(labels)
# ax.legend()
# plt.show()




