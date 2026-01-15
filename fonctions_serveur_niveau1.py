import csv
from fonctions_serveur_niveau2 import *
from dataclasses import dataclass
from typing import Dict, Optional

"""
Le module du serveur(niveau 1) a les 7 fonctions de différents actions faits quand le client choisit,
une action est faite niveau modification dans la base de donnée (les fichiers CSV), persistance 
...
"""


# ----- Fonctions de commandes ------ 

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
    if user_exists(data["username"], "users.csv"):
        return pdu_409(token)

    # Étape 4 : création
    with open(f"annuaire_{data['username']}.csv", "w"):
        try:
            add_user(
            username=data["username"],
            password=data["password"],
            role=data["role"], 
            filename="users.csv"
        )
        except: 
            return PDU_Reponse(
            status=500,
            message="Erreur côté serveur",
            data=None,
            token=token
        ) 
    # Étape 5 : succès
    return PDU_Reponse(
        status=201,
        message="Utilisateur créé avec succès",
        data=None,
        token=token
    )


