from dataclasses import dataclass
from typing import Any, Dict, Optional

"""
Le module du serveur a les fonctions de différents actions faits quand le client choisit,
une action est faite niveau modification dans la base de donnée (les fichiers CSV), persistance 
...
"""

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

#Fonctions Utilitaires

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

#Fonctions de commandes 

def CREATE_USER(pdu_recu: PDU_Requete) -> PDU_Reponse:

    '''
    Args : 
    pdu_recu : le client appelle la fonction avec cette pdu 
    Returns : 
    pdu_reponse : le client reçoit une réponse montrant l'action faite comme résultat 

    '''

    token = pdu_recu["token"]
    data = pdu_recu["data"]

    # Étape 1 : autorisation
    if not est_administrateur(token):
        return pdu_403(token)

    # Étape 2 : validation des données
    champs_obligatoires = ["username", "password", "role"]
    if sont_donnees_utilisateur_invalides(data, champs_obligatoires):
        return pdu_400(token)

    # Étape 3 : unicité de l'utilisateur
    if user_exists(data["username"]):
        return pdu_409(token)

    # Étape 4 : création
    with open(f"annuaire_{data['username']}.csv", "w"):
        add_user(
            username=data["username"],
            password=data["password"],
            role=data["role"]
        )
    # Étape 5 : succès
    return PDU_Reponse(
        status=201,
        message="Utilisateur créé avec succès",
        data=None,
        token=token
    )


