# -*- coding: utf-8 -*-
"""society"""

import logging
from model.exception import NotBodyException, NotBodySocietyException


class Society:
    """Society
    """

    def __init__(self, name: str, addresse: str, postal_code: str, city: str, email: str):

        self.logger = logging.getLogger("PostAumatique-Log")

        self.logger.info("Génération de la société...")

        self.logger.info("Nom de la société: " + name)
        self.name = name

        self.logger.info("Adresse de la société: " + addresse)
        self.addresse = addresse

        self.logger.info("Code postal de la société: " + postal_code)
        self.postal_code = postal_code

        self.logger.info("Ville de la société: " + city)
        self.city = city

        self.logger.info("Email de la société: " + email)
        self.email = email

        self.cv_path = ""
        self.motiv_letter = ""
        self.body_text = ""
        self.body_society_text = ""

        self.logger.info("Génération de la société réussi !")

    def get_name(self) -> str:
        """get_name

        Returns:
            str -- name
        """

        return self.name

    def get_addresse(self) -> str:
        """get_addresse

        Returns:
            str -- addresse
        """

        return self.addresse

    def get_postal_code(self) -> str:
        """get_postal_code"""

        return self.postal_code

    def get_city(self) -> str:
        """get_city

        Returns:
            str -- city
        """

        return self.city

    def get_email(self) -> str:
        """get_email

        Returns:
            str -- email
        """
        return self.email

    def get_cv_path(self) -> str:
        """get_cv_path

        Returns:
            str -- cv_path
        """

        return self.cv_path

    def get_motiv_letter(self) -> str:
        """get_motiv_letter

        Returns:
            str -- motiv_letter
        """

        return self.motiv_letter

    def get_body_text(self) -> str:
        """body_text

        Returns:
            str -- body_text
        """

        if self.body_text == "":
            raise NotBodyException("body_text is empty")
        else:
            return self.body_text

    def get_body_society_text(self) -> str:
        """body_society_text"""

        if self.body_society_text == "":
            raise NotBodySocietyException("body_society_text is empty")
        else:
            return self.body_society_text

    def get_paths(self) -> str:
        """get_paths"""

        path_cv = self.cv_path.split("/")[-1]
        path_motiv_letter = self.motiv_letter.split("/")[-1]

        return path_cv + ", " + path_motiv_letter + ", lettre_recommandation_Arthur_Castorama.pdf"

    def get_files(self) -> list[str]:
        """get_files"""

        return [self.cv_path, self.motiv_letter, "res/recomandationLetter/lettre_recommandation_Arthur_Castorama.pdf"]

    def afficher(self) -> str:
        """afficher"""

        return 'Society -> {name: ' + self.name + ', addresse: ' + self.addresse + \
            ', postal_code: ' + self.postal_code + ', city: ' + self.city + ', cv_path: ' + \
            self.cv_path + ', motiv_letter: ' + self.motiv_letter + '}'
