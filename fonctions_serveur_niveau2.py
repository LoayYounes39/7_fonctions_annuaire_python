import csv
from dataclasses import dataclass
from typing import Dict, Optional


"Le module de serveur niveau 2 a les différentes fonctions auxiliaires déclarées en serveur niveau 1 "

#Définition des types de PDU dans un style d'enregistrement en C 
#data et token sont des dictionnaires car ils ont des champs
@dataclass
class PDU_Requete:
    action: str
    data: Optional[Dict[str, str]]
    token: Optional[Dict[str, str]]

@dataclass
class PDU_Reponse:
    status: int
    message: str
    data: Optional[Dict[str, str]]
    token: Optional[Dict[str, str]]

# ------ Fonctions Utilitaires ------


def user_exists(username: str, filename: str) -> bool:
    """
    Vérifie si un utilisateur existe déjà dans le fichier users.csv
    Retourne True si trouvé, False sinon
    """
    try:
        with open(filename, mode="r", newline="") as fichier: 
            lecteur = csv.DictReader(fichier)
            for ligne in lecteur:
                print(ligne.get("username"))
                if ligne.get("username") == username:
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

    champs = ["username", "password", "role"]

    try:
        # Si le fichier existe, le curseur est placé à la fin
        with open(filename, mode="a", newline="") as fichier:
            writer = csv.DictWriter(fichier, fieldnames=champs)

            # Si le fichier est vide, écrire l'en-tête
            if fichier.tell() == 0:
                writer.writeheader()

            writer.writerow({
                "username": username,
                "password": password,
                "role": role
            })

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

def pdu_403(token):
    '''
    Erreur 403 Accès refusé
    '''
    return PDU_Reponse(
        status=403,
        message="Accès refusé : administrateur requis",
        data=None,
        token=token
    )

def pdu_409(token):
    '''
    Erreur 409 Conflit (utilisateur existant)
    '''
    return PDU_Reponse(
        status=409,
        message="Utilisateur déjà existant",
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
    if token is None:
        return False
    return token.get("role") == "administrateur"