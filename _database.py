# -*- coding: utf-8 -*-

# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
# [0] [Importation des modules]
# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
from __future__ import unicode_literals

# from deta import *

# # import bcrypt
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
# [1] [Creation des fonctions pour l'ajout d'utilisateur ]
# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜


def add_user(db, user):
    hashed = generate_password_hash(user.password)
    print("===========================")
    try:
        db.put(
            {
                "key": user.tel,
                "pp": user.pp,
                "nom": user.nom,
                "prenoms": user.prenoms,
                "naissance": user.naissance,
                "piece": user.piece,
                "npiece": user.npiece,
                "tel": user.tel,
                "email": user.email,
                "password": hashed,
                "validate": user.validate,
            },
            expire_in=600,
        )
        print("-------User enregistré")
        return True
    except:
        print("++++ user pas enrégistré")
        return False


def save_file(drive_name, file_name, file_data):
    try:
        drive_name.put(file_name, file_data)
        print("-------Image user sauvegardé")
        return True
    except:
        drive_name.put(file_name, path="static/img/profile-default.png")
        print("++++ erreur sauvegarde image")
        return False


def get_user(db, key):
    user = db.get(key)
    return user if user else False


def user_exist(db, key):
    user = db.get(key)
    return True if user else False


def get_all(db):
    print("-----telechargement de base de donnée")
    return db.fetch().items


def update_user(db, key, new_data, expire_in):
    user = db.put(new_data, key, expire_in=expire_in)
    return user


def delete_user(db, key):
    db.delete(key)
    return jsonify({"status": "ok"}, 200)


def pass_correct(passeword, hashed):
    result = check_password_hash(hashed, passeword)
    return result


def authentification(key, passeword):
    if get_user(key):
        if pass_correct(passeword, get_user(key).password):
            return True
        else:
            return False
    else:
        return None


# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
# [3] [Creation des objets pour la base de données ]
# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜


class utilisateur:
    def __init__(self):
        self.key = ""
        self.pp = ""
        self.nom = ""
        self.prenoms = ""
        self.naissance = ""
        self.piece = ""
        self.npiece = ""
        self.tel = ""
        self.email = ""
        self.passeword = ""
        self.validate = False


def add_declarations(db, declaration):
    db.put(
        {
            "auteur": declaration.auteur,
            "date": declaration.date,
            "type": declaration.type,
            "lieu": declaration.lieu,
            "description": declaration.description,
            "photo": declaration.photo,
            "horodator": datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S"),
        }
    )


class db_declaration:
    def __init__(self):
        self.auteur = ""
        self.date = ""
        self.type = ""
        self.lieu = ""
        self.description = ""
        self.photo = ""
