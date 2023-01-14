import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("texte", help="texte a encoder ou decoder", type=str)
parser.add_argument(
    "-d", "--decode", help="si on veut decoder et non encoder", default=False
)
parser.add_argument("-o", "--output", help="nom de fichier de sortie", type=str)
parser.add_argument(
    "-c", "--coder", help="choix de l encodage", default="english.coder", type=str
)
args = parser.parse_args()


with open(args.coder, "r") as f:
    dico_string = f.read()


dico = json.loads(dico_string)

with open(args.texte, "r") as f:
    texte = f.read()


if args.decode:
    # On inverse la dictionnaire pour decoder
    dico_inv = {v: k for k, v in dico.items()}
    decode = ""
    clefs = dico_inv.keys()
    code = ""
    for num in texte:
        code += num
        if code in clefs:
            decode += dico_inv[code]
            code = ""

    if args.output is not None:
        with open(args.output, "w") as f:
            f.write(decode)
        f.close()

    else:
        nom_texte = args.texte
        nom_texte_decode = nom_texte[: len(nom_texte) - 4]
        with open(nom_texte_decode, "w") as f:
            f.write(decode)
        f.close()


else:
    encode = ""
    for x in texte:
        encode += dico[x]

    if args.output is not None:
        with open(args.output, "w") as f:
            f.write(encode)
        f.close()

    else:
        nom_texte = args.texte
        nom_texte_encode = nom_texte + ".huf"
        with open(nom_texte_encode, "w") as f:
            f.write(encode)
        f.close()
