import csv
from dataclasses import dataclass
import hashlib
from typing import Dict, Optional


"Le module de serveur niveau 2 a les différentes fonctions auxiliaires déclarées en serveur niveau 1 "

#Définition des types de PDU dans des classes 
#car car cela correspond le plus au diagramme 
#aussi les data sont optionnels (peuvent être nul) => je me suis servi de GPT dans les classes

@dataclass
class PDU_Requete:
    action: str
    data: Optional[Dict[str, str]]
    token: str

@dataclass
class PDU_Reponse:
    status: int
    message: str
    data: Optional[Dict[str, str]]
    token: str

# ------ Fonctions Utilitaires ------


def user_exists(username: str, filename: str) -> bool:
    """
    Vérifie si un utilisateur existe déjà dans le fichier users.csv
    Retourne True si trouvé, False sinon
    """
    try:
        with open(filename, mode="r", encoding='utf-8') as fichier: 
            lecteur = csv.DictReader(fichier)
            for ligne in lecteur:
                if ligne['username'] == username:
                    return True
    except FileNotFoundError:
        print("Fichier " + filename + " pas trouvé")
        # Si le fichier n'existe pas encore, aucun utilisateur n'existe
        return False
    return False


def add_user(username: str, password: str, role: str, filename: str) -> None:
    """
    Ajoute un utilisateur dans le fichier users.csv
    """
    salt = 'u39'
    pwd_salt = password + salt 
    pwd_hashed = hashlib.sha256(pwd_salt.encode())
    try: 
        with open(filename, 'w+', encoding='utf-8') as f:
            writer = csv.writer(f)
            reader = csv.reader(f)
            rows = list(reader)
            if (len(rows) == 0):
                writer.writerow(('username', 'password', 'role'))
            writer.writerow((
                username,
                pwd_hashed.hexdigest(),
                role
            ))
    except Exception:
        # Laisser l'exception remonter vers CREATE_USER
        raise

def pdu_400(token):
    '''
    Erreur 400  Données invalides
    '''
    return PDU_Reponse(
        status=400,
        message="Données utilisateur invalides",
        data=None,
        token=token
    )

def pdu_403(token, message):
    '''
    Erreur 403 Accès refusé
    '''
    return PDU_Reponse(
        status=403,
        message="Accès refusé : " + message,
        data=None,
        token=token
    )

def pdu_409(token, message):
    '''
    Erreur 409 Conflit (utilisateur existant)
    '''
    return PDU_Reponse(
        status=409,
        message=message,
        data=None,
        token=token
    )

def pdu_500(token):
     return PDU_Reponse(
            status=500,
            message="Erreur côté serveur",
            data=None,
            token=token )

def pdu_201(token, message):
   return PDU_Reponse(
        status=201,
        message=message,
        data=None,
        token=token
    )

def sont_donnees_utilisateur_invalides(data, champs_obligatoires):
    if data is None:
        return True

    for champ in champs_obligatoires:
        if champ not in data:
            return True
        if data[champ] is None or data[champ] == "":
            return True

    return False

def est_administrateur(token):
    return token == "ADMIN_TOKEN"

def pdu_401(token): 
    """
    le message quand on ne sait pas qui se connecte
    """
    return PDU_Reponse(
        status=401,
        message="Non authentifié",
        data=None,
        token=token
    ) 

def verifier_champs_obligatoires(data): 
    return data["nom"] != "" and data["prenom"] != "" and data["adresseMail"] != "" and data["nomAnnuaire"] != ""

def est_Annuaire_Partage(data, current_user):
    nomAnnuaire = data["nomAnnuaire"]
    est_Permis = False
    with open("droits.csv", "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        #print("Colonnes disponibles:", reader.fieldnames)
        for ligne in reader:
           #print("Ligne:", ligne)  # Pour voir le contenu
            if ligne["utilisateur"] == nomAnnuaire:
                tab_permis = ligne["utilisateursPermis"].split(",")
                est_Permis = current_user in tab_permis
    return est_Permis