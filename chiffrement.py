import os
import glob
import secrets
import string

def xor(block1, block2):
    longueur = min(len(block1), len(block2))
    xo = []

    for i in range(longueur):
        xo.append(block1[i] ^ block2[i])

    return bytes(xo)

def chiffrer(mot_claire, iv, cle):

    #on passe en binaire 
    mot_claire = mot_claire.encode()
    iv = iv.encode()
    cle = cle.encode()
    taille = len(iv)
    bloc_precedant = iv
    mot_chiffre = b""
    
    for i in range(0, len(mot_claire), taille):
        #decoupage en bloc 
        bloc = mot_claire[i:i+taille]

        #rajout de caractère si les blocs sont trop petits 
        if len(bloc)< taille : 
            bloc += b' '

        #chiffrement 
        bloc_xor = xor(bloc, bloc_precedant)
        bloc_chiffrer = xor(bloc_xor, cle)
        mot_chiffre += bloc_chiffrer
        bloc_precedant = bloc_chiffrer

    
    return mot_chiffre.hex()

    
    
def dechiffrer(mot_chiffre, iv, cle):
    mot_chiffre = bytes.fromhex(mot_chiffre)
    iv = iv.encode()
    cle = cle.encode()
    bloc_precedant = iv
    taille = len(iv)
    mot_claire = b""

    for i in range(0, len(mot_chiffre), taille):
        # Découpage en blocs
        bloc = mot_chiffre[i:i+taille]

        # Déchiffrement
        bloc_de_xor = xor(bloc, cle)            
        mot_de_xor = xor(bloc_de_xor, bloc_precedant)  
        mot_claire += mot_de_xor

        # Mettre à jour bloc_precedant avec le bloc chiffré actuel
        bloc_precedant = bloc

    return mot_claire.decode().strip()  

def trouver_index_fichier(dossier):
    fichiers_existants = glob.glob(f"{dossier}Resultat_*.txt")
    if not fichiers_existants:
        return 0  # Aucun fichier existant
    indices = [int(f.split("_")[1].split(".")[0]) for f in fichiers_existants]
    return max(indices) + 1  # Trouve le prochain index disponible


def gen_iv_cle(taille):
    
    caracteres = string.ascii_letters + string.digits
    iv = ''.join(secrets.choice(caracteres) for _ in range(taille))
    cle = ''.join(secrets.choice(caracteres) for _ in range(taille))


    return iv, cle

#iv = "1234"
#cle = "abcd"


def main():
    

    print("Bienvenu\nMon programme permet de chiffrer un mot/un phrase/un texte\n")
    print("***************************************************************************\n")
    print("Pour chiffrer tapez '1'.\nPour dechiffrer Tapez '2'\npour quiter le programme tapez 'Sorti'\n")
    while 1==1: 
         
        
        dossier = "./resultat/"
        if not os.path.exists(dossier):
            os.makedirs(dossier)
        index = trouver_index_fichier(dossier)
        var = input("Votre choix : ")

        if var == "1" : 
            iv,cle = gen_iv_cle(16)
            print("\nPour chiffrer un message, il suffit de le taper si dessous. Votre message chiffre votre cle et votre IV seront stocke dans un fichier\n")
            message = input("Message : ")
            res = chiffrer(message,iv,cle)
            print("Mot chiffrer (⌐■_■) : ",res)
            print("IV utilise : ", iv)
            print("Cle utilise : ", cle)
            
            fichier = f"{dossier}Resultat_{index}.txt"
            with open(fichier,'w') as f :
                f.write(f"Message chiffré : {res}\nClé : {cle}\nIV : {iv}")
            
        
        
        elif var == "2" : 
            print("\nPour dechiffrer un message, il vous faut le message chiffre, l'iv et la cle ayant servi a chiffrer ce message. Ses information sont stocke dans un fichier\n")
            message = input("Message : ")
            ive = input("IV : ")
            clee = input("Cle : ")

            print(dechiffrer(message,ive,clee))

        elif var == "Sorti":
            break

        else : 
            print("\n!Commande indisponible!")


main()