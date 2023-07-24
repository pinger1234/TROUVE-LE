# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from urllib.parse import urlparse, urljoin
from werkzeug.security import generate_password_hash, check_password_hash
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
    jsonify,
)  # pip install flask

from mailer import Mailer  # pip install quick-mailer
from flask_login import (
    LoginManager,
    UserMixin,
    login_required,
    login_user,
    logout_user,
    current_user,
)  # pip install flask-login


from _database import *
from _forms import *
from _validation import *
from _declaration import *

# --------------------------- {Module de chiffrage} ----------------------------------------


# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
# [1] [Configuration de Deta et initialisation des bases de données]
# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
# ================ {initialisation du projet} ===============

# Token = "GvU7GWAn_4ZAs2z8fPiCk6HzxHajpRjDq4qAuYM45"
# Datakey = "a03qi4zrdq7_Tr6fSQyVRzP9u7xgbyssQSoZzEeeceQY"

# cle_trouve_le = "a0azww1wj87_tJRPYB72Z9XWSpd5Nx4n6VMTNaUfakcZ"
cle_trouve_le = "a0j21vwmstk_Jq4CUVuRjvTtUXt5eUqtQdVVycpnujgH"
deta = Deta(cle_trouve_le)

# ================ {Base de données} ===============

users = deta.Base("users")
histo_pass = deta.Base("histo_pass")
declaration = deta.Base("declaration")
type_objet = deta.Base("type_objet")

# ================ {drive} ===============
users_pp = deta.Drive("users_pp")
identite = deta.Drive("identite")
img_declaration = deta.Drive("img_declaration")

# ================ {Variables} ==================


app = Flask(__name__)


app.config["SECRET_KEY"] = "GvU7GWAn_4ZAs2z8fPiCk6HzxHajpRjDq4qAuYM45"
mail = Mailer(email="lacentrale.cognitive@gmail.com", password="xfyvwxvgmfizdmqs")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Connectez-vous pour accéder à cette page."
# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
# [2] [definition des fonctions ]
# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.values.get("next"), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


def redirect_back(endpoint, **values):
    target = request.form["next"]
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)


class dict_to_user(UserMixin):
    def __init__(self, data):
        for key, value in data.items():
            self.__dict__[key] = value

    def get_id(self):
        return self.key


@login_manager.user_loader
def load_user(user_id):
    data = users.get(user_id)
    user = dict_to_user(data)
    return user


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/carousel/")
def carousel():
    return render_template("carousel.html")


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
        user.pp = str(user.tel) + ".png"
        user.validate = False
        if user_exist(users, user.tel):
            return render_template(
                "signup.html",
                message="user-exist",
            )
        elif not get_user(users, user.tel) and passwordconfirm != user.password:
            return render_template(
                "signup.html",
                message="passe-confirm-error",
            )
        elif (
            not user_exist(users, user.tel)
            and passwordconfirm == user.password
            and passwordconfirm != ""
        ):
            if request.files["pp"]:
                file_data = request.files.get("pp")
                file_ext = file_data.filename.split(".")[-1]
                user.pp = str(user.tel) + "." + file_ext
                save_file(users_pp, user.pp, file_data)

            else:
                file_data = open("static/img/profile-default.png", "rb")
                file_name = str(user.tel) + ".png"
                save_file(users_pp, file_name, file_data.readlines())
                file_data.close()

            user.validate = gen_validation_code()
            message = validation_message(user.validate)
            objet = "VALIDATION DE MAIL POUR TROUVE-LE"
            destination = user.email
            result = add_user(users, user)
            print("reponse d'ajout utilisateur:", result)
            if not result:
                return render_template(
                    "signup.html",
                    message="erreur",
                )
            else:
                send_mail(mail, objet, message, destination)
                return redirect(url_for("validation", key=user.key))
        else:
            return render_template(
                "signup.html",
                message="passe-vide",
            )
    else:
        return render_template("signup.html", message="")


@app.route("/validation/<key>", methods=["POST", "GET"])
def validation(key):
    print(get_all(users))
    user = get_user(users, key)
    if request.method == "GET":
        if user:
            print(user)
            # print(user.validate)
            return render_template("validation.html", message="")
        else:
            return render_template("session_error.html")
    else:
        code = str(
            str(request.form["n1"])
            + str(request.form["n2"])
            + str(request.form["n3"])
            + str(request.form["n4"])
            + str(request.form["n5"])
            + str(request.form["n6"])
        )
        print(code)
        confirmation = validate_user(users, key, code)
        if confirmation:
            return redirect(url_for("login"))
        else:
            return render_template("validation.html", message="bad-code")


