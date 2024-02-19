import tkinter
from tkinter import ttk, Label
from param import *


class NouveauFournisseur(tkinter.Toplevel):

    def __init__(self, parent, titre_principal):
        super().__init__(parent)
        # Titre principale de la fenetre principale
        self.titre_principal = titre_principal
        self.wm_title(self.titre_principal + "  -  Nouveau fournisseur")
        self.wm_transient(parent)
        # Configurer la geometrie de la fenetre
        self.wm_geometry("700x350+250+150")
        # Impecher l'utilisateur de redimentionner la fenetre
        self.wm_resizable(False, False)
        self.config(background=CYAN)
        self.setMenu()
        
        self.label_nom_fournisseur = Label(self, text="Nom:", bg=CYAN)
        self.label_nom_fournisseur.place(x=140+50, y=75+35)

        self.entry_nom_fournisseur = ttk.Entry(self, width=35)
        self.entry_nom_fournisseur.place(x=180+50, y=75+35)

        self.label_adresse_fournisseur = Label(self, text="Adresse:", bg=CYAN)
        self.label_adresse_fournisseur.place(x=125+50, y=105+35)

        self.entry_adresse_fournisseur = ttk.Entry(self, width=35)
        self.entry_adresse_fournisseur.place(x=180+50, y=105+35)

        self.label_telephone_fournisseur = Label(self, text="Telephone:", bg=CYAN)
        self.label_telephone_fournisseur.place(x=110+50, y=145+35)

        self.entry_telephone_fournisseur = ttk.Entry(self, width=35)
        self.entry_telephone_fournisseur.place(x=180+50, y=145+35)
        
        self.label_mail_fournisseur = Label(self, text="Adresse mail:", bg=CYAN)
        self.label_mail_fournisseur.place(x=100+50, y=175+35)

        self.entry_mail_fournisseur = ttk.Entry(self, width=35)
        self.entry_mail_fournisseur.place(x=180+50, y=175+35)

        self.label_note_fournisseur = Label(self, text="Note:", bg=CYAN)
        self.label_note_fournisseur.place(x=190, y=175+35+40)

        self.entry_note_fournisseur = ttk.Entry(self, width=35)
        self.entry_note_fournisseur.place(x=180+50, y=175+35+40)

        self.boutonAnnuler()
        self.boutonOk()
        self.focus()

    # menu pour enregistrer les stocks
    def setMenu(self):
        titre = Label(self, font=(FONT_TYPE, FONT_SIZE, TITLE_FONT_WEIGHT),\
             text="Ajouter un fournisseur".upper(), background=LIGHTGREEN, height=3)
        titre.pack(side="top", fill="x")
    
    def boutonOk(self):
        btn_ok = ttk.Button(self, text="OK")
        btn_ok.place(x=620, y=320)

    def boutonAnnuler(self):
        btn_ok = ttk.Button(self, text="Annuler", command=self.destroy)
        btn_ok.place(x=540, y=320)

