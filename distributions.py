import matplotlib.pyplot as plt
from collections import Counter

def plot_distributions(file_path):
    """
    Lit un fichier d'entrée, extrait les nombres associés à 'H' et 'V',
    et trace un graphe des distributions séparées pour H (droite) et V (gauche).
    """
    # Lire le fichier et extraire les nombres associés à H et V
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]  # Ignorer la première ligne (nombre total)
    
    h_numbers = []
    v_numbers = []
    
    for line in lines:
        if line.startswith('H'):
            h_numbers.append(int(line.split()[1]))
        elif line.startswith('V'):
            v_numbers.append(int(line.split()[1]))
    
    # Compter les occurrences
    h_counts = Counter(h_numbers)
    v_counts = Counter(v_numbers)
    
    # Préparer les données pour le graphe
    h_keys, h_values = zip(*sorted(h_counts.items())) if h_counts else ([], [])
    v_keys, v_values = zip(*sorted(v_counts.items())) if v_counts else ([], [])
    
    # Créer les sous-graphiques
    fig, axes = plt.subplots(1, 2, figsize=(10, 6), sharey=True, gridspec_kw={'width_ratios': [1, 1]})
    
    # Graphique pour V
    axes[0].bar(v_keys, v_values, color='blue', alpha=0.7)
    axes[0].set_title("Distribution des nombres pour V")
    axes[0].set_xlabel("Nombres")
    axes[0].set_ylabel("Occurrences")
    
    # Graphique pour H
    axes[1].bar(h_keys, h_values, color='green', alpha=0.7)
    axes[1].set_title("Distribution des nombres pour H")
    axes[1].set_xlabel("Nombres")
    
    # Ajuster le graphique
    plt.tight_layout()
    plt.show()


plot_distributions("./e_shiny_selfies.txt")
