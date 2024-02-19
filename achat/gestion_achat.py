import tkinter
from tkinter import Frame, Label, Button, ttk
from achat import fournisseur
from param import *
import sqlite3
import pathlib


path = pathlib.Path('achat\\database\\fournisseurs.db')


class Achat(tkinter.Toplevel):
    inst_nouveau = None
    ligne = 1
    charger = False

    def __init__(self, parent, titre_principal):
        super().__init__(parent)
        self.titre_principal = titre_principal
        self.wm_title(self.titre_principal + "  -  Achats")
        self.wm_transient(parent)
        self.wm_geometry("1020x600+50+50")
        self.wm_resizable(False, False)
        self.frame_haut = Frame(self, bg=LIGHTGREEN, width=1020, height=60)
        self.frame_haut.pack(side='top', fill='y')
        # Menu gauche
        self.frame_gauche = Frame(self, bg="darkcyan", width=200, height=550)
        self.frame_gauche.pack(side='left', fill='x')
        # Menu droit
        self.frame_droit = Frame(self, bg="grey", width=820, height=550)
        self.frame_droit.pack(side='left', fill='x')
        # Titre
        self.label_titre = Label(self.frame_haut, text="GESTION DES ACHATS", font=(FONT_TYPE, FONT_SIZE, TITLE_FONT_WEIGHT),\
             background=LIGHTGREEN, height=3)
        self.label_titre.pack(side="top", fill="x", expand=True, padx=426)
        # Les boutons d'en-pied
        self.frame_bas = Frame(self, bg=LIGHTGREEN, width=1020, height=50)
        self.frame_bas.place(x=0, y=550)
        # Les boutons Ok et Quitter
        self.boutonOk()
        self.boutonQuitter()
        # Le tableau principal
        self.tableau = ttk.Treeview(self.frame_droit, height=487,columns=("Fournisseur", "Telephone", "Adresse", "Mail", "Notes"))
        self.tableau.heading("#0", text="ID")
        self.tableau.heading("Fournisseur", text="Fournisseur")
        self.tableau.heading("Telephone", text="Telephone")
        self.tableau.heading("Adresse", text="Adresse")
        self.tableau.heading("Mail", text="Mail")
        self.tableau.heading("Notes", text="Notes")
        self.tableau.column("#0", width=50)
        self.tableau.column("Fournisseur", width=160)
        self.tableau.column("Telephone", width=140)
        self.tableau.column("Adresse", width=150)
        self.tableau.column("Mail", width=141)
        self.tableau.column("Notes", width=163)
        self.tableau.place(x=0, y=0)
        # Une barre de defilement pour le Treeview
        self.scrollbar = ttk.Scrollbar(self.frame_droit, orient='vertical', command=self.tableau.yview)
        self.scrollbar.place(x=805, y=0, height=487)
        # Lier la barre au Treeview
        self.tableau.config(yscrollcommand=self.scrollbar.set)
        
        # Les style
        self.style  = ttk.Style()
        self.creStyle(self.style)

        # Les boutons du menu gauche
        self.bouton_nouveau_fournisseur = ttk.Button(self.frame_gauche, text="Nouveau fournisseurs", style="Default.TButton")
        self.bouton_nouveau_fournisseur.place(x=1, y=2, bordermode='outside', width=199, height=25)
        self.bouton_fournisseur = ttk.Button(self.frame_gauche, text="Fournisseurs", style="Default.TButton")
        self.bouton_fournisseur.place(x=1, y=27, bordermode='outside', width=199, height=25)
        self.bouton_detail = ttk.Button(self.frame_gauche, text="Details", style="Default.TButton")
        self.bouton_detail.place(x=1, y=52, bordermode='outside', width=199)
        
        self.bouton_nouveau_fournisseur.config(command=self.auClicButtonNouveauFournisseur)
        self.bouton_fournisseur.config(command=self.auClicButtonFournisseur)
        self.bouton_detail.config(command=self.auClicButtonDetail)
        self.protocol("WM_DELETE_WINDOW", self.fermer)

    def fermer(self):
        Achat.charger = False
        self.destroy()

    def boutonOk(self):
        global destroy
        def destroy():
            Achat.charger = False
            self.destroy()

        btn_ok = ttk.Button(self.frame_bas, text="OK", command=destroy)
        btn_ok.place(x=930, y=15)

    def boutonQuitter(self):
        btn_ok = ttk.Button(self.frame_bas, text="Quitter", command=destroy)
        btn_ok.place(x=850, y=15)
    
    def auClicButtonNouveauFournisseur(self):
        print("Nouveau Fournisseur - Active")
        self.bouton_detail.config(style="Default.TButton")
        self.bouton_fournisseur.config(style="Default.TButton")
        self.bouton_nouveau_fournisseur.config(style="Custum1.TButton")
        if Achat.inst_nouveau is None or not Achat.inst_nouveau.winfo_exists():
            Achat.inst_nouveau = fournisseur.NouveauFournisseur(self, self.titre_principal)
            # trouve le bouton OK de la fenetre Nouveau Fournisseur
            for widget in Achat.inst_nouveau.winfo_children():
                if "button" in widget.widgetName:
                    if widget.cget('text') == 'OK':
                        # relie ce bouton a notre methode ajouterFournisseur ici
                        widget.configure(command=self.ajouterFournisseur)
    
    def auClicButtonFournisseur(self):
        print("Fournisseur - Active")
        self.bouton_detail.config(style="Default.TButton")
        self.bouton_fournisseur.config(style="Custum1.TButton")
        self.bouton_nouveau_fournisseur.config(style="Default.TButton")

        # Base de donnee des fournisseurs
        con = sqlite3.connect(path)
        curs = con.cursor()
        curs.execute("SELECT * FROM Fournisseur")
        data = curs.fetchall()

        if Achat.charger is not True:
            for item in data:
                self.tableau.tag_configure("lignepaire", background=LIGHTGREY)
                self.tableau.tag_configure("ligneimpaire", background=LIGHTCYAN)
                tags = ("lignepaire",) if item[0] % 2 == 0 else ("ligneimpaire",)
                self.tableau.insert("", "end", values=(item[1], item[2], item[3], item[4], item[5]), text=str(item[0]), tags=tags)
                Achat.ligne += 1
            con.close()
            Achat.charger = True
            print('Charger: ', Achat.charger)

    
    def auClicButtonDetail(self):
        print("Details - Active")
        self.bouton_detail.config(style="Custum1.TButton")
        self.bouton_fournisseur.config(style="Default.TButton")
        self.bouton_nouveau_fournisseur.config(style="Default.TButton")
        Achat.charger = True
        print('Charger: ', Achat.charger)

    def creStyle(self, obj):
        obj.configure("Default.TButton", anchor='w', font=("Arial", 8))
        obj.configure("Custum1.TButton", font=("Arial", 8,"bold"), anchor='w', background='yellow')
    
    def ajouterFournisseur(self):
        args = (
            Achat.inst_nouveau.entry_nom_fournisseur.get(),
            Achat.inst_nouveau.entry_telephone_fournisseur.get(),
            Achat.inst_nouveau.entry_adresse_fournisseur.get(),
            Achat.inst_nouveau.entry_mail_fournisseur.get(),
            Achat.inst_nouveau.entry_note_fournisseur.get(),
        )

        if all([x != "" for x in args]):
            self.tableau.tag_configure("lignepaire", background=LIGHTGREY)
            self.tableau.tag_configure("ligneimpaire", background=LIGHTCYAN)
            tags = ("lignepaire",) if Achat.ligne % 2 == 0 else ("ligneimpaire",)
            self.tableau.insert("", "end", values=args, text=str(Achat.ligne), tags=tags)
            Achat.ligne += 1

            # ajouter les informations du nouveau fournisseur a la base de donnees
            con = sqlite3.connect(path)
            curs = con.cursor()
            curs.execute("INSERT INTO Fournisseur (fournisseur, telephone, adresse, mail, note) VALUES (?, ?, ?, ?, ?)", (args[0], args[1], args[2], args[3], args[4]))
            con.commit()
            con.close()
        Achat.inst_nouveau.destroy()
        print('Charger: ', Achat.charger)

