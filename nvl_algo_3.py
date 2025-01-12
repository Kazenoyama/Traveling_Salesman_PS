import io
import time

start_time = time.time()

score_total = 0
nbr_lines = 0

temps_accordé = 60      # Le nombre de secondes qu'on a pour faire tout tourner
ratio_quand_faire_gloutonne_pour_V = 0       #0.00034      #  nombre total de mots differents / nombre total de mots
combien_permutations_par_ligne_h_localsearch = 10000 # le nombre de permutations qu'on tente pour chaque ligne h (à partir de la fin)

def calculate_word_ratio_v_lines(input_file):
    """
    Calcule le rapport entre le nombre total de mots et le nombre total de mots différents
    uniquement pour les lignes commençant par 'V'.
    
    :param input_file: Chemin du fichier d'entrée
    :return: Rapport (float) entre le nombre total de mots et le nombre total de mots différents
             pour les lignes 'V'.
    """
    #with open(input_file, "r") as f:
    lines = input_file.read().strip().split("\n")
    
    # Extraire les lignes de contenu (en ignorant la première ligne)
    lines = lines[1:]
    
    total_words = 0
    unique_words = set()
    
    for line in lines:
        # Vérifier si la ligne commence par 'V'
        if line.startswith("V"):
            # Extraire les mots (en ignorant les 2 premières colonnes: type, nombre de mots)
            words = line.split()[2:]
            total_words += len(words)
            unique_words.update(words)
    
    # Calculer le rapport
    if len(unique_words) == 0:  # Éviter la division par zéro
        return 0.0
    return len(unique_words) / total_words

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
        #print(f"Erreur lors de la lecture du fichier : {e}")
        return False
 
def scoring(file_path):
    #print("Scoring : ", file_path)
    #with open(file_path, 'r') as file:
    lines = file_path.readlines()
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

def afficher_contenu_fichier(chemin_fichier):
    chemin_fichier.seek(0)
    try:
        #with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        for ligne in chemin_fichier:
            print(ligne, end='')  # Utilisation de end='' pour éviter les sauts de ligne supplémentaires
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{chemin_fichier}' est introuvable.")
    except Exception as e:
        print(f"Erreur : {e}")

