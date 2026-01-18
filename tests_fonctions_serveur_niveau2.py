from pathlib import Path
from fonctions_serveur_niveau2 import *


def test_user_exists():
    print("test_user_exists")
    assert user_exists("Loay", "test2.csv") == True
    assert user_exists("thanina", "test2.csv") == False #Pas miniscule
    assert user_exists("Amir", "test2.csv") == False
    with open("test3.csv","x") as fichier:
        fichier = Path("test3.csv") 
        assert user_exists("Loay", "test3.csv") == False
        fichier.unlink() 
    print("test OK")

def test_add_user(): 
    print("test_add_user")
    add_user("Amir", "1234","client","test1.csv")
    assert user_exists("Amir", "test1.csv") == True
    assert user_exists("amir", "test1.csv") == False
    with open("test3.csv","x") as fichier: 
        add_user("loay","1234","client","test3.csv") #Nouveau_fichier
        assert user_exists("loay", "test3.csv") ==  True
        fichier = Path("test3.csv") 
        fichier.unlink()
    print("test OK")

def test_sont_donnees_utilisateur_invalides(): 
    print("test utilisateurs_invalides")
    assert(sont_donnees_utilisateur_invalides({"username":"Loay","role":"client"},
                                              {"username","password","role"}) == True)
    assert(sont_donnees_utilisateur_invalides({"username":"Loay","password":"","role":"client"},
                                              {"username","password","role"}) == True)
    assert(sont_donnees_utilisateur_invalides({"username":"Loay","password":None,"role":"client"},
                                              {"username","password","role"}) == True)
    assert(sont_donnees_utilisateur_invalides({"username":"Loay","password":"123","role":"client"},
                                              {"username","password","role"}) == False)
    print("test OK")

def test_est_administrateur(): 
    print("test_est_administrateur")
    assert(est_administrateur(None) == False)
    assert(est_administrateur("ADMIN_TOKEN") == True)
    print("test ok")

def test_est_Annuaire_Partage(): 
    print("test_est_Annuaire_Partage")
    pdu1 = PDU_Requete("ADD_CONTACT", {"nomAnnuaire": "B"},"USER_TOKEN" )
    assert(est_Annuaire_Partage(pdu1.data, "Loay") == False )
    pdu2 = PDU_Requete("ADD_CONTACT", {"nomAnnuaire": "E"}, "USER_TOKEN")
    assert(est_Annuaire_Partage(pdu2.data, "Loay") == True )
    print("test ok")

def test_contact_exists():
    print("test_contact_exists")
    assert(contact_exists("emmatalley2016@gmail.com", "annuaire_Test.csv")) == True 
    assert(contact_exists("hassanshakoosh@nashaz.com", "annuaire_Test.csv")) == False
    print("test_ok")

def test_ajouter_contact(): 
    ajouter_contact({"nom": "Shakoosh", "prenom": "Hassan", "adresseMail": "hassanshakoosh@nashaz.com", 
                     "numTel": "012XXXXXXX", "adressePostale": "Camp Chizar" }, "annuaire_Test2.csv")
    assert(contact_exists("hassanshakoosh@nashaz.com", "annuaire_Test2.csv")) == True


if __name__ == "__main__":
    test_add_user()
    test_user_exists()
    test_sont_donnees_utilisateur_invalides()
    test_est_administrateur()
    test_est_Annuaire_Partage()
    test_contact_exists()
    test_ajouter_contact()
    
    