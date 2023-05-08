# -*- coding: utf-8 -*-
"""EmailSenderClass class"""

# Libraries

import logging
import smtplib
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class EmailSenderClass:

    def __init__(self, config):

        self.logger = logging.getLogger('PostAumatique-Log')

        self.logger.info("Initialisation de l'envoi d'email...")
        
        self.config = config

        self.logaddr = config.get("Email", "emailLogin")
        self.fromaddr = config.get("Email", "emailFrom")
        self.password = config.get("Email", "apiKey")

        self.logger.info("Email initialisé avec succès !")

    def load_email_template(self, template_path: str) -> str:

        self.logger.info("Chargement du template d'email...")

        email_template = ""

        with open(template_path, 'r') as file:
            email_template = file.read()

        self.logger.info("Template d'email chargé avec succès !")

        return email_template

    def send_message_via_server(self, toaddr: str, msg: MIMEMultipart) -> None:

        self.logger.info("Connexion au serveur d'email...")

        # Send the message via local SMTP server.
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        self.logger.info("Connexion au serveur d'email établie avec succès !")
        self.logger.info("Authentification au serveur d'email...")

        server.login(self.logaddr, self.password)

        self.logger.info(
            "Authentification au serveur d'email établie avec succès !")

        self.logger.info("Chargement du message à envoyer...")
        text = msg.as_string()
        self.logger.info("Message chargé avec succès !")

        self.logger.info("Envoi du message...")
        server.sendmail(self.fromaddr, toaddr, text)
        self.logger.info("Message envoyé avec succès !")

        self.logger.info("Déconnexion du serveur d'email...")
        server.quit()
        self.logger.info(
            "Déconnexion du serveur d'email établie avec succès !")

    def send_html_email_to(self, society) -> None:

        self.logger.info(
            "Préparation de l'envoi d'email à {}...".format(society.get_name()))

        # Message setup
        msg = MIMEMultipart()

        msg['From'] = "Hamelin Arthur <" + self.fromaddr + ">"
        msg['To'] = society.get_email()

        msg['Subject'] = "Hamelin Arthur - Etudiant à Polytech Nantes - Recherche d'alternance dans l'informatique"

        email_html = self.load_email_template("res/mail/index.html")

        self.logger.info("Formatage du template d'email...")

        email_html = email_html.replace("¤Society¤", society.get_name())

        email_html = email_html.replace("¤filePath¤", society.get_paths())

        self.logger.info("Template d'email formaté avec succès !")

        self.logger.info("attachment du template d'email...")
        # Add text to message
        msg.attach(MIMEText(email_html, 'html'))

        self.logger.info("Template d'email attaché avec succès !")

        self.logger.info("attachment des fichiers...")
        self.logger.info("Récupération des fichiers à attacher...")

        attach_files_name = society.get_files()

        self.logger.info("Fichiers à attacher récupérés avec succès !")

        if attach_files_name:

            self.logger.info("Traitement des fichiers à attacher...")

            for file_name in attach_files_name:

                self.logger.info(
                    "Traitement du fichier {}...".format(file_name))

                # Open file in binary mode
                with open(file_name, "rb") as attachment:

                    self.logger.info("Lecture du fichier...")

                    # Add file as application/octet-stream
                    # Email client can usually download this automatically as attachment
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())

                self.logger.info("Encodage du fichier...")
                # Encode file in ASCII characters to send by email
                encoders.encode_base64(part)

                self.logger.info("Ajout du fichier à l'email...")
                # Add header as key/value pair to attachment part
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {file_name.split('/')[-1]}",
                )

                self.logger.info("attachment du fichier...")
                # Add attachment to message and convert message to string
                msg.attach(part)

        self.logger.info("Fichiers attachés avec succès !")

        self.logger.info(
            "Etes-vous sûr de vouloir envoyer l'email à {} ?".format(society.get_name()))

        while True:

            input_user = input("Oui/Non : ")

            if input_user == "Oui":

                self.logger.info(
                    "Envoi de l'email à {}...".format(society.get_name()))

                self.send_message_via_server(society.get_email(), msg)

                self.logger.info("Email envoyé avec succès !")

                break

            elif input_user == "Non":

                self.logger.warning("Envoi de l'email annulé !")

                break
