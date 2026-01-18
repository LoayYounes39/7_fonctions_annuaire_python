# test_add_contact.py

from contacts import ADD_CONTACT,SEARCH_CONTACT, sessions
from auth import *

# 1️⃣ Créer une session utilisateur simulée
sessions["token_test"] = {
    "username": "testuser",
    "role": "utilisateur"
}
#add pdu ----------------------------------------------------------------
# 2️⃣ Construire un PDU pour ajouter un contact
pdu = {
    "token": "token_test",
    "data": {
        "nom": "Dupont",
        "prenom": "Jean",
        "email": "jean.dupont@gmail.com",
        "telephone": "0600000000",
        "adresse": "Toulouse"
    }
}
# Vérification téléphone

pdu2 = {
    "token": "token_test",
    "data": {
        "nom": "Dupont2",
        "prenom": "Jean2",
        "email": "jean.dupont2@gmail.com",
        "telephone": "0600",
        "adresse": "Toulouse"
    }
}
# Vérification email
pdu3 = {
    "token": "token_test",
    "data": {
        "nom": "Dupont3",
        "prenom": "Jean3",
        "email": "jean.dupont3@com",
        "telephone": "0600",
        "adresse": "Toulouse"
    }
}
# Vérifier que le token est valide
pdu4 = {
    "token": "token",
    "data": {
        "nom": "Dupont3",
        "prenom": "Jean3",
        "email": "jean.dupont3@com",
        "telephone": "0600",
        "adresse": "Toulouse"
    }
}
#search pdu----------------------------------------------------------
pdu_search = {
    "token": "token_test",
    "data": {
        "email": "jean.dupont@gmail.com"
    }
}

pdu_search2 = {
    "token": "token_test",
    "data": {
        "email": "jean.dupont@test.com"
    }
}
pdu_search3 = {
    "token": "token_test",
    "data": {
        "email": ""
    }
}

#login-----------------------------------------------------------

pdu_login1 = {
     "token": "token_test",
     "data": {
     "username": "Loay",
     "password": "Lolo1122"
     }
}


pdu_login2 = {
     "token": "token_test",
     "data": {
     "username": "Loay",
     "password": "Lolo1133"
     }
}


#logout----------------------------------------------------------

pdu_logout1 = {
     "token": "null",
     "data": {
     "username": "Loay",
     "password": "Lolo1133"
     }
}

pdu_logout2 = {
     "token": "token_test",
     "data": {
     "username": "Loay",
     "password": "Lolo1133"
     }
}

#add test---------------------------------------------------------------------------------
print("ce fichier test montre les messages de resultats des tests des fonction utilisées \n")
print("=== ADD_CONTACT ===")
#  Appel de la fonction ADD_CONTACT
#nouveau contact
print("test nouveau contact ")
reponse = ADD_CONTACT(pdu)
print(reponse["message"])
print("\n")

#contact existant:
print("test ajout contact exisrtant:")
reponse = ADD_CONTACT(pdu)
print(reponse["message"])
print("\n")

# Vérification téléphone
print("test vérification téléphone:")
reponse = ADD_CONTACT(pdu2)
print(reponse["message"])
print("\n")

# Vérification email
print("test vérification de mail:")
reponse = ADD_CONTACT(pdu3)
print(reponse["message"])
print("\n")

# Vérifier que le token est valide
# Vérification email
print("test vérification de token(authentification):")
reponse = ADD_CONTACT(pdu4)
print(reponse["message"])
print("\n")
#search test-------------------------------------------------------
print("\n=== SEARCH_CONTACT ===\n")

#test contact trouvé
print("test de recherche d'un contact trouvé:")
reponse_search = SEARCH_CONTACT(pdu_search)
print(reponse_search['message'])
print("\n")

#contact non trouvé
print("test de recherche d'un contact non trouvé:")
reponse_search = SEARCH_CONTACT(pdu_search2)
print(reponse_search['message'])
print("\n")

#requete invalide
print("test de recherche d'un contact non trouvé:")
reponse_search = SEARCH_CONTACT(pdu_search3)
print(reponse_search['message'])
print("\n")

#login valide
print("test login valide")
reponse_login = LOGIN(pdu_login1, "users.csv")
print(reponse_login['message'])

#login invalide

print("test login invalide, mot de passe incorrect")
reponse_login = LOGIN(pdu_login2, "users.csv")
print(reponse_login['message'])

#logout invalide (sans token de session)
print("logout invalide (sans token de session)")
reponse_logout = LOGOUT(pdu_logout1)
print(reponse_logout['message'])
     
#logout valide (avec token de session)
print("logout valide avec token de session ")
reponse_logout = LOGOUT(pdu_logout2)
print(reponse_logout['message'])     
     









