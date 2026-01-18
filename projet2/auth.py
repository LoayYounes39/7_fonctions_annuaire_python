import csv
import hashlib
import os
import uuid

sessions = {}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def generer_token():
    return str(uuid.uuid4())

def fichier_users_vide(fichier_csv):
    if not os.path.exists(fichier_csv):
        return True
    with open(fichier_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for _ in reader:
            return False
    return True

def creer_admin_initial(fichier_csv):
    username = "admin"
    password = "admin2004"
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    with open(fichier_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "password_hash", "role"])
        writer.writerow([username, password_hash, "administrateur"])

def charger_utilisateurs(fichier_csv):
    utilisateurs = {}
    with open(fichier_csv, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for ligne in reader:
            utilisateurs[ligne["username"]] = {
                "password_hash": ligne["password_hash"],
                "role": ligne["role"]
            }
    return utilisateurs

def LOGIN(PDU_Recu, fichier_csv):
    from auth import sessions

    if fichier_users_vide(fichier_csv):
        creer_admin_initial(fichier_csv)

    username = PDU_Recu.get("data", {}).get("username")
    password = PDU_Recu.get("data", {}).get("password")

    if not username or not password:
        return {"status": 400, "message": "Champs manquants", "token": "", "data": {}}

    utilisateurs = charger_utilisateurs(fichier_csv)
    if username not in utilisateurs:
        return {"status": 404, "message": "Username invalide", "token": "", "data": {}}

    hash_saisi = hashlib.sha256(password.encode()).hexdigest()
    if utilisateurs[username]["password_hash"] != hash_saisi:
        return {"status": 401, "message": "Mot de passe invalide", "token": "", "data": {}}

    token = generer_token()
    sessions[token] = {
        "username": username,
        "role": utilisateurs[username]["role"]
    }

    return {
        "status": 200,
        "message": "Connexion réussie",
        "token": token,
        "data": {
            "username": username,
            "role": utilisateurs[username]["role"]
        }
    }
def LOGOUT(PDU_Recu: dict) -> dict:
    """
    Déconnecte un utilisateur en supprimant son token de la session.
    """

    PDU_Reponse = {
        "status": None,
        "message": "",
        "token": "",
        "data": {
            "username": None,
            "role": None
        }
    }

    token = PDU_Recu.get("token")

    # Vérifier que le token existe
    if token not in sessions:
        PDU_Reponse["status"] = 401
        PDU_Reponse["message"] = "Non authentifié"
        return PDU_Reponse

    # Supprimer la session
    del sessions[token]

    PDU_Reponse["status"] = 200
    PDU_Reponse["message"] = "Déconnexion réussie"
    return PDU_Reponse
