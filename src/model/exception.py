# -*- coding: utf-8 -*-
"""This module contains the custom exception classes"""


class NotBodyException(Exception):
    "La lettre de motivation n'a pas de corps de texte"


class NotBodySocietyException(Exception):
    "La lettre de motivation n'a pas de corps de texte personalisé pour la société"


class NotConfigParamException(Exception):
    "Le paramètre n'est pas présent dans le fichier de configuration"
