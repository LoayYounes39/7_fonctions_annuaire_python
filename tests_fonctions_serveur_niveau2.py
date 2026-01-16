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
    assert(est_administrateur({"role":None}) == False)
    assert(est_administrateur({"role":"administrateur"} ) == True)
    print("test ok")

if __name__ == "__main__":
    test_add_user()
    test_user_exists()
    test_sont_donnees_utilisateur_invalides()
    test_est_administrateur()
    
    