# -*- coding:Utf-8 -*-
"""Data class"""

import csv
import logging

from . import society

""" Data class

   ? Prend en charge les données du fichier csv et les autres données.

   Entrée:
       *   path-csv -> str => Chemin du fichier csv

"""
class Data:
    """Data class"""

    def __init__(self, path_csv: str, config):

        self.logger = logging.getLogger('PostAumatique-Log')

        self.logger.info("Initialisation de la classe Data...")
        
        self.config = config

        self.logger.info("Récupération du fichier csv...")
        self.path_csv = path_csv
        
        self.logger.info("Récupération des données du fichier csv...")
        self.societys = self.__read_csv()
        
        self.logger.info("Données récupérées avec succès !")

    def get_societys(self) -> list:
        """get_societys function

        Returns:
            list -- list of society
        """
        return self.societys

    def __read_csv(self) -> list:
        """read_csv function

        Returns:
            list -- list of society
        """

        self.logger.info("Lecture du fichier csv...")
        fichier = open(self.path_csv, "r", encoding="utf-8")
        
        self.logger.info("Parssage du fichier csv...")
        c_r = csv.reader(fichier, delimiter=";")

        societys = []
        count = 0

        self.logger.info("Attribution des données du fichier csv...")
        for row in c_r:

            count += 1

            if count == 1:
                continue

            info = row[0].split(",")
            
            excludeOn = True
            
            if info[5].lower().strip() != "true":
                excludeOn = False

            societys.append(society.Society(
                info[0],
                info[1],
                info[2],
                info[3],
                info[4],
                excludeOn,
                self.config
            ))

        self.logger.info("Fermeture du fichier csv...")
        fichier.close()

        self.logger.info("Données du fichier csv attribuées avec succès !")

        return societys
