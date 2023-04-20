# -*- coding:Utf-8 -*-
"""Config file of the project"""

import yaml
import logging

from model.exception import NotConfigParamException

""" config.py

   ? Permet de charger les fichiers de configuration, de les lire et de les utiliser dans le programme.

   Entrée:
       *   path -> str => Chemin du fichier de configuration

"""


class config:

    # Initialisation de la classe
    def __init__(self, path: str):
        
        self.logger = logging.getLogger('PostAumatique-Log')
        
        self.logger.info("Initialisation de la configuration...")
        self.logger.info("Création des dictionnaires de configuration...")

        self.RES_IA = {}
        self.RES_EMAIL = {}
        self.RES_EXCLUDEFOLDER = {}
        
        self.CVPATH = ""
        
        self.logger.info("Dictionnaires de configuration créés avec succès !")

        self.logger.info("Chargement du fichier de configuration...")
        self.path = path

        self.logger.info("Parssage du fichier de configuration...")
        yaml_file = open(str(self.path), 'r')

        self.logger.info("Récupération des données du fichier de configuration...")
        dictionary = yaml.load_all(yaml_file, Loader=yaml.SafeLoader)

        for doc in dictionary:

            for key, value in doc.items():

                if key == "Ia":

                    self.RES_IA = value

                elif key == "Email":

                    self.RES_EMAIL = value
                
                elif key == "ExcludeFolder":

                    self.RES_EXCLUDEFOLDER = value
                    
                elif key == "CvPath":

                    self.CVPATH = value
        
        
        if self.CVPATH == "":
            
            raise NotConfigParamException(
                "Error: CvPath not found")
        
        self.logger.info("Configuration créée avec succès !")

    # Permet de récupérer les données d'un fichier de configuration
    # Retourne une donnée
    def get(self, types=None, arguments=None):

        self.logger.debug("Récupération des données de configuration...")
        self.logger.debug("Récupération des données de type {}...".format(types))
        self.logger.debug("Récupération des données de paramètre {}...".format(arguments))

        res = None

        if types == "Ia":

            res = self.RES_IA[str(arguments)]

        elif types == "Email":

            res = self.RES_EMAIL[str(arguments)]
        
        elif types == "ExcludeFolder":

            res = self.RES_EXCLUDEFOLDER[str(arguments)]
        
        elif types == "CvPath":
            
            res = self.CVPATH

        if res == None:

            raise NotConfigParamException(
                "Error: " + str(arguments) + " not found")

        else:

            self.logger.debug("Données récupérées avec succès !")
            self.logger.debug("Données récupérées: " + str(res))
            return res


""" import_conf.py

   ? Permet d'importer les fichiers de configuration.

    Entrée:
       *   path -> string =>  Chemin du fichier de configuration
"""


def import_conf(path):

    logger = logging.getLogger('PostAumatique-Log')

    logger.info("Création de la configuration...")

    try:

        conf = config(path)

        logger.info("Configuration créée avec succès !")

        return conf

    except Exception as error:

        logger.error("Erreur lors de la création de la configuration !")

        logger.error("Error: " + str(error))

        exit()

