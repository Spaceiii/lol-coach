import pandas as pd
import numpy as np
import time

print("--- Démarrage du script de Vectorisation POSITIONNELLE ---")

# --- 1. Lecture des Données Brutes ---
print("Étape 1/5 : Lecture du fichier matchData.csv...")
start_time = time.time()
try:
    df_match = pd.read_csv('data/matchData_Filtered.csv')
    print(f"   -> {len(df_match)} lignes (matchs) lues avec succès.")
except FileNotFoundError:
    print("Erreur : Assurez-vous que le fichier 'matchData.csv' est bien présent dans le dossier 'data/'")
    exit()  # Arrête le script si le fichier n'est pas trouvé

if not df_match.empty:

    # --- 2. Identification des Combinaisons Uniques (Champion + Rôle) ---
    print("\nÉtape 2/5 : Identification des combinaisons Champion_Rôle...")

    champion_cols = [f'participant{i}ChampionName' for i in range(10)]
    # ASSUMPTION: We assume the role column is named 'participant{i}Role'. ADJUST IF NEEDED.
    role_cols = [f'participant{i}IndividualPosition' for i in range(10)]

    unique_features = set()

    # Itérer sur les 10 participants pour extraire toutes les combinaisons uniques Champion_Role
    for i in range(10):
        champ_name_col = f'participant{i}ChampionName'
        role_col = f'participant{i}IndividualPosition'  # <<< VERIFIEZ CE NOM DE COLONNE

        if champ_name_col in df_match.columns and role_col in df_match.columns:
            # Créer une nouvelle colonne temporaire combinant ChampionName et Role
            combined_series = df_match[champ_name_col].astype(str) + '_' + df_match[role_col].astype(str)
            unique_features.update(combined_series.unique())

    # Suppression des éventuelles entrées "nan_nan" ou "nan_ROLE" si présentes dans les données
    list_features = sorted([f for f in list(unique_features) if f.split('_')[0] != 'nan'])
    num_features = len(list_features)

    print(f"   -> {num_features} caractéristiques uniques (Champion_Rôle) identifiées.")

    # --- 3. Initialisation du DataFrame Vectorisé ---
    print("\nÉtape 3/5 : Initialisation de la matrice de vectorisation positionnelle...")
    # Créer un nouveau DataFrame avec une colonne pour chaque feature + la colonne cible
    df_vectorized_pos = pd.DataFrame(0, index=df_match.index, columns=list_features)
    df_vectorized_pos['Blue_Win'] = 0
    print("   -> Matrice positionnelle initialisée.")

    # --- 4. Logique de Vectorisation (+1 / -1 / 0) ---
    print("\nÉtape 4/5 : Début de la vectorisation Champion_Camp_Rôle...")

    total_rows = len(df_match)
    progress_interval = max(1, total_rows // 10)

    for index, row in df_match.iterrows():

        # Affichage de la progression
        if index % progress_interval == 0 and index > 0:
            percent = (index / total_rows) * 100
            print(f"   -> Progression : {index}/{total_rows} ({percent:.0f}%)")

        # Déterminer si l'Équipe Bleue a gagné (Target Variable)
        blue_win = int(row['participant0Win']) if 'participant0Win' in row else 0
        df_vectorized_pos.loc[index, 'Blue_Win'] = blue_win

        for i in range(10):
            champ_name_col = f'participant{i}ChampionName'
            role_col = f'participant{i}IndividualPosition' 
            if champ_name_col in row and role_col in row:
                champ_name = row[champ_name_col]
                role_name = row[role_col]

                # Créer le nom de la colonne feature (ex: 'Zed_MID')
                feature_name = f"{champ_name}_{role_name}"

                # S'assurer que la feature existe et n'est pas un 'nan'
                if feature_name in df_vectorized_pos.columns:

                    # Déterminer le camp : participants 0-4 = Bleu (+1), 5-9 = Rouge (-1)
                    is_blue_team = i <= 4

                    if is_blue_team:
                        df_vectorized_pos.loc[index, feature_name] = 1
                    else:
                        df_vectorized_pos.loc[index, feature_name] = -1

    print(f"   -> Progression : {total_rows}/{total_rows} (100%) - Vectorisation positionnelle terminée.")

    # --- 5. Sauvegarde du Nouveau Dataset ---
    output_filename = 'data/draftVectorized_Positional.csv'
    print(f"\nÉtape 5/5 : Sauvegarde du DataFrame vectorisé sous '{output_filename}'...")
    df_vectorized_pos.to_csv(output_filename, index=False)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"\n✅ Succès : Le DataFrame vectorisé positionnellement a été créé en {elapsed_time:.2f} secondes.")
    print("------------------------------------------------------------------")
    print(f"Dimensions du dataset final : {len(df_vectorized_pos)} lignes x {len(df_vectorized_pos.columns)} colonnes.")
    print("Ce nouveau DataFrame est prêt pour un nouvel entraînement de modèles ML.")

else:
    print("\nLe script s'est terminé sans créer de fichier.")