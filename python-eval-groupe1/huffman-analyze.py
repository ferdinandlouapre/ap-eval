import argparse
import json
from collections import Counter

parser = argparse.ArgumentParser()

parser.add_argument("texte", help="texte a encoder")
args = parser.parse_args()
nom_decod = args.texte
parser.add_argument("-c", "--coder", help="nom du fichier decodeur", default=nom_decod)
args = parser.parse_args()


with open(args.texte, "r") as f:
    texte = f.read().decode(
        "utf8"
    )  # on ajoute decode pour resoudre les problemes de UnicodeDecodeError
f.close()

c = Counter(texte)
compte = dict(c)


# Classe des elements de l'abre


class Arbre:
    def __init__(self, x):
        self.carac = x[0]
        self.freq = x[1]

    def pere(self, papa):
        self.pere = papa

    def fils0(self, fiston):
        self.fils0 = fiston

    def fils1(self, fiston):
        self.fils1 = fiston

    def code(self, bin):
        papa = self.pere
        self.code = papa.code + bin


# Construction de l'abre

arbre = []
for x in sorted(compte.items(), key=lambda x: x[1]):
    feuille = Arbre(x)
    feuille.fils0 = None
    feuille.fils1 = None
    arbre.append(feuille)

k = 0

while k < len(arbre) - 1:
    nouveau = (arbre[k].carac + arbre[k + 1].carac, arbre[k].freq + arbre[k + 1].freq)
    Noeud = Arbre(nouveau)
    arbre[k].pere = Noeud
    arbre[k + 1].pere = Noeud
    Noeud.fils0 = arbre[k]
    Noeud.fils1 = arbre[k + 1]
    arbre.append(Noeud)
    k += 2
    arbre = sorted(arbre, key=lambda x: x.freq)


# On parcourt l'arbre pour creer un dictionnaire

dico = {}


def parcours(x):
    if x.fils0 == None:
        dico[x.carac] = x.code

    else:
        gauche = x.fils0
        droite = x.fils1
        gauche.code("0")
        droite.code("1")
        parcours(gauche)
        parcours(droite)


racine = arbre[-1]
racine.code = ""
parcours(racine)

coder = args.coder
nom_decod = coder + ".coder"
with open(nom_decod, "w") as f:
    fichier = json.dumps(dico)
    f.write(fichier)
f.close
