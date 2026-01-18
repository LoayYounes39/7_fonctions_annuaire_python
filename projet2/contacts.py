import csv
import os
from auth import sessions



def email_valide(email):
    if "@" not in email:
        return False
    if " " in email:
        return False
    if email.count("@") != 1:
        return False

    local, domaine = email.split("@")

    if not local or not domaine:
        return False
    if "." not in domaine:
        return False
    if domaine.startswith(".") or domaine.endswith("."):
        return False

    return True

def numero_valide(telephone: str) -> bool:
    """
    Vérifie qu'un numéro de téléphone est valide :
    - uniquement des chiffres
    - exactement 10 chiffres
    - commence par 0
    """
    if not telephone.isdigit():
        return False

    if len(telephone) != 10:
        return False

    if not telephone.startswith("0"):
        return False

    return True



BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def ADD_CONTACT(PDU_Reçu: dict) -> dict:
    """
    Ajoute un contact dans l'annuaire d'un utilisateur.
    
    Paramètre :
        PDU_Reçu : dict contenant 'type', 'token', 'data' (avec 'nom', 'prenom', 'email', 'telephone', 'adresse')
    
    Retour :
        PDU_Réponse : dict avec 'status', 'message', 'token', 'data' (data vide pour ADD_CONTACT)
    """
    PDU_Réponse = {
        "status": None,
        "message": "",
        "token": PDU_Reçu.get("token", ""),
        "data": {  # Tous les champs mis à None pour rester conforme
            "username": None,
            "password": None,
            "role": None,
            "nom": None,
            "prenom": None,
            "email": None,
            "telephone": None,
            "adresse": None,
            "invite": None,
            "proprietaire": None,
            "filename": None,
            "contacts": None,
            "users": None
        }
    }

    # Vérifier que le token est valide
    session = sessions.get(PDU_Reçu.get("token"))
    if not session:
        PDU_Réponse["status"] = 401
        PDU_Réponse["message"] = "Non authentifié"
        return PDU_Réponse

    username = session["username"]
    data = PDU_Reçu.get("data", {})
    nom = data.get("nom")
    prenom = data.get("prenom")
    email = data.get("email")
    telephone = data.get("telephone", "")
    adresse = data.get("adresse", "")

    # Vérifier les champs obligatoires
    if not nom or not prenom or not email:
        PDU_Réponse["status"] = 400
        PDU_Réponse["message"] = "Données de contact invalides"
        return PDU_Réponse
    

    # Vérification email
    if not email_valide(email):
       PDU_Réponse["status"] = 400
       PDU_Réponse["message"] = "Email invalide"
       return PDU_Réponse


    # Vérification téléphone
    if not numero_valide(telephone):
       PDU_Réponse["status"] = 400
       PDU_Réponse["message"] = "Numéro de téléphone invalide"
       return PDU_Réponse



    # Vérifier si le contact existe déjà
    annuaire_file = os.path.join(BASE_DIR, f"annuaire_{username}.csv")
    if os.path.exists(annuaire_file):
        with open(annuaire_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["email"] == email:
                    PDU_Réponse["status"] = 409
                    PDU_Réponse["message"] = "Contact déjà existant"
                    return PDU_Réponse

    # Ajouter le contact
    file_exists = os.path.exists(annuaire_file)
    with open(annuaire_file, "a", newline="", encoding="utf-8") as f:
        fieldnames = ["nom", "prenom", "email", "telephone", "adresse"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists or os.stat(annuaire_file).st_size == 0:
            writer.writeheader()
        writer.writerow({
            "nom": nom,
            "prenom": prenom,
            "email": email,
            "telephone": telephone,
            "adresse": adresse
        })

    # Réponse succès
    PDU_Réponse["status"] = 201
    PDU_Réponse["message"] = "Contact ajouté avec succès"
    return PDU_Réponse
#--------------------------------------------------------------------------------------


def SEARCH_CONTACT(PDU_Reçu: dict) -> dict:
    """
    Recherche un contact dans l'annuaire de l'utilisateur.

    Paramètre :
        PDU_Reçu : dict contenant 'token' et 'data' avec 'email' du contact à rechercher

    Retour :
        PDU_Réponse : dict avec 'status', 'message', 'token', 'data' (infos du contact si trouvé)
    """
    # Initialisation du PDU de réponse
    PDU_Réponse = {
        "status": None,
        "message": "",
        "token": PDU_Reçu.get("token", ""),
        "data": {  # Tous les champs mis à None par défaut
            "username": None,
            "password": None,
            "role": None,
            "nom": None,
            "prenom": None,
            "email": None,
            "telephone": None,
            "adresse": None,
            "invite": None,
            "proprietaire": None,
            "filename": None,
            "contacts": None,
            "users": None
        }
    }

    # Vérifier que le token est valide
    session = sessions.get(PDU_Reçu.get("token"))
    if not session:
        PDU_Réponse["status"] = 401
        PDU_Réponse["message"] = "Non authentifié"
        PDU_Réponse["token"] = ""
        return PDU_Réponse

    username = session["username"]
    data = PDU_Reçu.get("data", {})
    email = data.get("email")

    # Vérifier que l'email est fourni
    if not email:
        PDU_Réponse["status"] = 400
        PDU_Réponse["message"] = "Requête invalide"
        return PDU_Réponse

    annuaire_file = os.path.join(BASE_DIR, f"annuaire_{username}.csv")

    if not os.path.exists(annuaire_file):
        # Si le fichier n'existe pas, aucun contact trouvé
        PDU_Réponse["status"] = 404
        PDU_Réponse["message"] = "Contact introuvable"
        return PDU_Réponse

    # Parcourir le CSV pour trouver le contact
    with open(annuaire_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["email"] == email:
                # Contact trouvé
                PDU_Réponse["status"] = 200
                PDU_Réponse["message"] = "Contact trouvé"
                PDU_Réponse["data"]["nom"] = row["nom"]
                PDU_Réponse["data"]["prenom"] = row["prenom"]
                PDU_Réponse["data"]["email"] = row["email"]
                PDU_Réponse["data"]["telephone"] = row.get("telephone")
                PDU_Réponse["data"]["adresse"] = row.get("adresse")
                return PDU_Réponse

    # Contact non trouvé
    PDU_Réponse["status"] = 404
    PDU_Réponse["message"] = "Contact introuvable"
    return PDU_Réponse

#---------------------------------------------------------------------------------
def LIST_CONTACTS(PDU_Reçu: dict) -> dict:
    """
    Liste tous les contacts de l'annuaire d'un utilisateur.

    Paramètre :
        PDU_Reçu : dict contenant 'token' et 'data' (vide ici)

    Retour :
        PDU_Réponse : dict avec 'status', 'message', 'token', 'data.contacts' (liste des contacts)
    """
    # Initialisation du PDU de réponse
    PDU_Réponse = {
        "status": None,
        "message": "",
        "token": PDU_Reçu.get("token", ""),
        "data": {
            "username": None,
            "password": None,
            "role": None,
            "nom": None,
            "prenom": None,
            "email": None,
            "telephone": None,
            "adresse": None,
            "invite": None,
            "proprietaire": None,
            "filename": None,
            "contacts": None,
            "users": None
        }
    }

    # Vérifier que le token est valide
    session = sessions.get(PDU_Reçu.get("token"))
    if not session:
        PDU_Réponse["status"] = 401
        PDU_Réponse["message"] = "Non authentifié"
        PDU_Réponse["token"] = ""
        return PDU_Réponse

    username = session["username"]
    annuaire_file = os.path.join(BASE_DIR, f"annuaire_{username}.csv")

    # Vérifier si le fichier existe
    if not os.path.exists(annuaire_file):
        PDU_Réponse["status"] = 204
        PDU_Réponse["message"] = "Aucun contact dans l’annuaire"
        PDU_Réponse["data"]["contacts"] = []
        return PDU_Réponse

    contacts = []
    with open(annuaire_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            contacts.append({
                "nom": row.get("nom"),
                "prenom": row.get("prenom"),
                "email": row.get("email"),
                "telephone": row.get("telephone"),
                "adresse": row.get("adresse")
            })

    # Si l'annuaire est vide
    if not contacts:
        PDU_Réponse["status"] = 204
        PDU_Réponse["message"] = "Aucun contact dans l’annuaire"
        PDU_Réponse["data"]["contacts"] = []
        return PDU_Réponse

    # Annuaire non vide
    PDU_Réponse["status"] = 200
    PDU_Réponse["message"] = "Liste des contacts"
    PDU_Réponse["data"]["contacts"] = contacts
    return PDU_Réponse
#-------------------------------------------------------------------    
def DELETE_CONTACT(PDU_Reçu: dict) -> dict:
    """
    Supprime un contact de l'annuaire d'un utilisateur.

    Paramètre :
        PDU_Reçu : dict contenant 'token' et 'data' avec 'email' du contact à supprimer

    Retour :
        PDU_Réponse : dict avec 'status', 'message', 'token', 'data' (toujours vide)
    """
    # Initialisation du PDU de réponse
    PDU_Réponse = {
        "status": None,
        "message": "",
        "token": PDU_Reçu.get("token", ""),
        "data": {  # Tous les champs mis à None par défaut
            "username": None,
            "password": None,
            "role": None,
            "nom": None,
            "prenom": None,
            "email": None,
            "telephone": None,
            "adresse": None,
            "invite": None,
            "proprietaire": None,
            "filename": None,
            "contacts": None,
            "users": None
        }
    }

    # Vérifier que le token est valide
    session = sessions.get(PDU_Reçu.get("token"))
    if not session:
        PDU_Réponse["status"] = 401
        PDU_Réponse["message"] = "Non authentifié"
        PDU_Réponse["token"] = ""
        return PDU_Réponse

    username = session["username"]
    data = PDU_Reçu.get("data", {})
    email = data.get("email")

    # Vérifier que l'email est fourni
    if not email:
        PDU_Réponse["status"] = 400
        PDU_Réponse["message"] = "Requête invalide"
        return PDU_Réponse

    annuaire_file = os.path.join(BASE_DIR, f"annuaire_{username}.csv")

    # Vérifier que le fichier existe
    if not os.path.exists(annuaire_file):
        PDU_Réponse["status"] = 404
        PDU_Réponse["message"] = "fichier introuvable"
        return PDU_Réponse

    # Lire tous les contacts et vérifier si l'email existe
    contacts = []
    contact_trouve = False
    with open(annuaire_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["email"] == email:
                contact_trouve = True  # On ne met pas ce contact dans la nouvelle liste
            else:
                contacts.append(row)

    if not contact_trouve:
        PDU_Réponse["status"] = 404
        PDU_Réponse["message"] = "Contact introuvable"
        return PDU_Réponse

    # Réécrire le fichier CSV sans le contact supprimé
    with open(annuaire_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["nom", "prenom", "email", "telephone", "adresse"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(contacts)

    # Réponse succès
    PDU_Réponse["status"] = 200
    PDU_Réponse["message"] = "Contact supprimé avec succès"
    return PDU_Réponse