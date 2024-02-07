import sys
import os
import typing
from PyQt5 import QtGui
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer, QSettings
from PyQt5.QtWidgets import QWidget
from googletrans import Translator
import openai
import subprocess
import webbrowser

with open('token.txt', 'r') as file:
    api_key = file.read().strip()
openai.api_key = api_key

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        scriptDir = os.path.dirname(os.path.realpath(__file__))
        iconPath = os.path.join(scriptDir, 'resources', 'Logo.png')
        self.setWindowIcon(QtGui.QIcon(iconPath))
        self.setWindowTitle("DumsTools")

        # Dark mode
        self.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        
        # Boutons du menu correction
        self.btn_correction = QPushButton("Correction", self)
        self.btn_correction.clicked.connect(self.ouvrir_correction)
        self.btn_correction.setFixedSize(450, 30)  # Définir une taille fixe pour le bouton
        self.btn_correction.setStyleSheet("QPushButton"
                                          "{"
                                          "border-radius: 10px;"
                                          "}"
                                          "QPushButton::hover"
                                          "{"
                                          "background: rgba(105, 105, 105, 0.3) ;border-radius: 10px;"
                                          "}"
                                          )
        shadow = QGraphicsDropShadowEffect() 
        shadow.setOffset(1, 1)
        shadow.setColor(QColor("black"))
        shadow.setBlurRadius(15)
        self.btn_correction.setGraphicsEffect(shadow) 
        self.layout.addWidget(self.btn_correction, alignment=Qt.AlignCenter)


        # Boutons du menu raccourcis
        self.btn_raccourcis = QPushButton("Raccourcis", self)
        self.btn_raccourcis.clicked.connect(self.ouvrir_raccourcis)
        self.btn_raccourcis.setFixedSize(450, 30)  # Définir une taille fixe pour le bouton
        self.btn_raccourcis.setStyleSheet("QPushButton"
                                    "{"
                                    "border-radius: 10px;"
                                    "}"
                                    "QPushButton::hover"
                                    "{"
                                    "background: rgba(105, 105, 105, 0.3) ;border-radius: 10px;"
                                    "}")
        shadow = QGraphicsDropShadowEffect() 
        shadow.setOffset(1, 1)
        shadow.setColor(QColor("black"))
        shadow.setBlurRadius(15)
        self.btn_raccourcis.setGraphicsEffect(shadow) 
        self.layout.addWidget(self.btn_raccourcis, alignment=Qt.AlignCenter)

        # Boutons du menu traduction
        self.btn_traduction = QPushButton("Traduction", self)
        self.btn_traduction.clicked.connect(self.ouvrir_traduction)
        self.btn_traduction.setFixedSize(450, 30)  # Définir une taille fixe pour le bouton
        self.btn_traduction.setStyleSheet("QPushButton"
                                    "{"
                                    "border-radius: 10px;"
                                    "}"
                                    "QPushButton::hover"
                                    "{"
                                    "background: rgba(105, 105, 105, 0.3) ;border-radius: 10px;"
                                    "}")
        shadow = QGraphicsDropShadowEffect() 
        shadow.setOffset(1, 1)
        shadow.setColor(QColor("black"))
        shadow.setBlurRadius(15)
        self.btn_traduction.setGraphicsEffect(shadow) 
        self.layout.addWidget(self.btn_traduction, alignment=Qt.AlignCenter)

        # Ajouter un étirement automatique en bas pour centrer les boutons
        self.centrer_fenetre()

    def keyPressEvent(self, event):
        # Séquence de touches : L-L R-R Haut-Bas Gauche-Droite
        if event.key() == Qt.Key_L and event.isAutoRepeat() == False:
            self.key_sequence.append('L')
        elif event.key() == Qt.Key_R and event.isAutoRepeat() == False:
            self.key_sequence.append('R')
        elif event.key() == Qt.Key_Z and event.isAutoRepeat() == False:
            self.key_sequence.append('Z')
        elif event.key() == Qt.Key_S and event.isAutoRepeat() == False:
            self.key_sequence.append('S')
        elif event.key() == Qt.Key_Q and event.isAutoRepeat() == False:
            self.key_sequence.append('Q')
        elif event.key() == Qt.Key_D and event.isAutoRepeat() == False:
            self.key_sequence.append('D')
        else:
            # Réinitialiser la séquence si une autre touche est pressée
            self.key_sequence = []
        if len(self.key_sequence) > 8:
            self.key_sequence = []
        if "".join(self.key_sequence) == "LLRRZSQD":
            self.play_easter_egg()
        print(self.key_sequence)
        print(len(self.key_sequence))
    def play_easter_egg(self):
        # Ouvrir la vidéo YouTube
        webbrowser.open("https://www.youtube.com/watch?v=QdBZY2fkU-0")
    key_sequence = []

    def ouvrir_correction(self):
        self.correction_window = CorrectionWindow(self)
        self.setCentralWidget(self.correction_window)

    def ouvrir_traduction(self):
        self.traduction_window = TraductionWindow(self)
        self.setCentralWidget(self.traduction_window)

    def ouvrir_raccourcis(self):
        self.raccourcis_window = RaccourcisWindow(self)
        self.setCentralWidget(self.raccourcis_window)
    

    def centrer_fenetre(self):
        resolution = QDesktopWidget().screenGeometry()
        self.setGeometry(
            (resolution.width() - self.width()) // 2,
            (resolution.height() - self.height()) // 2,
            self.width(),
            self.height()
        )

class CorrectionWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        label_original = QLabel("Entrez la phrase à corriger", self)
        label_original.setStyleSheet("font-family: arial, sans-serif; font-size: 12pt; font-weight: 900;")
        label_original.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(label_original)

        self.text_edit_original = QTextEdit(self)
        self.text_edit_original.setStyleSheet("border: 0px solid red; font-size: 12pt;")
        self.text_edit_original.setMinimumHeight(100)
        self.text_edit_original.setMaximumHeight(300)
        self.text_edit_original.setMinimumWidth(400)
        self.text_edit_original.setMaximumWidth(600)
        shadow_original = QGraphicsDropShadowEffect()
        shadow_original.setOffset(0, 0)
        shadow_original.setColor(QColor("black"))
        shadow_original.setBlurRadius(20)
        self.text_edit_original.setGraphicsEffect(shadow_original)
        self.layout.addWidget(self.text_edit_original, alignment=Qt.AlignCenter)

        self.btn_corriger = QPushButton("Corriger", self)
        self.btn_corriger.clicked.connect(self.corriger_phrase)
        self.btn_corriger.setFixedSize(100, 30)
        self.btn_corriger.setStyleSheet("QPushButton"
                                    "{"
                                    "border-radius: 10px;"
                                    "}"
                                    "QPushButton::hover"
                                    "{"
                                    "background: rgba(105, 105, 105, 0.3) ;border-radius: 10px;"
                                    "}")
        shadow_corriger = QGraphicsDropShadowEffect()
        shadow_corriger.setOffset(1, 1)
        shadow_corriger.setColor(QColor("black"))
        shadow_corriger.setBlurRadius(15)
        self.btn_corriger.setGraphicsEffect(shadow_corriger)
        self.layout.addWidget(self.btn_corriger, alignment=Qt.AlignCenter)

        label_corrige = QLabel("Texte corrigé", self)
        label_corrige.setStyleSheet("font-family: arial, sans-serif; font-size: 12pt; font-weight: 900;")
        label_corrige.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(label_corrige)

        self.text_edit_corrige = QTextEdit(self)
        self.text_edit_corrige.setStyleSheet("border: 0px solid red; font-size: 12pt;")
        self.text_edit_corrige.setMinimumHeight(100)
        self.text_edit_corrige.setMaximumHeight(300)
        self.text_edit_corrige.setMinimumWidth(400)
        self.text_edit_corrige.setMaximumWidth(600)
        shadow_corrige = QGraphicsDropShadowEffect()
        shadow_corrige.setOffset(0, 0)
        shadow_corrige.setColor(QColor("black"))
        shadow_corrige.setBlurRadius(20)
        self.text_edit_corrige.setGraphicsEffect(shadow_corrige)
        self.layout.addWidget(self.text_edit_corrige, alignment=Qt.AlignCenter)

        self.btn_copier = QPushButton("Copier", self)
        self.btn_copier.clicked.connect(self.copier_texte)
        self.btn_copier.setFixedSize(100, 30)
        self.btn_copier.setStyleSheet("QPushButton"
                                    "{"
                                    "border-radius: 10px;"
                                    "}"
                                    "QPushButton::hover"
                                    "{"
                                    "background: rgba(105, 105, 105, 0.3) ;border-radius: 10px;"
                                    "}")
        shadow_copier = QGraphicsDropShadowEffect()
        shadow_copier.setOffset(1, 1)
        shadow_copier.setColor(QColor("black"))
        shadow_copier.setBlurRadius(15)
        self.btn_copier.setGraphicsEffect(shadow_copier)
        self.layout.addWidget(self.btn_copier, alignment=Qt.AlignCenter)

        self.btn_menu = QPushButton("Menu", self)
        self.btn_menu.clicked.connect(self.retour_menu)
        self.btn_menu.setFixedSize(100, 30)
        self.btn_menu.setStyleSheet("QPushButton"
                                    "{"
                                    "border-radius: 10px;"
                                    "}"
                                    "QPushButton::hover"
                                    "{"
                                    "background: rgba(105, 105, 105, 0.3) ;border-radius: 10px;"
                                    "}")
        shadow_menu = QGraphicsDropShadowEffect()
        shadow_menu.setOffset(1, 1)
        shadow_menu.setColor(QColor("black"))
        shadow_menu.setBlurRadius(15)
        self.btn_menu.setGraphicsEffect(shadow_menu)
        self.layout.addWidget(self.btn_menu, alignment=Qt.AlignCenter)


    def corriger_phrase(self):
        phrase_a_corriger = self.text_edit_original.toPlainText()
        if phrase_a_corriger:
            # Implémentez votre logique pour corriger la phrase avec OpenAI ici
            prompt = f"Corrigez les erreurs dans le texte suivant :\n\n{phrase_a_corriger}\n\nCorrection :"
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=150
            )
            phrase_corrigee = response.choices[0].text.strip()
            self.text_edit_corrige.clear()
            self.text_edit_corrige.setPlainText(phrase_corrigee)

    def copier_texte(self):
        texte_copier = self.text_edit_corrige.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(texte_copier)

        # Modifier le texte et la couleur
        self.btn_copier.setText("Copié !")
        self.btn_copier.setStyleSheet("border-radius: 10px; padding: 6px;border-style: outset;color: green;")
        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(1, 1)
        shadow.setColor(QColor("green"))
        shadow.setBlurRadius(15)
        self.btn_copier.setGraphicsEffect(shadow)

        # Définir un QTimer pour rétablir les valeurs d'origine après 3 secondes
        QTimer.singleShot(1000, self.retablir_valeurs_originales)

    def retablir_valeurs_originales(self):
        self.btn_copier.setText("Copier")
        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(1, 1)
        shadow.setColor(QColor("black"))
        shadow.setBlurRadius(15)
        self.btn_copier.setGraphicsEffect(shadow)



    def retour_menu(self):
        self.parent().setCentralWidget(MainWindow())

class RenameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Renommer le fichier")
        
        self.layout = QVBoxLayout(self)
        self.lineEdit = QLineEdit(self)
        self.layout.addWidget(self.lineEdit)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(buttonBox)

class RaccourcisWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.layout = QVBoxLayout(self)

        # Ajouter un bouton pour ouvrir Chrome
        self.btn_chrome = QPushButton("Fl studio", self)
        self.btn_chrome.clicked.connect(self.ouvrir_fl)
        self.btn_chrome.setFixedSize(150, 150)
        self.btn_chrome.setStyleSheet("QPushButton"
                                    "{"
                                    "border-radius: 10px;"
                                    "}"
                                    "QPushButton::hover"
                                    "{"
                                    "background: rgba(105, 105, 105, 0.3) ;border-radius: 10px;"
                                    "}")
        shadow = QGraphicsDropShadowEffect() 
        shadow.setOffset(1, 1)
        shadow.setColor(QColor("black"))
        shadow.setBlurRadius(15)
        self.btn_chrome.setGraphicsEffect(shadow) 


        self.btn_menu = QPushButton("Menu", self)
        self.btn_menu.clicked.connect(self.retour_menu)
        self.btn_menu.setFixedSize(100, 30)
        self.btn_menu.setStyleSheet("QPushButton"
                                    "{"
                                    "border-radius: 10px;"
                                    "}"
                                    "QPushButton::hover"
                                    "{"
                                    "background: rgba(105, 105, 105, 0.3) ;border-radius: 10px;"
                                    "}")
        shadow = QGraphicsDropShadowEffect() 
        shadow.setOffset(1, 1)
        shadow.setColor(QColor("black"))
        shadow.setBlurRadius(15)
        self.btn_menu.setGraphicsEffect(shadow)


 # Ajouter un bouton pour ouvrir le programme personnalisé
        self.btn_programme_personnalise = QPushButton("Programme personnalisé", self)
        self.btn_programme_personnalise.setFixedSize(150, 150)
        self.btn_programme_personnalise.setStyleSheet("QPushButton"
                                    "{"
                                    "border-radius: 10px;"
                                    "}"
                                    "QPushButton::hover"
                                    "{"
                                    "background: rgba(105, 105, 105, 0.3) ;border-radius: 10px;"
                                    "}")
        shadow = QGraphicsDropShadowEffect() 
        shadow.setOffset(1, 1)
        shadow.setColor(QColor("black"))
        shadow.setBlurRadius(15)
        self.btn_programme_personnalise.setGraphicsEffect(shadow)
        # Charger le programme personnalisé enregistré
        self.settings = QSettings("VotreEntreprise", "VotreApplication")
        self.programme_personnalise = self.settings.value("programme_personnalise", "")
        # Extraire le nom du fichier du chemin complet
        self.nom_programme_personnalise = self.settings.value("nom_programme_personnalise", "")
        # Afficher le programme personnalisé sur le bouton
        self.btn_programme_personnalise.setText(self.nom_programme_personnalise)
        # Créer un menu contextuel pour le bouton
        self.btn_programme_personnalise.setContextMenuPolicy(Qt.CustomContextMenu)
        self.btn_programme_personnalise.customContextMenuRequested.connect(self.afficher_menu_contextuel)
        # Connecter le clic gauche pour ouvrir le programme
        self.btn_programme_personnalise.clicked.connect(self.ouvrir_programme_enregistre)
        # Connecter le clic droit pour afficher le menu contextuel
        self.btn_programme_personnalise.customContextMenuRequested.connect(self.afficher_menu_contextuel)
        self.layout.addWidget(self.btn_programme_personnalise)
        self.setGeometry(0, 0, 600, 300) 
        self.btn_programme_personnalise.move(210, 10)
        self.btn_chrome.move(10, 10)
        self.btn_menu.move(275, 425)


    def ouvrir_programme_personnalise(self):
        # Utiliser une boîte de dialogue pour permettre à l'utilisateur de choisir un programme
        programme_personnalise, ok = QFileDialog.getOpenFileName(self, "Programme personnalisé", "", "Tous les fichiers (*);;Fichiers exécutables (*.exe)")
        if ok:
            self.programme_personnalise = programme_personnalise
            nom_fichier = os.path.basename(self.programme_personnalise)
            self.btn_programme_personnalise.setText(nom_fichier)

            # Enregistrer le choix dans les paramètres
            self.settings.setValue("programme_personnalise", self.programme_personnalise)
            self.settings.setValue("nom_programme_personnalise", nom_fichier)

    def ouvrir_programme_enregistre(self):
        if self.programme_personnalise:
            try:
                subprocess.run([self.programme_personnalise], shell=True)
            except Exception as e:
                print(f"Erreur lors de l'ouverture du programme personnalisé : {e}")


    def supprimer_programme_enregistre(self):
        # Supprimer le programme enregistré
        self.programme_personnalise = ""
        self.btn_programme_personnalise.setText("Programme personnalisé")

        # Enregistrez la nouvelle valeur dans les paramètres
        self.settings.setValue("programme_personnalise", "")


    def changer_nom_programme(self):
        nouveau_nom, ok = QInputDialog.getText(self, "Changer le nom du programme", "Entrez le nouveau nom :")
        if ok:
            self.nom_programme_personnalise = nouveau_nom
            self.btn_programme_personnalise.setText(nouveau_nom)

            # Enregistrez le nouveau nom dans les paramètres
            self.settings.setValue("nom_programme_personnalise", nouveau_nom)

    def afficher_menu_contextuel(self, pos):
        menu = QMenu(self)

        # Ajouter une action pour ouvrir le programme
        ouvrir_programme_action = QAction("Ouvrir le raccourcis", self)
        ouvrir_programme_action.triggered.connect(self.ouvrir_programme_enregistre)
        menu.addAction(ouvrir_programme_action)

        # Ajouter une action pour changer le programme
        changer_programme_action = QAction("Changer le raccourcis", self)
        changer_programme_action.triggered.connect(self.ouvrir_programme_personnalise)
        menu.addAction(changer_programme_action)

        # Ajouter une action pour supprimer le programme
        supprimer_programme_action = QAction("Supprimer le raccourcis", self)
        supprimer_programme_action.triggered.connect(self.supprimer_programme_enregistre)
        menu.addAction(supprimer_programme_action)

        # Ajouter une action pour renommer le fichier
        renommer_action = QAction("Renommer le raccourcis", self)
        renommer_action.triggered.connect(self.changer_nom_programme)
        menu.addAction(renommer_action)

        # Personnaliser le design du menu
        menu.setStyleSheet(
            """
            QMenu {
                background-color: #2E2E2E;
                color: white;
                border: 1px solid #555555;
                border-radius: 10px;
            }
            QMenu::item {
                background-color: transparent;
                padding: 8px 20px;
                border-radius: 10px;
            }
            QMenu::item:selected {
                background-color: #555555;
            }
            """
        )

        # Afficher le menu contextuel à la position du clic droit
        menu.exec_(self.btn_programme_personnalise.mapToGlobal(pos))


    def ouvrir_fl(self):
        fichier_flp = r"C:\Users\augus\Desktop\config.flp"  # Remplacez par le chemin correct
        subprocess.run(["start", fichier_flp], shell=True)



    def retour_menu(self):
        self.parent().setCentralWidget(MainWindow())

class TraductionWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        # Créer un widget onglet
        self.onglets = QTabWidget(self)
        self.layout.addWidget(self.onglets)

        # Onglet pour le texte source et traduit
        self.onglet_texte = QWidget(self)
        layout_texte = QVBoxLayout(self.onglet_texte)

        self.label_texte_source = QLabel("Entrez la phrase à traduire :", self.onglet_texte)
        self.label_texte_source.setStyleSheet("font-family: arial, sans-serif	; font-size: 12pt;font-weight: 900;")
        self.label_texte_source.setAlignment(Qt.AlignCenter)
        layout_texte.addWidget(self.label_texte_source)

        self.text_edit_source = QTextEdit(self.onglet_texte)
        self.text_edit_source.setStyleSheet("border: 0px solid red; font-size: 12pt")
        self.text_edit_source.setMinimumHeight(100)
        self.text_edit_source.setMaximumHeight(300)
        self.text_edit_source.setMinimumWidth(400)
        self.text_edit_source.setMaximumWidth(600)
        shadow = QGraphicsDropShadowEffect() 
        shadow.setOffset(0, 0)
        shadow.setColor(QColor("black"))
        shadow.setBlurRadius(20)
        self.text_edit_source.setGraphicsEffect(shadow) 
        layout_texte.addWidget(self.text_edit_source, alignment=Qt.AlignCenter)

        self.label_texte_traduit = QLabel("Texte traduit :", self.onglet_texte)
        self.label_texte_traduit.setStyleSheet("font-family: arial, sans-serif	; font-size: 12pt;font-weight: 900;")
        self.label_texte_traduit.setAlignment(Qt.AlignCenter)
        layout_texte.addWidget(self.label_texte_traduit)

        self.text_edit_traduit = QTextEdit(self.onglet_texte)
        self.text_edit_traduit.setStyleSheet("border: 0px solid red; font-size: 12pt")
        self.text_edit_traduit.setMinimumHeight(100)
        self.text_edit_traduit.setMaximumHeight(300)
        self.text_edit_traduit.setMinimumWidth(400)
        self.text_edit_traduit.setMaximumWidth(600)
        shadow = QGraphicsDropShadowEffect() 
        shadow.setOffset(0, 0)
        shadow.setColor(QColor("black"))
        shadow.setBlurRadius(20)
        self.text_edit_traduit.setGraphicsEffect(shadow) 
        layout_texte.addWidget(self.text_edit_traduit, alignment=Qt.AlignCenter)

        self.onglets.addTab(self.onglet_texte, "Texte source et traduit")
        self.onglets.tabBar().setVisible(False)
        self.onglets.setStyleSheet("QTabWidget::pane { border: 0; }")

        # Ajouter les boutons
        self.btn_traduire = QPushButton("Traduire", self)
        self.btn_traduire.clicked.connect(self.traduire_phrase)
        self.btn_traduire.setFixedSize(100, 30)
        self.btn_traduire.setStyleSheet("QPushButton"
                                    "{"
                                    "border-radius: 10px;"
                                    "}"
                                    "QPushButton::hover"
                                    "{"
                                    "background: rgba(105, 105, 105, 0.3) ;border-radius: 10px;"
                                    "}")
        shadow = QGraphicsDropShadowEffect() 
        shadow.setOffset(1, 1)
        shadow.setColor(QColor("black"))
        shadow.setBlurRadius(15)
        self.btn_traduire.setGraphicsEffect(shadow) 
        self.layout.addWidget(self.btn_traduire, alignment=Qt.AlignCenter)

        self.btn_copier = QPushButton("Copier", self)
        self.btn_copier.clicked.connect(self.copier_texte)
        self.btn_copier.setFixedSize(100, 30)
        self.btn_copier.setStyleSheet("QPushButton"
                                    "{"
                                    "border-radius: 10px;"
                                    "}"
                                    "QPushButton::hover"
                                    "{"
                                    "background: rgba(105, 105, 105, 0.3) ;border-radius: 10px;"
                                    "}")
        shadow = QGraphicsDropShadowEffect() 
        shadow.setOffset(1, 1)
        shadow.setColor(QColor("black"))
        shadow.setBlurRadius(15)
        self.btn_copier.setGraphicsEffect(shadow) 
        self.layout.addWidget(self.btn_copier, alignment=Qt.AlignCenter)

        self.btn_menu = QPushButton("Menu", self)
        self.btn_menu.clicked.connect(self.retour_menu)
        self.btn_menu.setFixedSize(100, 30)
        self.btn_menu.setStyleSheet("QPushButton"
                                    "{"
                                    "border-radius: 10px;"
                                    "}"
                                    "QPushButton::hover"
                                    "{"
                                    "background: rgba(105, 105, 105, 0.3) ;border-radius: 10px;"
                                    "}")
        shadow = QGraphicsDropShadowEffect() 
        shadow.setOffset(1, 1)
        shadow.setColor(QColor("black"))
        shadow.setBlurRadius(15)
        self.btn_menu.setGraphicsEffect(shadow) 
        self.layout.addWidget(self.btn_menu, alignment=Qt.AlignCenter)

    def traduire_phrase(self):
        phrase_a_traduire = self.text_edit_source.toPlainText()
        if phrase_a_traduire:
            # Utiliser soit l'API Google Translate, soit googletrans, pas les deux.
            # Choisissez celle qui répond à vos besoins.

            # Utiliser l'API Google Translate (googletrans)
            translator = Translator()
            resultat_traduction = translator.translate(phrase_a_traduire, dest='en')  # Remplacez 'en' par la langue de destination souhaitée
            phrase_traduite = resultat_traduction.text

            # OU utiliser googletrans
            # phrase_traduite = Translator().translate(phrase_a_traduire).text

            self.text_edit_traduit.clear()
            self.text_edit_traduit.setPlainText(phrase_traduite)

    def copier_texte(self):
        texte_copier = self.text_edit_traduit.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(texte_copier)

        # Modifier le texte et la couleur
        self.btn_copier.setText("Copié !")
        self.btn_copier.setStyleSheet("border-radius: 10px; padding: 6px;border-style: outset;color: green;")
        shadow = QGraphicsDropShadowEffect() 
        shadow.setOffset(1, 1)
        shadow.setColor(QColor("green"))
        shadow.setBlurRadius(15)
        self.btn_copier.setGraphicsEffect(shadow) 

        # Définir un QTimer pour rétablir les valeurs d'origine après 3 secondes
        QTimer.singleShot(1000, self.retablir_valeurs_originales)

    def retablir_valeurs_originales(self):
        self.btn_copier.setText("Copier")
        shadow = QGraphicsDropShadowEffect() 
        shadow.setOffset(1, 1)
        shadow.setColor(QColor("black"))
        shadow.setBlurRadius(15)
        self.btn_copier.setGraphicsEffect(shadow) 
        self.btn_copier.setStyleSheet("border-radius: 10px; padding: 6px;border-style: outset;color: white;")

    def retour_menu(self):
        self.parent().setCentralWidget(MainWindow())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())