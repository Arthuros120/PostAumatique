# -*- coding: utf-8 -*-
"""generator"""

import logging
import datetime as dt
import os
import shutil

from model.ia import Ia


class Generator:
    """Generator
    """

    def __init__(self, data, config):

        self.logger = logging.getLogger("PostAumatique-Log")

        self.logger.info("Initialisation du générateur...")
        self.logger.info("Récupération des données...")

        self.data = data

        self.logger.info("Récupération de la configuration...")
        self.config = config

        self.logger.info("Récupération de l'IA...")
        self.ia = Ia(config)

        self.logger.info("Génération du dossier d'export...")
        self.export_path = self.__generate_directory()

        self.logger.info("Génération des dossiers de sociétés...")
        self.export_society_paths = self.__generate_society_directorys()

        self.logger.info("Génération des fichiers de sociétés...")
        self.__generate_society_files()

    def __generate_directory(self) -> str:
        """ generate_directory """

        export_path = "export/" + dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        self.logger.info("Création du dossier d'export: " +
                         export_path + "...")

        os.mkdir(export_path)

        self.logger.info("Dossier d'export créé avec succès !")

        return export_path

    def __generate_society_directorys(self) -> list:
        """generate_society_directorys

        Returns:
            list -- list of society directorys
        """

        self.logger.info("Création des dossiers de sociétés...")
        export_society_paths = []

        for society in self.data.get_societys():

            self.logger.info(
                "Création du dossier de la société: " + society.get_name() + "...")
            export_society_path = self.export_path + "/" + society.get_name()
            export_society_paths.append(export_society_path)

            os.mkdir(export_society_path)

            self.logger.info("Dossier de la société créé avec succès !")

        self.logger.info("Dossiers de sociétés créés avec succès !")
        return export_society_paths

    def __generate_society_files(self):
        """generate_society_files
        """

        self.logger.info("Création des fichiers de sociétés...")
        for i in range(len(self.data.get_societys())):

            self.logger.info("Création du fichier de la société: " +
                             self.data.get_societys()[i].get_name() + "...")
            society = self.data.get_societys()[i]

            self.logger.info(
                "Récupération des données de la société: " + society.get_name() + "...")
            export_society_path = self.export_society_paths[i]

            self.logger.info(
                "Génération du fichier de la société: " + society.get_name() + "...")
            self.__generate_society_file(society, export_society_path)

        self.logger.info("Fichiers de sociétés créés avec succès !")

    def __generate_society_file(self, society, export_society_path: str):
        """generate_society_file

        Args:
            society (Society): society
            export_society_path (str): export_society_path
        """

        self.logger.info("Génération du cv de la société: " +
                         society.get_name() + "...")
        cv_path = export_society_path + \
            "/Cv_Hamelin_Arthur_" + society.get_name() + ".pdf"
        shutil.copy("res/cv/Cv_Hamelin_Arthur_20230117.pdf", cv_path)

        society.cv_path = cv_path

        self.logger.info("Génération du cv de la société réussi !")

        society.motiv_letter = self.__generate_motivation_file(
            society, export_society_path)

    def __generate_motivation_file(self, society, export_society_path: str) -> str:
        """generate_motivation_file

        Args:
            society (Society): society
            export_society_path (str): export_society_path

        Returns:
            str -- motivation letter path
        """

        self.logger.info(
            "Génération de la lettre de motivation de la société: " + society.get_name() + "...")

        motiv_letter_tex_path = export_society_path + \
            "/Arthur-Hamelin_Lettre-de-motivation_" + society.get_name() + ".tex"

        motiv_letter_pdf_path = export_society_path + \
            "/Arthur-Hamelin_Lettre-de-motivation_" + society.get_name() + ".pdf"

        shutil.copy(
            "res/motivationLetter/motivationLetter.tex",
            motiv_letter_tex_path
        )

        shutil.copy(
            "res/motivationLetter/body.txt",
            export_society_path + "/body.txt"
        )

        self.__format_body_file(export_society_path + "/body.txt", society)

        # A mettre dans un if avec ou sans IA
        shutil.copy(
            "res/motivationLetter/bodySociety.txt",
            export_society_path + "/bodySociety.txt"
        )

        self.__format_body_society_file(
            export_society_path + "/bodySociety.txt", society, export_society_path + "/body.txt")

        current_path = os.getcwd()

        self.__format_motivation_file(
            motiv_letter_tex_path, society, current_path)

        full_tex_path = current_path + "/" + motiv_letter_tex_path

        os.chdir(export_society_path)

        os.system(
            "pdflatex " + full_tex_path + " -output-directory " + export_society_path
        )
        os.chdir(current_path)

        self.logger.info(
            "Génération de la lettre de motivation de la société réussi !")

        return motiv_letter_pdf_path

    def __format_body_file(self, body_path: str, society):
        """__format_body_file

        Arguments:
            body_path {str} -- body_path
            society {Society} -- society
        """

        with open(body_path, "r", encoding="utf-8") as file:

            lines = file.readlines()

        with open(body_path, "w", encoding="utf-8") as file:

            for line in lines:

                if "¤Society¤" in line:

                    print(line.replace("¤Society¤", society.get_name()),
                          file=file, end="")
                else:

                    print(line, file=file, end="")

        with open(body_path, "r", encoding="utf-8") as file:

            lines = file.readlines()

        for line in lines:

            society.body_text += line

    def __format_body_society_file(self, body_society_path: str, society, body_path: str):
        """__format_body_society_file

        Arguments:
            body_society_path {str} -- body_society_path
            society {Society} -- society
        """

        if self.config.get("Ia", 'enable'):

            society.body_society_text = self.ia.generate_text(
                body_path,
                society
            )

        else:

            with open(body_society_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            for line in lines:

                society.body_society_text += line

    def __format_motivation_file(
        self,
        motiv_letter_tex_path: str,
        society,
        current_path: str
    ):
        """format_motivation_file

        Args:
            motiv_letter_tex_path (str): motiv_letter_tex_path
            society (Society): society
            current_path (str): current_path
        """

        with open(motiv_letter_tex_path, "r", encoding="utf-8") as file:

            lines = file.readlines()

        with open(motiv_letter_tex_path, "w", encoding="utf-8") as file:

            for line in lines:

                if "¤Society¤" in line:

                    print(line.replace("¤Society¤", society.get_name()),
                          file=file, end="")

                elif "¤Addresse¤" in line:

                    print(line.replace("¤Addresse¤",
                                       society.get_addresse()), file=file, end="")

                elif "¤Body¤" in line:

                    print(line.replace("¤Body¤",
                                       society.get_body_text()), file=file, end="")

                elif "¤BodySociety¤" in line:

                    print(line.replace("¤BodySociety¤",
                                       society.get_body_society_text()), file=file, end="")

                elif "¤Base_Url¤" in line:

                    print(line.replace("¤Base_Url¤",
                                       current_path), file=file, end="")

                elif "¤City¤" in line or "¤PostalCode¤" in line:

                    if "¤City¤" in line:

                        line = line.replace("¤City¤", society.get_city())

                    if "¤PostalCode¤" in line:

                        line = line.replace("¤PostalCode¤",
                                            society.get_postal_code())

                    print(line, file=file, end="")

                else:

                    print(line, file=file, end="")
