def correct_form(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        try:
            n = int(lines[0].strip())
        except ValueError:
            return False
        
        # n lignes après la première
        if len(lines[1:]) != n:
            return False
        
        # Vérifier le format des n lignes restantes
        for line in lines[1:]:
            parts = line.strip().split()
            if len(parts) < 3:
                return False
            
            # H ou V
            if parts[0] not in {'H', 'V'}:
                return False
            
            # ensuite un int
            try:
                m = int(parts[1])
            except ValueError:
                return False
            
            # m mots après le int
            if len(parts[2:]) != m:
                return False
        
        return True  # valide
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return False

def scoring(file_path):
    if correct_form(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Liste pour stocker les mots avec les doublons
        word_lists = []
        i = 1  # Commencer après la première ligne (nombre total)

        while i < len(lines):
            parts = lines[i].strip().split()
            line_type = parts[0]
            words = parts[2:]  # Extraire les mots

            if line_type == 'H':
                # Ajouter les mots directement pour les lignes H
                word_lists.append(words)  # Liste pour conserver les doublons
                i += 1
            elif line_type == 'V':
                # Regrouper deux lignes V consécutives
                current_list = words[:]
                if i + 1 < len(lines) and lines[i + 1].startswith('V'):
                    next_parts = lines[i + 1].strip().split()
                    next_words = next_parts[2:]
                    current_list.extend(next_words)  # Conserver les doublons
                    i += 1  # Sauter la deuxième ligne V
                word_lists.append(current_list)
                i += 1

        # calcul du score total
        #print(word_lists)
        score_total = 0
        for j in range(len(word_lists) - 1):
            #convertir en Counter pour gérer les doublons
            set1 = set(word_lists[j])
            set2 = set(word_lists[j + 1])

            communs = len(set1 & set2)  # Intersection
            unique1 = len(set1 - set2)  # Uniques dans set1
            unique2 = len(set2 - set1)  # Uniques dans set2

            #Score entre deux ensembles
            score_ligne = min(communs, unique1, unique2)
            score_total += score_ligne

        return score_total

    else:
        return "Fichier d'entrée pas de la bonne forme"

def process_file(input_path, output_path):
    with open(input_path, 'r') as file:
        lines = file.readlines()

    size = lines[0].strip()
    size = int(size)
    print(size)
    
    h_lines = []
    v_lines = []

    # Séparation des lignes H et V
    for line in lines:
        line = line.strip()
        if line.startswith("H"):
            h_lines.append(line)
        elif line.startswith("V"):
            v_lines.append(line)

    # Tri des lignes H en ordre croissant par leur nombre avec approche gloutonne
    h_lines = process_h_lines_greedy(h_lines)


    # V
    # Étape 1 : Regrouper par groupes de deux les V (le plus petit avec le plus grand)
    v_lines.sort(key=lambda x: int(x.split()[1]))
    v_groups = []
    while len(v_lines) > 1:
        smallest = v_lines.pop(0)
        largest = v_lines.pop(-1)
        v_groups.append((smallest, largest))

    # Ajouter un groupe avec une seule ligne si une ligne reste
    if v_lines:
        v_groups.append((v_lines[0],))

    # Étape 2 : Créer des groupes de groupes en fonction de la somme des chiffres
    grouped_v_groups = {}
    for group in v_groups:
        group_sum = sum(int(v.split()[1]) for v in group)
        if group_sum not in grouped_v_groups:
            grouped_v_groups[group_sum] = []
        grouped_v_groups[group_sum].append(group)

    # Étape 2.5 : Vérifier la taille des groupes et fusionner si nécessaire
    sorted_keys = sorted(grouped_v_groups.keys())  # Trier les clés pour un traitement séquentiel

    for i in range(len(sorted_keys) - 1):
        current_key = sorted_keys[i]
        next_key = sorted_keys[i + 1]
        
        # Calculer la taille totale des groupes actuels
        total_size = len(grouped_v_groups[current_key])
        
        print(size // 10)
        if total_size < size//10:                                                         # merge groupes si taille < ...
            # Déplacer les groupes actuels dans le groupe suivant
            grouped_v_groups[next_key].extend(grouped_v_groups[current_key])
            del grouped_v_groups[current_key]  # Supprimer le groupe déplacé

    # print(grouped_v_groups)

    # Étape 3 : Ordonnancement glouton au sein de chaque grand groupe
    final_v_order = []
    for group_sum, groups in sorted(grouped_v_groups.items()):
        all_lines = [
            (merge_v_group(group), group)
            for group in groups
        ]
        ordered_lines = []
        current_line = all_lines.pop(0)  # Initialisation avec le premier groupe
        ordered_lines.append(current_line[1])

        max_fail_count = 150                                                         # Limite pour les échecs consécutifs pour les V

        while all_lines:
            fail_count = 0  # Compteur d'échecs consécutifs
            best_score = -1
            best_index = -1
            best_group = None

            for index, (merged_line, group) in enumerate(all_lines):
                score = calculate_score(current_line[0], merged_line)
                if score > best_score:
                    best_score = score
                    best_index = index
                    best_group = group
                    fail_count = 0  # Réinitialiser le compteur en cas de succès
                else:
                    fail_count += 1  # Incrémenter le compteur en cas d'échec

                # Vérifier si la limite d'échecs est atteinte
                if fail_count > max_fail_count:
                    break

            # Mise à jour des ordres après la condition de ... échecs
            if fail_count > max_fail_count:
                current_line = all_lines.pop(best_index)  # Prendre le meilleur groupe trouvé jusque-là
                ordered_lines.append(current_line[1])    # Ajouter ce groupe à la liste ordonnée
                fail_count = 0  # Réinitialiser le compteur d'échecs
                continue  # Passer à l'itération suivante de la boucle while

            # Mise à jour des ordres
            current_line = all_lines.pop(best_index)
            ordered_lines.append(current_line[1])

        final_v_order.extend(ordered_lines)


    # Écriture dans le fichier de sortie
    with open(input_path, 'r') as file:
        lines = file.readlines()
    with open(output_path, 'w') as output_file:
        first_line = lines[0].strip()
        output_file.write(first_line + '\n')
        # Écriture des lignes H
        for h_line in h_lines:
            output_file.write(h_line + '\n')

        # Écriture des groupes V ordonnés
        for group in final_v_order:
            for line in group:
                output_file.write(line + '\n')

def merge_v_group(group):
    """
    Combine les mots d'un groupe de lignes V en une seule ligne pour calculer le score.
    """
    group_sum = sum(int(line.split()[1]) for line in group)
    merged_words = set()
    for line in group:
        merged_words.update(line.split()[2:])
    return f"V {group_sum} " + " ".join(merged_words)

def process_h_lines_greedy(h_lines):
    
    # Regrouper par numéro
    groups = {}
    for line in h_lines:
        key = int(line.split()[1])
        if key not in groups:
            groups[key] = []
        groups[key].append(line)

    # Convertir les groupes en une liste triée par clé
    sorted_groups = [(key, groups[key]) for key in sorted(groups.keys())]

    # Fusionner les groupes de petite taille avec les suivants
    merged_groups = []
    i = 0
    while i < len(sorted_groups):
        key, current_group = sorted_groups[i]
        while len(current_group) < 200 and i + 1 < len(sorted_groups):   # On merge les groupes si < à ... lignes dans ce groupe
            # Ajouter les lignes du groupe suivant au groupe actuel
            next_key, next_group = sorted_groups[i + 1]
            current_group = current_group + next_group
            i += 1  # Passer au groupe suivant après la fusion
        merged_groups.append((key, current_group))
        i += 1

    # Appliquer l'approche gloutonne sur chaque groupe fusionné
    ordered_lines = []
    for _, current_group in merged_groups:
        all_lines = current_group.copy()
        current_line = all_lines.pop(0)
        ordered_group = [current_line]

        limite_checks_H = 150                        # combien de checks max sans amélioration pour les H

        while all_lines:
            best_score = -1
            best_index = -1
            best_line = None
            no_improvement_count = 0  # Compteur pour vérifier l'absence d'amélioration

            for index, line in enumerate(all_lines):
                score = calculate_score(current_line, line)
                if score > best_score:
                    best_score = score
                    best_index = index
                    best_line = line
                    no_improvement_count = 0  # Réinitialiser le compteur lorsque la condition est respectée
                else:
                    no_improvement_count += 1  # Incrémenter le compteur si la condition n'est pas respectée

                # Si le compteur atteint 50, sortir de la boucle for
                if no_improvement_count >= limite_checks_H:
                    break

            # Ajout de la meilleure ligne trouvée à la liste ordonnée
            current_line = all_lines.pop(best_index)
            ordered_group.append(current_line)


        ordered_lines += ordered_group

    return ordered_lines

def calculate_score(line1, line2):
    """
    Calcule le score entre deux lignes (H ou V).
    """
    if isinstance(line1, str):  # Ligne simple
        words1 = set(line1.split()[2:])
    else:  # Ligne combinée
        words1 = set(line1.split()[2:])
    if isinstance(line2, str):  # Ligne simple
        words2 = set(line2.split()[2:])
    else:  # Ligne combinée
        words2 = set(line2.split()[2:])
    communs = len(words1 & words2)
    unique1 = len(words1 - words2)
    unique2 = len(words2 - words1)
    return min(communs, unique1, unique2)

# Utilisation de la fonction
input_file = "./c_memorable_moments.txt"
# input_file = "./e_shiny_selfies.txt"
# input_file = "./b_lovely_landscapes.txt"
output_file = "res2.txt"
process_file(input_file, output_file)
print(scoring("res2.txt"))