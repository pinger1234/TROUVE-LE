# -*- coding: utf-8 -*-

# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
# [0] [Importation des modules]
# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
from __future__ import unicode_literals
from deta import *
import bcrypt
from flask import request, jsonify
# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
# [1] [Creation des fonctions pour l'ajout d'utilisateur ]
# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜

Token = "GvU7GWAn_4ZAs2z8fPiCk6HzxHajpRjDq4qAuYM45"
Datakey = "a03qi4zrdq7_Tr6fSQyVRzP9u7xgbyssQSoZzEeeceQY"
deta = Deta(Datakey)
salt = bcrypt.gensalt()

def add_user(db,user):
	bytes = user.password.encode('utf-8')
	hashed = bcrypt.hashpw(bytes, salt)
	utilisateur = db.put({
		"key":user.tel,
		"pp":user.pp,
        "nom": user.nom,
        "prenoms":user.prenoms,
        "naissance":user.naissance
        "piece": user.piece,
        "npiece":user.npiece,
        "tel":user.tel,
        "email":user.email,
        "password":hashed
    })
    return jsonify(utilisateur, 201)



def get_user(key):
    user = db.get(key)
    return user if user else jsonify({"error": "Not found"}, 404)


def update_user(key,new_data):
    user = db.put(new_data, key)
    return user


def delete_user(key):
    db.delete(key)
    return jsonify({"status": "ok"}, 200)


def pass_correct(passeword,hashed):
	userBytes=passeword.encode('utf-8')
	result = bcrypt.checkpw(userBytes, hashed)
	return result


def authentification(key,passeword):
	if get_user(key) :
		if pass_correct(passeword, get_user(key).password):
			return True
		else:
			return False
	else:
		return None