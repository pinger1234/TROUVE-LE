# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random
import string

data = {}


def declarations():
    for i in range(1, 50):
        numero = f"declaration-{i}"
        auteur = "".join(
            random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10)
        )
        date = f"{random.randint(1, 31)}/{random.randint(1, 12)}/{random.randint(2010, 2023)}"
        types = ["Incendie", "Accident de la route", "Inondation", "Vol", "Vandalisme"]
        lieu = "".join(
            random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10)
        )
        description = "".join(
            random.choices(
                string.ascii_uppercase
                + string.ascii_lowercase
                + string.digits
                + string.punctuation,
                k=30,
            )
        )
        photo = f"https://example.com/declaration-{i}.jpg"

        data[numero] = {
            "auteur": auteur,
            "date": date,
            "type": random.choice(types),
            "lieu": lieu,
            "description": description,
            "photo": photo,
        }

    return data