def process_file(input_path, output_path):
    global nbr_lines, score_total

    
    lines = input_path.readlines()

    h_lines = []
    v_lines = []

    # Séparation des lignes H et V, avec ajout des identifiants uniques
    for idx, line in enumerate(lines):
        line = line.strip()
        if line.startswith("H"):
            h_lines.append(f"{idx-1} {line}")
        elif line.startswith("V"):
            v_lines.append(f"{idx-1} {line}")

    # Tri des lignes H en ordre croissant par leur nombre avec approche gloutonne
    h_lines = process_h_lines_greedy(h_lines)

    # V
    if (len(v_lines) >= 2):

        ratio = calculate_word_ratio_v_lines(input_path)
        #print(ratio)

        if (ratio < ratio_quand_faire_gloutonne_pour_V):    # on fait le greedy pour les V et on combine avec nouvelle technique
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
                

                nbr_lines += 1

                

                # Mise à jour des ordres
                current_line = all_lines.pop(0)
                ordered_lines.append(current_line[1])

            # Ajouter les lignes ordonnées au résultat final
            final_v_order.extend(ordered_lines)

            # Suppression des doublons dans final_v_order (au cas où)
            final_v_order = list(dict.fromkeys(final_v_order))

        else:                                               # sinon on accroche la ligne la + longue avec la + petite etc.
            v_lines.sort(key=lambda x: int(x.split()[2]))
            v_groups = []
            while len(v_lines) > 1:
                smallest = v_lines.pop(0)
                largest = v_lines.pop(-1)
                v_groups.append((smallest, largest))
            

            # Étape 2 : Créer des groupes de groupes en fonction de la somme des chiffres
            grouped_v_groups = {}
            for group in v_groups:
                group_sum = sum(int(v.split()[2]) for v in group)
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
                
                if total_size < V_merge:                                                         # merge groupes si taille < ...
                    # Déplacer les groupes actuels dans le groupe suivant
                    grouped_v_groups[next_key].extend(grouped_v_groups[current_key])
                    del grouped_v_groups[current_key]  # Supprimer le groupe déplacé
                    

            #print(grouped_v_groups)

            # Étape 3 : Ordonnancement glouton au sein de chaque grand groupe
            final_v_order = []
            for group_sum, groups in sorted(grouped_v_groups.items()):
                all_lines = [
                    (merge_v_group(group), group)
                    for group in groups
                ]
                ordered_lines = []
                current_line = all_lines.pop(0)  # Initialisation avec le premier groupe
                nbr_lines += 1
                ordered_lines.append(current_line[1])

                max_fail_count = Number_of_checks_greedy_V                                                         # Limite pour les échecs consécutifs pour les V

                while all_lines:
                    fail_count = 0  # Compteur d'échecs consécutifs
                    best_score = -1
                    best_index = -1

                    length = len(current_line[0])

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
                        if fail_count > max_fail_count | best_score >= length//2:
                            break

                    nbr_lines += 1
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

        # Ajouter un groupe avec une seule ligne si une ligne reste
        #if v_lines:
            #v_groups.append((v_lines[0],))

    else:
        final_v_order = []

    
    #local search
    end_time = time.time()
    temps_restant = temps_accordé - (end_time - start_time)
    h_lines = local_search_h_with_param(h_lines, combien_permutations_par_ligne_h_localsearch, temps_restant)


    # Écriture dans le fichier de sortie
    #with open(input_path, 'r') as file:
    lines = input_path.readlines()

    #with open(output_path, 'w') as output_file:
    afficher_contenu_fichier(input_path)
    #first_line = lines[0].strip()
    #output_file.write(str(nbr_lines) + '\n')
    print("")
    print(str(nbr_lines))
    
    last_line = None
    # Écriture des lignes H
    for h_line in h_lines:
        #output_file.write(h_line.split()[0] + '\n')
        print(h_line.split()[0])
        if (last_line != None):
            score_total += scoring2(h_line, last_line)
        last_line = h_line

    for group in final_v_order:
        # Combiner les lignes d'un groupe en fusionnant les mots
        combined_line = combine_v_group(group)
        #output_file.write(" ".join(line.split()[0] for line in group) + '\n')
        print(" ".join(line.split()[0] for line in group))

        # Calculer le score entre le groupe précédent et le groupe courant
        if last_line is not None:
            score_total += scoring2(combined_line, last_line)

        # Mettre à jour le dernier groupe traité
        last_line = combined_line

def combine_v_group(group):
    """
    Combine les mots de plusieurs lignes V dans un groupe.
    """
    # Extraire tous les mots des lignes du groupe après la 3e colonne
    all_words = set()
    for line in group:
        all_words.update(line.split()[3:])  # Ajouter les mots à l'ensemble
    
    # Construire la ligne combinée
    group_id = group[0].split()[0]  # ID du groupe (premier ID dans le tuple)
    combined_line = f"{group_id} V {len(all_words)} " + " ".join(sorted(all_words))
    return combined_line

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
    global nbr_lines
    
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
            
            nbr_lines += 1
            # Ajout de la meilleure ligne trouvée à la liste ordonnée
            current_line = all_lines.pop(best_index)
            ordered_group.append(current_line)


        ordered_lines += ordered_group

    return ordered_lines

def process_v_lines_greedy(v_lines):
    
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

