import csv
import hashlib
import os
from auth import sessions

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def creation_compte(pdu_recu):
    """
    Création d'un compte utilisateur (réservé à l'administrateur).
    """

    # Préparation du PDU réponse
    pdu_reponse = {
        "status": None,
        "message": "",
        "data": None,
        "token": pdu_recu.get("token")
    }
    token = pdu_recu.get("token")

    # 1️⃣ Vérifier l'authentification
    if token not in sessions:
        pdu_reponse["status"] = 401
        pdu_reponse["message"] = "Non authentifié"
        pdu_reponse["token"] = ""
        return pdu_reponse

    # 2️⃣ Vérifier le rôle administrateur
    if sessions[token]["role"] != "administrateur":
        pdu_reponse["status"] = 403
        pdu_reponse["message"] = "Accès refusé : administrateur requis"
        return pdu_reponse

    # 2. Vérifier la validité des données
    data = pdu_recu.get("data", {})
    username = data.get("username")
    password = data.get("password")
    role_new_user = data.get("role")

    if not username or not password or not role_new_user:
        pdu_reponse["status"] = 400
        pdu_reponse["message"] = "Données utilisateur invalides"
        return pdu_reponse

    # --- Chemins sécurisés ---
    users_path = os.path.join(BASE_DIR, "users.csv")
    annuaire_path = os.path.join(BASE_DIR, f"annuaire_{username}.csv")

    # 3. Vérifier si l'utilisateur existe déjà
    if os.path.exists(users_path):
        with open(users_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row and row[0] == username:
                    pdu_reponse["status"] = 409
                    pdu_reponse["message"] = "Utilisateur déjà existant"
                    return pdu_reponse

    # 4. Hacher le mot de passe
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # 5. Ajouter le nouvel utilisateur dans users.csv
        
    if not os.path.exists(users_path):
         with open(users_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["username", "password_hash", "role"])

    # 5bis. Ajouter le nouvel utilisateur
    with open(users_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([username, password_hash, role_new_user])


    # 6. Créer l'annuaire utilisateur
    if not os.path.exists(annuaire_path):
        with open(annuaire_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["nom", "prenom", "email", "telephone", "adresse"])

    # 7. Succès
    pdu_reponse["status"] = 201
    pdu_reponse["message"] = "Utilisateur créé avec succès"
    return pdu_reponse