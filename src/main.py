# -*- coding:Utf-8 -*-
"""Main file of the project"""

import os
import logging
import time

from model.data import Data
from model.emailsenderclass import EmailSenderClass
from model.generator import Generator
from model.config import import_conf

FILE_EXPORT_DIRECTORY = "export/"
FILE_LOG_DIRECTORY = FILE_EXPORT_DIRECTORY + "logs/"

if __name__ == "__main__":

    print("Lancement du programme...")
    print("Changement du répertoire de travail...")

    os.chdir(__file__[:__file__.rfind("/")].replace("/src", ""))

    print("Répertoire de travail: " + os.getcwd())

    print("Mise en place des fichiers de log...")

    if not os.path.exists(FILE_EXPORT_DIRECTORY):
        os.makedirs(FILE_EXPORT_DIRECTORY)

    if not os.path.exists(FILE_LOG_DIRECTORY):
        os.makedirs(FILE_LOG_DIRECTORY)

    file_log_name = (
        FILE_LOG_DIRECTORY
        + str(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))
        + "_PostAumatique"
        + ".log"
    )  # Création  du nom du ficher log

    logger = logging.getLogger("PostAumatique-Log")
    logger.setLevel(logging.DEBUG)

    # Create file
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filename=file_log_name,
        level=logging.DEBUG,
    )

    # Create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - [ %(message)s ]"
    )

    # Add formatter to ch
    ch.setFormatter(formatter)

    # Add ch to logger
    logger.addHandler(ch)

    logger.info("Lancement du programme...")

    logger.debug("Importation du fichier de configuration...")
    config = import_conf("config/config.yml")

    while True:

        logger.debug("Demande du nom du fichier à importer...")

        input_file = input(
            "Entrez le nom du fichier à importer (sans l'extension): ")

        logger.debug("Retour de l'utilisateur: " + input_file)

        logger.info("Vérification de l'existence du fichier...")
        if os.path.isfile("import/" + input_file + ".csv"):

            logger.info("Le fichier existe !")
            break

        else:

            logger.error("Erreur: le fichier " + input_file + " n'existe pas")

    logger.info("Importation des données...")
    data = Data("import/" + input_file + ".csv", config)

    logger.info("Génération des lettres de motivation et des CV...")
    generator = Generator(data, config)

    if not config.get("Email", "enable"):

        logger.warning("Email désactivé")
        exit()

    societys = data.get_societys()

    correct_number = []

    for i in range(len(societys)):

        logger.info(str(i + 1) + " - " + societys[i].get_name())
        correct_number.append(str(i + 1))

    while True:

        societys_to_treat = []
        trigger_error = False

        logger.info(
            "Sélectionnez les société à traiter.\n(all pour toutes, none pour aucune, ou les numéros séparés par des espaces")
        logger.debug("Demande de l'utilisateur...")

        input_societys = input("Société(s) à traiter: ")

        logger.debug("Retour de l'utilisateur: " + input_societys)

        societys_to_trea_input = input_societys.split(" ")

        if len(societys_to_trea_input) == 1 and societys_to_trea_input[0] == "all":

            societys_to_treat = [int(i) for i in range(len(societys))]

            logger.info("Traitement de plusieurs société en cours...")
            break

        elif len(societys_to_trea_input) == 1 and societys_to_trea_input[0] == "none":

            logger.warning("Aucune société à traiter")
            exit()

        else:

            # Vérification que les numéros entrés sont corrects
            for number in societys_to_trea_input:

                if str(number) not in correct_number:

                    logger.error("Erreur: le numéro " +
                                 str(number) + " n'est pas valide")
                    trigger_error = True

            if not trigger_error:

                logger.info("Traitement de plusieurs société en cours...")
                societys_to_treat = [
                    int(society) - 1 for society in societys_to_trea_input]
                break

            else:

                logger.error("Veuillez réessayer")

    Mail = EmailSenderClass(config)

    for society in societys_to_treat:

        society = societys[society]

        logger.info("Traitement de la société " + society.get_name())

        Mail.send_html_email_to(society)

    logger.info("Traitement terminé")
    logger.info("Fin du programme")
