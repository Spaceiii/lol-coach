import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import lightgbm as lgb
import time
import warnings
import numpy as np

warnings.filterwarnings('ignore', category=UserWarning)

print("--- Démarrage de l'Entraînement des Modèles (Vectorisation Positionnelle) ---")

# --- 1. Chargement et Définition des Données de Test ---
try:
    df = pd.read_csv('data/draftVectorized_Positional.csv')
    X = df.drop(columns=['Blue_Win'])
    Y = df['Blue_Win']
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y,
        test_size=0.2,
        random_state=42,
        stratify=Y
    )
    print(f"   -> {len(df)} matchs chargés.")
    print(f"   -> Données d'entraînement : {len(X_train)} lignes (80%)")
    print(f"   -> Données de test : {len(X_test)} lignes (20%)")
except FileNotFoundError:
    print("\nERREUR : Le fichier 'draftVectorized_Positional.csv' est introuvable. Arrêt du script.")
    exit()

print("\nÉtape 1.5/5 : Calcul des Poids d'Échantillon pour la Régression Logistique...")

# 1. Calculer la fréquence d'apparition (count) pour chaque feature (Champion_Role)
feature_counts = X_train.abs().sum(axis=0)

# 2. Créer un poids pour chaque match dans l'ensemble d'entraînement (inversement proportionnel à la rareté)
# Le poids d'un match est la somme des fréquences d'apparition des 10 features qu'il contient.
# L'idée est que les matchs avec des features courantes (haute fréquence) aient plus de poids.
weights_train = X_train.apply(lambda row: np.sum(feature_counts[row.abs() == 1]), axis=1)

# Normaliser les poids pour éviter une magnitude trop grande
weights_train = weights_train / weights_train.mean()

print(f"   -> Poids d'échantillon calculés (Moyenne : {weights_train.mean():.2f})")


# --- 2. Stratégie 1 : Régression Logistique PONDÉRÉE (Score de Force Brute - WR_Base) ---
print("\nÉtape 2/5 : Entraînement de la Régression Logistique PONDÉRÉE pour le WR_Base...")
start_time_lr = time.time()

# Entraînement du modèle LR, utilisant maintenant les weights_train
lr_model = LogisticRegression(solver='liblinear', C=1.0, random_state=42, max_iter=1000)
lr_model.fit(X_train, Y_train, sample_weight=weights_train) # <<< MODIFICATION ICI

# Prédiction WR_Base
Y_proba_lr = lr_model.predict_proba(X_test)[:, 1]

accuracy_lr = accuracy_score(Y_test, lr_model.predict(X_test))
print(f"   -> Temps d'entraînement LR : {time.time() - start_time_lr:.2f} secondes")
print(f"   -> Précision (Accuracy) LR sur test : {accuracy_lr:.4f}")

# Extraction du Score de Force Brute (Beta)
champion_coeffs = pd.Series(lr_model.coef_[0], index=X_train.columns)
champion_coeffs = champion_coeffs.sort_values(ascending=False)

print("\n🏆 Score de Force Brute (Beta PONDÉRÉ - Top 5) :")
print(champion_coeffs.head(5).to_string())

# ... (Reste du code à partir de l'Étape 3 est réutilisé pour LGBM et l'analyse des scores)
# NOTE: Nous n'utilisons pas de pondération pour LGBM dans cet exemple car la correction du biais de la LR est prioritaire.
# LGBM utilise déjà des mécanismes robustes pour gérer les données.

best_lgbm_model = lgb.LGBMClassifier(lambda_l1=0.1, lambda_l2=0.0, learning_rate=0.05, max_depth=7, min_child_samples=79, n_estimators=654, num_leaves=21, random_state=42, n_jobs=-1, verbose=-1)
best_lgbm_model.fit(X_train, Y_train)
Y_proba_lgbm = best_lgbm_model.predict_proba(X_test)[:, 1]
final_accuracy_lgbm = accuracy_score(Y_test, best_lgbm_model.predict(X_test))


# --- 4. Détermination des Scores d'Interaction (Synergie/Contre) ---
# ... (Code de l'Étape 4 ici, il est correct) ...
print("\nÉtape 4/5 : Détermination du Score d'Interaction (Synergie/Contre)...")

score_interaction_par_match = Y_proba_lgbm - Y_proba_lr

results_df = X_test.copy()
results_df['WR_Base_LR'] = Y_proba_lr
results_df['WR_Reel_LGBM'] = Y_proba_lgbm
results_df['Score_Interaction'] = score_interaction_par_match
results_df['Resultat_Reel'] = Y_test

synergies = results_df.sort_values(by='Score_Interaction', ascending=False).head(5)
print("\n🌟 Top 5 des Drafts à forte Synergie (LGBM a prédit beaucoup mieux que la LR) :")
print(synergies[['WR_Base_LR', 'WR_Reel_LGBM', 'Score_Interaction', 'Resultat_Reel']].to_string())

counters = results_df.sort_values(by='Score_Interaction', ascending=True).head(5)
print("\n💔 Top 5 des Drafts à fort Contre (LGBM a prédit un WR bien plus faible que la LR) :")
print(counters[['WR_Base_LR', 'WR_Reel_LGBM', 'Score_Interaction', 'Resultat_Reel']].to_string())

print("\n--- Analyse Terminée ---")