def local_search_h_with_param(ordered_lines, n, tmps):
    """
    Optimise la position de la dernière ligne et des précédentes dans les `n` dernières lignes via une recherche locale.
    Évalue toutes les permutations possibles et garde celle qui maximise le score.
    
    Parameters:
        ordered_lines (list): Liste ordonnée des lignes.
        n (int): Portée pour permuter les dernières lignes avec les `n` lignes précédentes.
    """
    start_time_LS = time.time()
    global score_total

    # Index de la dernière ligne
    last_idx = len(ordered_lines) - 1

    # Limiter n pour éviter d'accéder à des indices négatifs
    n = min(n, len(ordered_lines) - 1)

    best_score = float('-inf')
    best_order = ordered_lines[:]

    # Parcours des lignes de l'avant-dernière ligne jusqu'à la deuxième ligne
    for j in range(last_idx - 1, n - 1, -1):  # j représente la ligne à tester, de l'avant-dernière vers la deuxième ligne
        # On initialise le meilleur score local pour cette ligne j
        local_best_score = float('-inf')
        local_best_order = ordered_lines[:]

        # Pour chaque ligne j, tester de permuter avec les n lignes avant lui
        for i in range(j - n, j):  # i est l'indice de la ligne à permuter avec la ligne j
            # Calculer le score avant permutation
            original_score = scoring2(ordered_lines[j], ordered_lines[j+1]) + scoring2(ordered_lines[j-1], ordered_lines[j])
            original_score += scoring2(ordered_lines[i], ordered_lines[i+1]) + scoring2(ordered_lines[i-1], ordered_lines[i])

            # Échanger les deux lignes (i et j)
            ordered_lines[i], ordered_lines[j] = ordered_lines[j], ordered_lines[i]

            # Calculer le score après permutation
            new_score = scoring2(ordered_lines[j], ordered_lines[j+1]) + scoring2(ordered_lines[j-1], ordered_lines[j])
            new_score += scoring2(ordered_lines[i], ordered_lines[i+1]) + scoring2(ordered_lines[i-1], ordered_lines[i])

            # Si la permutation améliore le score, on met à jour le meilleur score local et l'ordre des lignes
            if new_score > local_best_score:
                local_best_score = new_score
                local_best_order = ordered_lines[:]

            # Revenir à l'ordre initial pour tester la prochaine permutation
            ordered_lines[i], ordered_lines[j] = ordered_lines[j], ordered_lines[i]

        # Après avoir testé toutes les permutations pour cette ligne j, on met à jour l'ordre des lignes
        if local_best_score > best_score:
            best_score = local_best_score
            best_order = local_best_order

            # Appliquer la meilleure permutation pour cette itération
            ordered_lines = best_order[:]  # Mise à jour immédiate après chaque itération de j

            # Mise à jour du score_total après chaque itération de j
            score_total += best_score - original_score
        temps_ecroulé = time.time()

        if (tmps - (temps_ecroulé - start_time_LS) <= 0):
            break
    # Retourner l'ordre optimal des lignes
    return best_order

# Utilisation de la fonction
# input_file = "c_memorable_moments.txt"

