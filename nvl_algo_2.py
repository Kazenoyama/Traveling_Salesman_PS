import time

total_score = 0
nbr_lines = 0
H_merge = 500
V_merge = 500
Number_of_checks_greedy_H = 150
Number_of_checks_greedy_V = 150

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
    print("Scoring : ", file_path)
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
    

def scoring2(ligne1, ligne2):
    # print("Scoring : ", ligne1, ligne2)
    set1 = ligne1.strip().split()[3:]
    set2 = ligne2.strip().split()[3:]

    set1 = set(set1)
    set2 = set(set2)

    communs = len(set1 & set2)  # Intersection
    unique1 = len(set1 - set2)  # Uniques dans set1
    unique2 = len(set2 - set1)  # Uniques dans set2

        
    score_ligne = min(communs, unique1, unique2)

    return score_ligne


def process_file(input_path, output_path):
    global total_score, nbr_lines

    with open(input_path, 'r') as file:
        lines = file.readlines()

    h_lines = []
    v_lines = []

    # Séparation des lignes H et V, avec ajout des identifiants uniques
    for idx, line in enumerate(lines):
        line = line.strip()
        if line.startswith("H"):
            h_lines.append(f"{idx} {line}")
        elif line.startswith("V"):
            v_lines.append(f"{idx} {line}")

    # Tri des lignes H en ordre croissant par leur nombre avec approche gloutonne
    h_lines = process_h_lines_greedy(h_lines)

    # V
    if (len(v_lines) >= 2):
        v_lines = process_v_lines_greedy(v_lines)

        v_groups = []
        while len(v_lines) > 1:
            smallest = v_lines.pop(0)
            largest = v_lines.pop(-1)
            v_groups.append((smallest, largest))

        # Ajouter un groupe avec une seule ligne si une ligne reste
        #if v_lines:
            #v_groups.append((v_lines[0],))

        # Étape 2 : Ordonnancement glouton pour tous les petits groupes
        final_v_order = []
        all_lines = [
            (merge_v_group(group), group)
            for group in v_groups
        ]
        
        ordered_lines = []
        current_line = all_lines.pop(0)  # Initialisation avec le premier groupe
        nbr_lines += 1
        ordered_lines.append(current_line[1])


        while all_lines:
            
            total_score += scoring2(current_line[0][2:], all_lines[0][0][2:])
            nbr_lines += 1

            

            # Mise à jour des ordres
            current_line = all_lines.pop(0)
            ordered_lines.append(current_line[1])

        # Ajouter les lignes ordonnées au résultat final
        final_v_order.extend(ordered_lines)

        # Suppression des doublons dans final_v_order (au cas où)
        final_v_order = list(dict.fromkeys(final_v_order))
    else:
        final_v_order = []

    # Écriture dans le fichier de sortie
    with open(input_path, 'r') as file:
        lines = file.readlines()

    with open(output_path, 'w') as output_file:
        first_line = lines[0].strip()
        output_file.write(str(nbr_lines) + '\n')

        # Écriture des lignes H
        for h_line in h_lines:
            output_file.write(h_line.split()[0] + '\n')

        # Écriture des groupes V ordonnés
        for group in final_v_order:
            output_file.write(" ".join(line.split()[0] for line in group) + '\n')



def merge_v_group(group):
    """
    Combine les mots d'un groupe de lignes V en une seule ligne pour calculer le score.
    """
    group_sum = sum(int(line.split()[2]) for line in group)
    merged_words = set()
    for line in group:
        merged_words.update(line.split()[3:])
    return f"V {group_sum} " + " ".join(merged_words)


def process_h_lines_greedy(h_lines):
    global total_score, nbr_lines
    
    # Regrouper par numéro
    groups = {}
    for line in h_lines:
        key = int(line.split()[2])
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
        while len(current_group) < H_merge and i + 1 < len(sorted_groups):   # On merge les groupes si < à ... lignes dans ce groupe 500
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
        nbr_lines += 1
        ordered_group = [current_line]

        while all_lines:
            best_score = -1
            best_index = -1
            no_improvement_count = 0  # Compteur pour vérifier l'absence d'amélioration
            size = len(current_line)

            for index, line in enumerate(all_lines):
                score = calculate_score(current_line, line)
                if score > best_score:
                    best_score = score
                    best_index = index
                    no_improvement_count = 0  # Réinitialiser le compteur lorsque la condition est respectée
                else:
                    no_improvement_count += 1  # Incrémenter le compteur si la condition n'est pas respectée

                # Si le compteur atteint 50, sortir de la boucle for
                if no_improvement_count >= Number_of_checks_greedy_H | best_score >= size//2:
                    break
            
            total_score += scoring2(current_line, all_lines[best_index])
            nbr_lines += 1
            # Ajout de la meilleure ligne trouvée à la liste ordonnée
            current_line = all_lines.pop(best_index)
            ordered_group.append(current_line)


        ordered_lines += ordered_group

    return ordered_lines



def process_v_lines_greedy(v_lines):
    global total_score
    
    # Regrouper par numéro
    groups = {}
    for line in v_lines:
        key = int(line.split()[2])
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
        while len(current_group) < V_merge and i + 1 < len(sorted_groups):   # On merge les groupes si < à ... lignes dans ce groupe
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

        while all_lines:
            best_score = -1
            best_index = -1
            no_improvement_count = 0  # Compteur pour vérifier l'absence d'amélioration
            size = len(current_line)

            for index, line in enumerate(all_lines):
                score = calculate_score(current_line, line)
                if score > best_score:
                    best_score = score
                    best_index = index
                    no_improvement_count = 0  # Réinitialiser le compteur lorsque la condition est respectée
                else:
                    no_improvement_count += 1  # Incrémenter le compteur si la condition n'est pas respectée

                # Si le compteur atteint 50, sortir de la boucle for
                if no_improvement_count >= Number_of_checks_greedy_V | best_score >= size//2:
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
    words1 = set(line1.split()[3:])
    words2 = set(line2.split()[3:])
    communs = len(words1 & words2)
    return communs


# Utilisation de la fonction
# input_file = "c_memorable_moments.txt"
input_file = "b_lovely_landscapes.txt"
output_file = "res2.txt"
process_file(input_file, output_file)
# print(scoring("res2.txt"))
print(total_score)
