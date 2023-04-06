# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
# [0] [Importation des modules et packages]
# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
from deta import *  # pip install deta
from jinja2 import *  # pip install jinja2"
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
)  # pip install flask

# from pydantic import BaseModel  # pip install pydantic
# from cookies import *  # pip install cookies
# from PIL import Image # pip install pillow
import os
from _database import *
from _forms import *

# --------------------------- {Module de chiffrage} ----------------------------------------
from hashlib import *
import secrets
import getpass
import re

# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
# [1] [Configuration de Deta et initialisation des bases de données]
# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
# ================ {initialisation du projet} ===============

# Token = "GvU7GWAn_4ZAs2z8fPiCk6HzxHajpRjDq4qAuYM45"
# Datakey = "a03qi4zrdq7_Tr6fSQyVRzP9u7xgbyssQSoZzEeeceQY"

cle_trouve_le = "a0azww1wj87_tJRPYB72Z9XWSpd5Nx4n6VMTNaUfakcZ"
deta = Deta(cle_trouve_le)


# ================ {Base de données} ===============

users = deta.Base("users")
declaration = deta.Base("declaration")
type_objet = deta.Base("type_objet")

# ================ {drive} ===============
users_pp = deta.Drive("users_pp")
identite = deta.Drive("identite")
img_declaration = deta.Drive("img_declaration")

# ================ {Variables} ==================

# photo_profil = Image.open("static/img/logo.png",mode="r")
# photo_piece = Image.open("static/img/logo.png",mode="r")


# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
# [2] [definition des fonctions ]
# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/carousel/")
def carousel():
    return render_template("carousel.html")


@app.route("/login/", methods=["POST", "GET"])
def login():
    print(get_all(users))
    return render_template("login.html")


@app.route("/signup/", methods=["POST", "GET"])
def signup():
    # global photo_piece, photo_profil
    # print ("la methode de requet est :", request.method)
    print(get_all(users))
    if request.method == "POST":
        user = utilisateur()
        user.nom = request.form["nom"]
        user.prenoms = request.form["prenoms"]
        user.naissance = request.form["naissance"]
        user.npiece = request.form["npiece"]
        user.piece = request.form["piece"]
        user.tel = request.form["tel"]
        user.key = user.tel
        user.email = request.form["email"]
        user.password = request.form["password"]
        passwordconfirm = request.form["passwordconfirm"]
        user.pp = str(user.tel) + ".webp"

        if user_exist(users, user.tel):
            return render_template(
                "signup.html",
                message="user-exist",
            )
        elif (
            user_exist(users, user.tel) == False
        ) and passwordconfirm != user.password:
            return render_template(
                "signup.html",
                message="passe-confirm-error",
            )
        elif (
            (user_exist(users, user.tel) == False)
            and passwordconfirm == user.password
            and passwordconfirm != ""
        ):
            if request.files["pp"]:
                file_data = request.files.get("pp")
                file_ext = file_data.filename.split(".")[-1]
                user.pp = str(user.tel) + "." + file_ext
                # print("Donnees image:-----------------")
                # print(file_data)
                # print("Nom fichier image:-----------------")
                # print(file_name)
                save_file(users_pp, user.pp, file_data)
                result = add_user(users, user)
            print("reponse d'ajout utilisateur:", result)
            else:
                file_data = open("static/img/profile-default.png", "rb")
                print(file_data.readlines())
                save_file(users_pp, str(user.tel) + ".png", file_data.readlines())
                file_data.close()
            if result == False:
                return render_template(
                    "signup.html",
                    message="erreur",
                )
            else:
                return redirect(url_for("login"))
        else:
            return render_template(
                "signup.html",
                message="passe-vide",
            )
    else:
        return render_template("signup.html", message="")
    # Creation d'image par defaut de photo de profile et de piece d'identité
    # photo_profil = Image.open(url_for("static",filename="img/logo.png"), mode="rb")
    # photo_piece = Image.open(url_for("static",filename="img/logo.png"), mode="rb")

    # photo_profil = Image.open("static/img/logo.png", mode="r")
    # photo_profil = iio.imread("imageio:static/img/logo.png")
    # # photo_piece = Image.open("static/img/logo.png", mode="r")
    # photo_piece = iio.imread("imageio:static/img/logo.png")

    # file_ext = "png"

    # recupération des images depuis le formulaire si elle ont été envoyées
    # if request.files["photo_profil"]:
    #     photo_profil = request.files.get("photo_profil")
    #     file_ext = photo_profil.filename.split(".")[-1]

    # if request.files["photo_piece"]:
    #     photo_piece = request.files.get("photo_piece")
    #     file_ext=photo_piece.filename.split(".")[-1]

    # Ajout des images dans le drive de deta
    # pp.put(number_piece + "." + file_ext, photo_piece)
    # identite.put(number_piece + "." + file_ext, photo_piece)

    # # Sauvegarde des données dans la base de données users
    # users.put(
    #     {
    #         "First_name": name,
    #         "Last_name": second_name,
    #         "Birthday": birthday,
    #         "Number_of_piece": number_piece,
    #         "Type_piece": type_piece,
    #         "Photo_piece": "identite/" + number_piece + "." + file_ext,
    #         "Photo_profil": "pp/" + number_piece + "." + file_ext,
    #         "Contact": contact,
    #         "Email": email,
    #         "Password": password,
    #         "Password_confirm": passwordconfirm,
    #     }
    # )

    # return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8080")