def decideParameter(input_file, nameFile, time):
    global H_merge, V_merge, Number_of_checks_greedy_H, Number_of_checks_greedy_V, temps_accordé, ratio_quand_faire_gloutonne_pour_V, combien_permutations_par_ligne_h_localsearch
    #print(nameFile)
    onlyName = nameFile.split("/")[-1]
    #print(onlyName)
    if "b" in onlyName:
        H_merge = 500
        V_merge = 0
        Number_of_checks_greedy_H = 138
        Number_of_checks_greedy_V = 0
        temps_accordé = time
        ratio_quand_faire_gloutonne_pour_V = 0
        combien_permutations_par_ligne_h_localsearch = 10000
    elif "d" in onlyName:
        H_merge = 500
        V_merge = 500
        Number_of_checks_greedy_H = 138
        Number_of_checks_greedy_V = 115
        temps_accordé = time
        ratio_quand_faire_gloutonne_pour_V = 0
        combien_permutations_par_ligne_h_localsearch = 10000
    elif "e" in onlyName:
        H_merge = 0
        V_merge = 500
        Number_of_checks_greedy_H = 0
        Number_of_checks_greedy_V = 115
        temps_accordé = time
        ratio_quand_faire_gloutonne_pour_V = 0.00034
        combien_permutations_par_ligne_h_localsearch = 10000

    #with input_file as file:
    input_stream.seek(0)
    first_line = input_file.readline().strip()
    try:
        first_line_int = int(first_line)
        # print(f"The first line as integer: {first_line_int}")
        if first_line_int <= 1000:
            Number_of_checks_greedy_H = first_line_int
            Number_of_checks_greedy_V = first_line_int
            H_merge = first_line_int
            V_merge = first_line_int
        else:
            # print("The first line is greater than 1000.")
            if 'b' in onlyName:
                if first_line_int >= 50000 :
                    H_merge = first_line_int // 3
                    Number_of_checks_greedy_H = 120 * (temps_accordé //20)
                elif first_line_int >= 25000:
                    H_merge = first_line_int // 3
                    Number_of_checks_greedy_H = Number_of_checks_greedy_H * (temps_accordé // 11)
                elif first_line_int >= 10000:
                    H_merge = first_line_int // 3
                    Number_of_checks_greedy_H = Number_of_checks_greedy_H * (temps_accordé // 4)
                elif first_line_int >= 5000:
                    H_merge = first_line_int // 3
                    Number_of_checks_greedy_H = Number_of_checks_greedy_H * (temps_accordé // 3)

            elif 'd' in onlyName:
                if first_line_int >= 50000 :
                    H_merge = first_line_int // 3
                    V_merge = first_line_int // 3
                    Number_of_checks_greedy_H = Number_of_checks_greedy_H * (temps_accordé // 15)
                    Number_of_checks_greedy_V = Number_of_checks_greedy_V * (temps_accordé // 30)
                elif first_line_int >= 25000:
                    H_merge = first_line_int // 3
                    V_merge = first_line_int // 3
                    Number_of_checks_greedy_H = Number_of_checks_greedy_H * (temps_accordé // 7)
                    Number_of_checks_greedy_V = Number_of_checks_greedy_V * (temps_accordé // 15)
                elif first_line_int >= 10000:
                    H_merge = first_line_int // 3
                    V_merge = first_line_int // 3
                    Number_of_checks_greedy_H = Number_of_checks_greedy_H * (temps_accordé // 3)
                    Number_of_checks_greedy_V = Number_of_checks_greedy_V * (temps_accordé // 6)
                elif first_line_int >= 5000:
                    H_merge = first_line_int // 3
                    V_merge = first_line_int // 3
                    Number_of_checks_greedy_H = Number_of_checks_greedy_H * (temps_accordé // 2)
                    Number_of_checks_greedy_V = Number_of_checks_greedy_V * (temps_accordé // 3)

            elif 'e' in onlyName:
                if first_line_int >= 50000 :
                    V_merge = first_line_int // 3
                    Number_of_checks_greedy_V = Number_of_checks_greedy_V * (temps_accordé //30)
                elif first_line_int >= 25000:
                    V_merge = first_line_int // 3
                    Number_of_checks_greedy_V = Number_of_checks_greedy_V * (temps_accordé // 15)
                elif first_line_int >= 10000:
                    V_merge = first_line_int // 3
                    Number_of_checks_greedy_V = Number_of_checks_greedy_V * (temps_accordé // 6)
                elif first_line_int >= 5000:
                    V_merge = first_line_int // 3
                    Number_of_checks_greedy_V = Number_of_checks_greedy_V * (temps_accordé // 3)



    except ValueError:
        print("The first line is not a valid integer.")

    

def doTheFile(input_file,output_file, timeMax, input_file_name):
    global score_total
    start_time = time.time()
    
    decideParameter(input_file, input_file_name, timeMax)
    input_file.seek(0)
    #print("Parameters: ", H_merge, V_merge, Number_of_checks_greedy_H, Number_of_checks_greedy_V, temps_accordé, ratio_quand_faire_gloutonne_pour_V, combien_permutations_par_ligne_h_localsearch)
    process_file(input_file, output_file)
    input_file.seek(0)
    #print(score_total)
    score_total =0
    end_time = time.time()
    elapsed_time = end_time - start_time
    #print("Elapsed time: {:02}:{:02}:{:02}".format(int(elapsed_time // 3600), int((elapsed_time % 3600) // 60), int(elapsed_time % 60)))




#input_file = "./test/e00100-0.txt"
input_file_name = "d00100-1.txt"
content = """100
V 9 t34 t87 tc4 tm2 t37 ts2 tq6 tq1 tx
H 10 tq2 tz2 tw5 tq6 tm2 th5 tc4 tz6 t34 t52
V 6 tw3 t44 tc4 tq1 tw5 tp2
V 4 tf1 th tf tl1
V 13 t02 tb3 t52 t87 tq2 tz4 tq1 tc4 tf tr5 tk3 tc5 tk1
V 7 tw3 tl3 t05 tr1 tl5 tf1 tb7
V 14 tp6 t82 tl5 t52 t8 t94 tr2 tz6 th4 tn6 tb5 tr5 t47 tx2
V 10 th5 td4 tp6 tl5 tc5 th tv2 tx1 tw5 tk3
V 12 t05 td2 tn6 tw5 tq2 tb5 t37 tq6 t52 tq4 tc5 th6
V 5 tz2 tw5 tq6 tb6 t52
H 13 tb7 th5 tf1 t87 t72 td1 tq1 tr5 tz4 tl5 th6 tv2 t86
V 7 t51 tn6 t85 td2 t53 tq4 t75
H 14 t05 t02 tn6 t47 t01 t62 t37 t6 tg tm2 tr5 t34 th4 t87
H 3 tl2 t01 tp6
V 11 tc4 tz2 tq1 t86 t34 t6 tm2 tz tq5 tv2 tq6
V 7 tl5 tk1 td4 t52 tc4 t01 t05
V 13 tx2 tn3 tm2 th4 tf1 t47 tp3 td4 t34 tp2 t52 tz2 tz6
V 13 t85 tq2 tz6 tr3 tx4 t86 tj5 tx1 t8 t56 tr5 t93 tq6
V 9 t53 t86 ts2 tc5 tl5 t85 t02 tq1 tp6
V 3 th5 tl2 tx1
V 7 t02 tb7 th4 t86 th tz6 tx1
V 18 td4 tz6 tb5 tq2 tc4 tb7 tz tq3 t42 tv2 tl5 t8 tn6 th4 tm2 t05 tc5 t02
H 13 t82 t01 tb5 th5 t05 ts2 t47 t34 tq1 tm5 tb t53 tc4
V 6 t53 tc4 t74 tz2 t52 t34
V 13 t05 tz4 t94 tm5 t31 t86 tq6 tr5 t42 t85 tq1 t34 t82
H 9 tp6 tz2 t01 t53 t82 tz4 t31 td2 t05
V 14 th6 tf1 tc5 t52 tz5 t56 tf4 t47 t53 tl5 tw3 th tp2 th5
V 4 tv2 t87 t85 th6
V 3 t42 t74 t64
V 4 tx1 t87 tw3 t02
V 12 tz3 tf1 tv2 tc5 tk1 tq2 tk5 th6 t86 t47 t02 th5
V 14 t91 tm2 t87 tc4 tw3 tz4 tl2 th t86 tk1 tn6 tc5 t02 td4
V 15 tm tn6 t86 ts2 tz2 tc4 tx tc tc2 t94 t6 t53 t34 tb7 t44
H 10 tb5 td4 tp6 tf t82 th6 tp1 t86 th4 tz6
H 14 tp6 tx1 t02 tq2 tw4 tz6 tr2 th5 tm2 t56 t52 tc5 tw5 t87
H 3 tw1 tq2 th
H 13 t82 th6 t47 tc4 tj5 th5 ts2 tj4 tz4 tw6 t53 tn3 t34
H 9 tn1 tb5 tp2 t13 t02 t51 tl3 tx1 tf4
H 7 tc4 tw5 tl5 tz5 th5 t52 tp6
H 3 t82 tb2 t44
V 15 t82 tq6 t52 tp6 t85 tw3 t53 tf1 t87 tn3 tc1 tb5 tq1 tr6 t05
H 10 th t94 tm5 t01 t7 tc tp2 t47 t87 tl3
V 9 tc1 t52 tm2 td4 ts2 tn6 tk1 th5 tr5
V 13 tx2 tl5 t01 t61 tr5 tb7 t02 tf1 td4 tz3 th5 tm2 t47
V 5 tp2 tb5 tb7 tc4 tw5
H 10 ts2 tk1 td4 t34 tj3 t53 tc4 tp6 tz4 t05
H 10 td4 t12 tc5 tr5 t86 t34 tq6 td5 t94 tf1
V 9 th6 t05 t87 tw5 tr5 td4 tz6 th4 t86
V 10 tl t6 tf1 t02 tq1 t74 tv3 t01 t47 th6
V 14 t02 t82 t53 tc5 tw3 tp2 t01 t8 th5 tg6 tc2 tz4 t87 tm2
V 5 tq1 t46 t44 tc tz2
H 14 t6 t87 th6 tb6 t86 tn5 tz2 t02 t47 tx1 t61 th5 t34 tj4
V 9 t53 tz4 t82 tc5 t8 t05 t85 tj5 tf2
V 12 t74 tn6 t6 tb5 tm2 tn3 t85 t47 t05 t02 tl5 tw5
H 8 t56 tp2 tf2 tz2 t94 td4 t87 tm2
V 4 t86 tf2 ts2 t52
V 13 t87 tz6 tw3 tm2 tx2 t05 tb7 td4 tn6 t01 tq1 tr5 tp2
V 5 tc5 th4 tb7 ts2 t52
V 14 t94 tb7 tw3 td4 tm2 th5 tq6 t72 tj4 tx1 t91 tq1 t47 t26
V 5 th6 td1 t01 t33 tq3
V 10 t86 t52 tz6 t34 t51 tq2 tp6 tq6 t42 th4
V 5 t01 t53 t34 t42 t37
V 14 tl3 tf tp6 t86 t47 tp2 t01 tz6 t87 tq1 tc4 tm2 tw5 tb5
H 17 t56 tl5 t52 t86 t34 tr2 tz6 tr5 td6 tq6 th6 tw5 tp2 t61 t02 th5 t42
V 3 th5 tw3 th4
H 14 t57 t52 t51 th4 tp2 tc5 th6 tw3 t6 t05 tb5 tn3 tx4 tq1
V 7 tx t86 t8 tz4 tz2 tr6 th5
V 10 td4 t85 tc5 t52 t31 tj5 tz6 tq3 t93 t87
V 9 tz2 t47 t82 th6 tc1 t02 t86 ts2 tx1
V 6 t93 tx1 th6 tl5 t86 t53
V 7 t91 tz4 th6 tc3 tz6 t01 td4
V 3 tc5 th4 tp6
H 14 t01 tq6 tf1 th5 tb7 t05 tq1 tw3 t86 t87 ts4 th2 t6 tl2
V 4 t47 tq1 t87 tz6
H 17 th5 tz6 ts2 tz4 t6 t05 tq4 tl5 tq2 t86 th6 tq6 tc4 th4 tq3 tc1 tc5
H 15 t53 tw5 t47 tz4 tw4 tx1 th6 th4 tc5 tr1 tl4 t01 tp2 tq1 t87
H 7 t53 t2 tb7 tw th5 tb5 t87
V 13 td6 tq2 t61 tv4 tw5 tx tb5 t31 ts2 tp tq1 tw1 t87
V 5 t05 t74 t42 tf1 tr5
H 8 th5 tm tr6 t74 tl5 t52 tz2 tm2
V 7 tr5 td4 tz6 t87 tm2 t6 tl5
H 16 tz4 tb5 tn6 t6 tw3 tq2 th4 tw tc5 t02 t51 tc4 tl5 tr5 t32 t93
H 3 t85 t44 tz6
V 17 tc4 tf1 tz2 t51 t74 t93 tz4 th5 tq2 t87 th6 tq6 t75 tb5 tb1 tw4 t01
V 9 tz4 tp t21 tm5 t87 tp2 tx1 t6 tr6
H 14 tf1 tz6 th4 tl5 t6 tm5 tc tc5 tq2 tc4 tz2 tk3 t47 t37
V 12 tv3 th6 tn6 tc4 tp6 t82 tq2 td4 tk5 tj4 tm2 tq1
V 17 tc4 td4 t31 tq2 tl5 tr5 t3 tb5 tz6 tq1 t82 tf1 th4 t87 tw5 t47 tn6
H 5 td4 t47 tl5 t44 ts2
V 15 tn6 t05 td4 t22 t37 t34 tp6 tq1 tm5 tq6 tb tr5 tm2 t86 t53
V 3 tf1 tc5 tv3
V 10 ts2 t61 t87 tw2 tp2 tp6 t34 t53 t52 t91
V 12 t93 tc4 tw3 tb1 tv2 tl3 tz5 t01 t87 tl5 t44 tz2
V 12 t53 t85 tr5 t6 tb5 th6 tx1 tp6 t87 tf2 t82 t86
H 14 tc4 t52 tw5 t02 t01 tq2 tm2 t47 t86 tx1 tq6 t87 tl5 tb7
V 9 t02 th2 tq2 tq6 t86 tw5 ts4 tg2 t01
V 4 tp3 tr5 tq5 t01
V 6 t61 tq1 tz6 td4 tq2 tq3
V 5 tp6 tn6 tr5 t93 tb7
V 6 tc4 tc5 tx1 tr t22 tb5""" 

input_stream = io.StringIO(content)
# Écriture du contenu dans un fichier
#with open(input_file_name, "w") as file:
#    file.write(content.strip())

# Lecture et utilisation du fichier
#with open(input_file_name, "r") as file:
#    lines = file.readlines()

# Afficher les lignes lues
#for line in lines:
#    print(line.strip())

output_file = "res2.txt"
doTheFile(input_stream, output_file, 20, input_file_name)








