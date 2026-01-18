from auth import LOGIN
from users import creation_compte
from contacts import ADD_CONTACT, SEARCH_CONTACT, LIST_CONTACTS, DELETE_CONTACT
import os
from getpass import getpass
from auth import LOGOUT


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#  MENU ADMIN
# ============================================================

def menu_admin(token):
    while True:
        print("\n=== MENU ADMIN ===")
        print("1. Ajouter un utilisateur")
        print("2. Se déconnecter")
        print("3. Quitter")

        choix = input("Votre choix : ")

        if choix == "1":
            print("\n=== AJOUT UTILISATEUR ===")

            new_username = input("Nouveau username : ")
            new_password = getpass("Mot de passe : ")

            pdu_add_user = {
                "token": token,
                "data": {
                    "username": new_username,
                    "password": new_password,
                    "role": "utilisateur"
                }
            }

            # Appel de la fonction creation_compte()
            reponse = creation_compte(pdu_add_user)
            print("\nRéponse :", reponse["message"])

        elif choix == "2":
            pdu_logout = { "token": token }
            rep = LOGOUT(pdu_logout)
            print(rep["message"])
            main()
            break
        elif choix == "3":
            return

        else:
            print("Choix invalide.")


#-------------------------------------------------------------
def menu_user(token):
    while True:
        print("\n=== MENU UTILISATEUR ===")
        print("1. Ajouter un contact")
        print("2. Rechercher un contact")
        print("3. Supprimer un contact")
        print("4. Lister mes contacts")
        print("5. Se déconnecter")
        print("6. Quitter")
       

        choix = input("Votre choix : ")

        # 1️⃣ Ajouter un contact
        if choix == "1":
            print("\n=== AJOUT CONTACT ===")
            nom = input("Nom : ")
            prenom = input("Prénom : ")
            email = input("Email : ")
            telephone = input("Téléphone : ")
            adresse = input("Adresse : ")

            pdu_add = {
                "token": token,
                "data": {
                    "nom": nom,
                    "prenom": prenom,
                    "email": email,
                    "telephone": telephone,
                    "adresse": adresse
                }
            }

            rep = ADD_CONTACT(pdu_add)
            print("\nRéponse :", rep["message"])

        # 2️⃣ Rechercher un contact
        elif choix == "2":
            print("\n=== RECHERCHE CONTACT ===")
            email = input("Email du contact : ")

            pdu_search = {
                "token": token,
                "data": {
                    "email": email
                }
            }

            rep = SEARCH_CONTACT(pdu_search)
            print("\nRéponse :", rep["message"])

            if rep["status"] == 200:
                print("Nom :", rep["data"]["nom"])
                print("Prénom :", rep["data"]["prenom"])
                print("Email :", rep["data"]["email"])
                print("Téléphone :", rep["data"]["telephone"])
                print("Adresse :", rep["data"]["adresse"])

        # 3️⃣ Supprimer un contact
        elif choix == "3":
            print("\n=== SUPPRESSION CONTACT ===")
            email = input("Email du contact à supprimer : ")

            pdu_delete = {
                "token": token,
                "data": {
                    "email": email
                }
            }

            rep = DELETE_CONTACT(pdu_delete)
            print("\nRéponse :", rep["message"])

        # 4️⃣ Lister tous les contacts
        elif choix == "4":
            print("\n=== LISTE DES CONTACTS ===")

            pdu_list = {
                "token": token,
                "data": {}
            }

            rep = LIST_CONTACTS(pdu_list)
            print("\nRéponse :", rep["message"])

            if rep["status"] == 200 and rep["data"]["contacts"]:
                for c in rep["data"]["contacts"]:
                    print(f"- {c['nom']} {c['prenom']} ({c['email']})")
            else:
                print("Aucun contact.")
        elif choix == "5":
           pdu_logout = { "token": token }
           rep = LOGOUT(pdu_logout)
           print(rep["message"])
           main()
           break


        # 5️⃣ Quitter
        elif choix == "6":
            return
        else:
            print("Choix invalide.")



# ============================================================
#  MAIN
# ============================================================

def main():
    print("=== LOGIN ===")

    username = input("Username : ")
    password = getpass("Mot de passe : ")

    # Construire le PDU pour LOGIN
    pdu_login = {
        "data": {
            "username": username,
            "password": password
        }
    }

    # Appel de LOGIN
    users_path = os.path.join(BASE_DIR, "users.csv")
    rep = LOGIN(pdu_login, users_path)
    if rep["status"] == 404:
        print("Cet utilisateur n'existe pas.")
        choix = input("Voulez-vous créer un compte ? (oui/non) : ").strip().lower()

        if choix == "oui":
            new_password = getpass("Choisissez un mot de passe : ")

            # 🔹 Connexion automatique de l'admin
            pdu_admin_login = {
                "data": {
                    "username": "admin",
                    "password": "admin2004"
                }
            }

            rep_admin = LOGIN(pdu_admin_login, users_path)

            if rep_admin["status"] != 200:
                print("Erreur : impossible de connecter l'administrateur.")
                main()
                return

            admin_token = rep_admin["token"]

            # 🔹 Création du compte utilisateur avec le token admin
            pdu_create = {
                "token": admin_token,
                "data": {
                    "username": username,
                    "password": new_password,
                    "role": "utilisateur"
                }
            }

            rep_create = creation_compte(pdu_create)
            print(rep_create["message"])
            main()
            return
        else:
            print("Connexion annulée.")
            main()
            return


    print("\nRéponse LOGIN :", rep["message"])

    # Si login échoue
    if rep["status"] != 200:
        print("Échec de connexion.")
        return

    # Récupération des infos
    token = rep["token"]
    role = rep["data"]["role"]
    username = rep["data"]["username"]

    # Redirection selon le rôle
    if role == "administrateur":
        print("\n=== MODE ADMIN ===")
        menu_admin(token)

    else:
        print("\n=== MODE UTILISATEUR ===")
        # Tu ajouteras ton menu utilisateur ici
        # menu_user(username, token)
        menu_user(token)



if __name__ == "__main__":
    
    main()