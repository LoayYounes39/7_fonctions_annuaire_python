import csv
from fonctions_serveur_niveau2 import *
from dataclasses import dataclass
from typing import Dict, Optional


"""
Le module du serveur(niveau 1) a les 7 fonctions de différents actions faits quand le client choisit,
une action est faite niveau modification dans la base de donnée (les fichiers CSV), persistance 
...
"""

CURRENT_USER = "Loay"

# ----- Fonctions de commandes ------ 

def CREATE_USER(pdu_recu: PDU_Requete) -> PDU_Reponse:

    '''
    Args : 
    pdu_recu : le user (admin ou client) appelle la fonction avec cette pdu 
    Returns : 
    pdu_reponse : le user reçoit une réponse montrant l'action faite comme résultat 

    '''

    token = pdu_recu.token
    data = pdu_recu.data

    # Étape 1 : autorisation
    if not est_administrateur(token):
        return pdu_403(token, "administrateur requis")

    # Étape 2 : validation des données
    champs_obligatoires = ["username", "password", "role"]
    if sont_donnees_utilisateur_invalides(data, champs_obligatoires):
        return pdu_400(token)

    # Étape 3 : unicité de l'utilisateur
    if user_exists(data["username"], "users.csv"):
        return pdu_409(token, "utilisateur déjà existant")

    # Étape 4 : création
    with open(f"annuaire_{data['username']}.csv", "w"):
        try:
            nom = data["username"]
            mdp = data["password"]
            role = data["role"]
            nom_fic = 'users.csv'
            add_user(nom, mdp, role, nom_fic )
        except: 
           return pdu_500(token)
    # Étape 5 : succès
    return pdu_201(token, "utilisateur ajouté par succès")

def ADD_CONTACT(pdu_recu: PDU_Requete) -> PDU_Reponse: 

    '''
    Args : 
    pdu_recu : le user (client plus souvent mais ça peut être admin aussi) appelle la fonction avec cette pdu 
    Returns : 
    pdu_reponse : le user reçoit une réponse montrant l'action faite comme résultat 
    '''
    token = pdu_recu.token
    data = pdu_recu.data

    if token == "": 
        return pdu_401(token)
    
    if not verifier_champs_obligatoires(data): 
        return pdu_400(token)
    
    
    if not est_Annuaire_Partage(data, CURRENT_USER): 
        return pdu_403(token, f" Tu n'as pas accès à {data["nomAnnuaire"]}" )

    if contact_exists(data["adresseMail"], f"annuaire_{data["nomAnnuaire"]}.csv"): 
        return pdu_409(token, "contact déjà existant")
    
    try: 
        ajouter_contact(pdu_recu.data, f"annuaire_{data["nomAnnuaire"]}.csv" )
    except: 
        return pdu_500(token)
    
    return pdu_201(token, "contact ajouté par succès")
    