@app.route("/login/", methods=["POST", "GET"])
def login():
    # print(get_all(users))
    if current_user.is_authenticated:
        return redirect(url_for("accueil"))
    if request.method == "POST":
        input_key = request.form["key"]
        if input_key == "":
            return render_template("login.html", message="login-error")
        else:
            print(input_key)
            input_password = request.form["password"]
            user = get_user(users, input_key)
        if user and pass_correct(input_password, user["password"]) and user["validate"]:
            print("======Login user added successfully")
            print(user)
            remember = request.form["remember"]
            login_user(load_user(input_key), remember=remember)
            next = request.args.get("next")
            if not is_safe_url(next):
                return abort(400)
            print(current_user)
            return redirect(next or url_for("accueil"))
        elif (
            user
            and pass_correct(input_password, user["password"])
            and not user["validate"]
        ):
            return redirect(url_for("validation", key=input_key))
        else:
            return render_template("login.html", message="login-error")
    return render_template("login.html", message="")


@app.route("/accueil", methods=["POST", "GET"])
@login_required
def accueil():
    declar = declarations()
    # print(declar)
    return render_template("accueil.html", declarations=declar)


@app.route("/settings")
@login_required
def settings():
    pass


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/resetpass", methods=["POST", "GET"])
def resetpass():
    user = utilisateur()
    if request.method == "POST": 
        user_ = request.form["user_identify"]
        if is_tel(user_) and user_exist(users, user_):
            use_data = get_user(users, user_)
            user.email=use_data["email"]
            user.validate = gen_validation_code()
            use_data["validate"] = user.validate
            update_user(users,user_,use_data,100)
            message = validation_message_reset_pass(user.validate)
            objet = "CODE DE REINITIALISATION DU MOT DE PASSE"
            destination = user.email
            status = send_mail(mail, objet, message, destination)
            return redirect(url_for("validate_pass", key=user_))
            # else:
            #     return render_template("Reset_request.html",  title="Reset passe",val = user_, message="erreur")
        else:
            return render_template("Reset_request.html",  title="Reset passe",val = user_, message="erreur_utili")
    return render_template("Reset_request.html", title="Reset passe")

@app.route("/validate_pass/<key>", methods=["POST", "GET"])
def validate_pass(key):
    user = get_user(users, key)
    if request.method == "GET":
        if user:
            return render_template("validation.html", message="")
        else:
            return render_template("session_error.html")
    else:  
        code = str(
            str(request.form["n1"])
            + str(request.form["n2"])
            + str(request.form["n3"])
            + str(request.form["n4"])
            + str(request.form["n5"])
            + str(request.form["n6"])
        )
        print(code)
        confirmation = validate_user(users, key, code)
        if confirmation:
            return redirect(url_for("reset_pas"))
        else:
            return render_template("validation.html",message="bad-code")

@app.route("/reset_pas", methods=["POST", "GET"])
def reset_pas():
    # update = False
    # if request.method=="POST":
    #     user_pass            = pass_user()
    #     user_pass.autoincre  += 1
    #     user_pass.key        = request.form["user_identify"]
    #     user_pass.newpasswrd = request.form["user_password"]
    #     user_pass.confnewpasswrd = request.form["user_newpassword"]
        
    #     if user_pass.key !="" and user_exist(users, user_pass.key) and user_pass.newpasswrd==user_pass.confnewpasswrd:
    #         user = get_user(users, user_pass.key)
    #         add_password(histo_pass,user_pass)
    #         if user_exist(histo_pass, user_pass.key):
    #             user["password"]= generate_password_hash(user_pass.newpasswrd)
    #             update_user(users,user_pass.key,user,600)
    #             print("******** Mot de passe modifier ********")
    #             return render_template("reset_pass_form.html", title="Reinitialisation", message="erreur")

    #     else:
    #         return render_template("reset_pass_form.html", title="Reinitialisation", message="erreur_pass")

    if request.method == "POST":
        id_  = request.form["user_identify"]
        newpass = request.form["user_password"]
        confpass = request.form["user_newpassword"]
        if id_ != "" and newpass == confpass:
            user = get_user(users, id_)
            hashe = generate_password_hash(newpass)
            user ["password"] = hashe
            update_user(users,id_, user, 600)
            return redirect(url_for("login"))
        else:
             return render_template("reset_pass_form.html", title="Reinitialisation", message="erreur_pass")
    return render_template("reset_pass_form.html", title="Reinitialisation")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8080")
