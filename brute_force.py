from itertools import combinations

def calculate_score(line1, line2):
    """
    Calcule le score entre deux lignes (H ou regroupement de V).
    """
    words1 = set(line1.split()[3:])
    words2 = set(line2.split()[3:])
    communs = len(words1 & words2)
    uniques1 = len(words1 - words2)
    uniques2 = len(words2 - words1)
    return min(communs, uniques1, uniques2)

def group_v_lines(v_lines):
    """
    Regroupe toutes les combinaisons possibles de lignes V par deux.
    """
    grouped = []
    for pair in combinations(v_lines, 2):
        ids = f"{pair[0][0]} {pair[1][0]}"  # Identifiants des lignes regroupées
        words = pair[0][1] + pair[1][1]
        grouped.append((ids, words))
    return grouped

def generate_permutations(elements, current_permutation, used, results, max_combinations):
    """
    Génère toutes les permutations possibles à l'aide de boucles et backtracking.
    """
    if len(current_permutation) == len(elements):
        results.append(current_permutation[:])
        return len(results) >= max_combinations

    for i in range(len(elements)):
        if not used[i]:
            used[i] = True
            current_permutation.append(elements[i])
            if generate_permutations(elements, current_permutation, used, results, max_combinations):
                return True
            current_permutation.pop()
            used[i] = False

    return False

def brute_force(input_file, output_file, max_combinations):
    """
    Algorithme brute force pour maximiser les scores avec une limite de combinaisons.
    Lit l'entrée depuis un fichier et écrit la sortie dans un autre fichier.
    """
    # Lire le fichier d'entrée
    with open(input_file, "r") as f:
        lines = f.read().strip().split("\n")

    # Nombre de lignes
    num_lines = int(lines[0])

    # Récupérer les lignes restantes
    lines = lines[1:]

    h_lines = []
    v_lines = []
    identifiers = []

    # Sépare les lignes H et V
    for i, line in enumerate(lines):
        parts = line.split()
        identifiers.append(str(i))
        if parts[0] == "H":
            h_lines.append((str(i), parts[3:]))
        elif parts[0] == "V":
            v_lines.append((str(i), parts[3:]))

    # Regroupe les lignes V
    v_combinations = group_v_lines(v_lines)

    # Combine les lignes H et les regroupements de V
    all_lines = h_lines + v_combinations

    # Générer les permutations avec une limite
    results = []
    generate_permutations(all_lines, [], [False] * len(all_lines), results, max_combinations)

    # Teste chaque permutation
    max_score = -1
    best_order = None

    for perm in results:
        current_score = 0
        for i in range(len(perm) - 1):
            current_score += calculate_score(" ".join(perm[i][1]), " ".join(perm[i + 1][1]))

        if current_score > max_score:
            max_score = current_score
            best_order = perm

    # Construit le contenu du fichier de sortie
    output = []
    if best_order:
        output.append(str(len(best_order)))
        for line in best_order:
            output.append(line[0])  # Identifiant des lignes ou des regroupements

    # Écrit le résultat dans le fichier de sortie
    with open(output_file, "w") as f:
        f.write("\n".join(output))

    print(f"Meilleur score trouvé : {max_score}")

# Fichiers d'entrée et de sortie
input_file = "./b_instance/100/instance_100_number1.txt"
output_file = "res2.txt"

# Limite le nombre de combinaisons testées
max_combinations = 100000

# Exécute l'algorithme
brute_force(input_file, output_file, max_combinations)
