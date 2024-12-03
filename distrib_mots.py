from collections import defaultdict

def count_word_occurrences(file_path, output_path):
   
    word_counts = defaultdict(lambda: {'H': 0, 'V': 0})
    
    # Lecture du fichier
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]  # Ignorer la première ligne (nombre total)

    # Comptage des mots
    for line in lines:
        parts = line.split()
        if len(parts) < 3:
            continue  # Ignorer les lignes mal formatées
        line_type = parts[0]  # 'H' ou 'V'
        words = parts[2:]  # Mots après le nombre
        for word in words:
            if line_type == 'H':
                word_counts[word]['H'] += 1
            elif line_type == 'V':
                word_counts[word]['V'] += 1

    # Écriture dans le fichier de sortie
    with open(output_path, 'w') as output_file:
        for word, counts in sorted(word_counts.items()):  # Trie alphabétique des mots
            output_file.write(f"{word} {counts['H']} {counts['V']}\n")



count_word_occurrences("./instances/e_shiny_selfies.txt", "res_distrib.txt")
