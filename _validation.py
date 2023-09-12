# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import numpy as np
from deta import *
import time
import datetime
from _database import *


def is_tel(value):
    regex = r"^(01|07|05)[0-9]{8}"
    result = re.match(regex, value)
    return result


def is_email(value):
    regex = r"^\S+@\S+\.\S+$"
    result = re.match(regex, value)
    return result


def gen_validation_code():
    return "".join(str(e) for e in list((np.random.choice(a=10, size=6))))


def validation_message(value):
    text = f"""Vous avez essayé de creer un compte 'Trouve-le'. \n
    Votre code de validation est : <b> {value} </b>. \n
    Ce code expirera dans 10 minutes à compter de {datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')}.
    """
    return text

def validation_message_reset_pass(value):
    text = f"""Vous avez essayé de modifier le mot de passe de votre compte 'Trouve-le'. \n
    Votre code de validation est : <b> {value} </b>. \n
    Ce code expirera dans 10 minutes à compter de {datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')}.
    """
    return text

def send_mail(mail, objet, message, destination):
    mail.send(receiver=destination, subject=objet, message=message)
    print("====STATUS MESSAGE:", mail.status)
    print(f"+++ Email envoyé à {destination} avec succès:  +++++++++")
    return mail.status


def validate_user(db, key, code):
    if str(get_user(db, key)["validate"]) == code:
        old_data = get_user(db, key)
        old_data["validate"] = True
        old_data.pop("__expires", None)
        new_data = old_data
        print(new_data)
        db.put(new_data)
        print("New data:", get_user(db, key))
        return True
    else:
        return False


# prit(gen_validation_code())
