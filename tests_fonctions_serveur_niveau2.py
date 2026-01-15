from pathlib import Path
from fonctions_serveur_niveau2 import *


def test_user_exists():
    print("test_user_exists")
    #assert user_exists("Loay", "test1.csv") == True
    assert user_exists("thanina", "test1.csv") == False #Pas miniscule
    assert user_exists("Amir", "test1.csv") == False
    with open("test2.csv","x") as fichier:
        fichier = Path("test2.csv") 
        assert user_exists("Loay", "test2.csv") == False
        fichier.unlink() 
    print("test OK")

def test_add_user(): 
    print("test_add_user")
    add_user("Amir", "1234","client","test1.csv")
    assert user_exists("Amir", "test1.csv") == True
    assert user_exists("amir", "test1.csv") == False
    with open("test2.csv","x") as fichier: 
        add_user("loay","1234","client","test2.csv") #Nouveau_fichier
        assert user_exists("loay", "test2.csv") ==  True
        fichier = Path("test2.csv") 
        fichier.unlink()
    print("test OK")

if __name__ == "__main__":
    test_user_exists()
    test_add_user()
    
    