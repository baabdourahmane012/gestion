import tkinter
import sqlite3
from tkinter import Entry, ttk, Label, Button, filedialog, LabelFrame, Frame
from param import *


class Stock(tkinter.Toplevel):
    ligne = 1
    index = 0
    y_incr = 135
    background_dyn = CYAN
    db = dict()

    def __init__(self, parent, titre_principal):
        super().__init__(parent)
        self.titre_principal = titre_principal
        self.wm_title(self.titre_principal + "  -  Stocks")
        self.wm_transient(parent)
        self.wm_geometry("752x644+50+45")
        self.setMenu()
        self.setProduit()
        self.setProduitEntry()
        self.setSpace()
        self.setQuantite()
        self.setQuantiteEntry()
        self.setSpace()
        self.setPrix()
        self.setPrixEntry()
        self.setSpace(xspace=30)
        self.modifierBd()
        self.ajouterBd()
        self.validerStock()
        # self.ligneTable(89)
        self.tree = ttk.Treeview(self, height=21, selectmode='browse', columns=('Article', 'Quantite', 'PrixUnitaire', 'Montant'))
        # Ajouter des en-tetes
        self.tree.heading("#0", text="ID")
        self.tree.heading("Article", text="Article")
        self.tree.heading("Quantite", text="Quantite")
        self.tree.heading("PrixUnitaire", text="Prix Unitaire")
        self.tree.heading("Montant", text="Montant")
        # Definir la largeur par defaut des colonnes
        self.tree.column("#0", width=50)
        self.tree.column("Article", width=190, anchor='w')
        self.tree.column("Quantite", width=120, anchor='e')
        self.tree.column("PrixUnitaire", width=185, anchor='e')
        self.tree.column("Montant", width=175, anchor='e')
        self.tree.place(x=5, y=104)

        # Une barre de defilement pour le Treeview
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        # Lier la barre au Treeview
        self.tree.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(x=728, y=103, height=447)
        
        # self.ligneTable(550)
        self.qte_totale = 0
        self.mtn_total = 0

        self.etatStock()
        self.quitter()
        self.enregistrer()
        self.focus()
        
    # menu pour enregistrer les stocks
    def setMenu(self):
        titre = Label(self, font=(FONT_TYPE, FONT_SIZE, TITLE_FONT_WEIGHT),\
             text="GESTION DE STOCKS".upper(), background=LIGHTGREEN, height=3)
        titre.pack(side="top", fill="x")
    
    def setSpace(self, xspace=10, yspace=3):
        titre = Label(self, font=(FONT_TYPE, FONT_SIZE-2, FONT_WEIGHT),\
             text=" ")
        titre.pack(side='left', fill='none', anchor='nw', pady=yspace, padx=xspace)
    
    # Label produit
    def setProduit(self):
        global produit
        produit = Label(self, font=(FONT_TYPE, FONT_SIZE-2, FONT_WEIGHT),\
             text="Produit:")
        produit.pack(side='left', fill='none', anchor='nw', pady=4)
    
    # Produit entry
    def setProduitEntry(self):
        global produit_entry
        produit_entry = ttk.Entry(self, font=(FONT_TYPE, FONT_SIZE-3, FONT_WEIGHT), width=15)
        produit_entry.pack(side='left', fill='none', anchor='nw', pady=4)
    
    # quantite de produit
    def setQuantite(self):
        qte_produit = Label(self, font=(FONT_TYPE, FONT_SIZE-2, FONT_WEIGHT),\
             text="Qte:")
        qte_produit.pack(side='left', fill='none', anchor='nw', pady=4)
    
    # quantite produit entry
    def setQuantiteEntry(self):
        global qte_produit_entry
        qte_produit_entry = ttk.Entry(self, font=(FONT_TYPE, FONT_SIZE-3, FONT_WEIGHT),\
             width=5, justify="right")
        qte_produit_entry.pack(side='left', fill='none', anchor='nw', pady=4)

    # prix produit
    def setPrix(self):
        global prix_produit
        prix_produit = Label(self, font=(FONT_TYPE, FONT_SIZE-2, FONT_WEIGHT),\
             text="Prix:")
        prix_produit.pack(side='left', fill='none', anchor='nw', pady=4)
    
    # prix produit entry
    def setPrixEntry(self):
        global prix_produit_entry
        prix_produit_entry = ttk.Entry(self, font=(FONT_TYPE, FONT_SIZE-3, FONT_WEIGHT),\
             width=15, justify="right")
        prix_produit_entry.pack(side='left', fill='none', anchor='nw', pady=4)
    
    # valider
    def validerStock(self):
        style = ttk.Style()
        style.configure("Custum.TButton", font=("Helvetica", 8))
        btn_valider = ttk.Button(self, text="Valider", style="Custum.TButton", command=self.valider)
        btn_valider.pack(side='right', fill='none', anchor='nw', pady=3, padx=0)

    # Valider
    def valider(self):
        numero = None
        produit = None
        pu = None
        qte = None
        montant = None

        if "" in [produit_entry.get(), qte_produit_entry.get(), prix_produit_entry.get()]:
            self.bell(self)
        elif str(produit_entry.get()).isnumeric():
            self.bell(self)
            produit_entry.focus()
            produit_entry.select_range(0, 'end')

        elif not str(qte_produit_entry.get()).isnumeric():
            self.bell(self)
            qte_produit_entry.focus()
            qte_produit_entry.select_range(0, 'end')

        elif not str(prix_produit_entry.get()).isnumeric():
            self.bell(self)
            prix_produit_entry.focus()
            prix_produit_entry.select_range(0, 'end')

        else:
            # Stock les infromations dans le dictionnaire
            Stock.db[Stock.ligne] = [produit_entry.get(), f'{int(qte_produit_entry.get()):,}', f'{int(prix_produit_entry.get()):,}', f'{int(int(qte_produit_entry.get())*int(prix_produit_entry.get())):,}']
            # Preparer les infromations pour le tableau
            for clef, valeur in Stock.db.items():
                numero, produit, qte, pu, montant = clef, valeur[0], valeur[1], valeur[2], valeur[3]

            # Définissez des configurations de balises pour les arrière-plans
            self.tree.tag_configure("evenrow", background=LIGHTGREY)
            self.tree.tag_configure("oddrow", background=LIGHTCYAN)
            tags = ("evenrow",) if Stock.ligne % 2 == 0 else ("oddrow",)
            self.tree.insert("", "end", values=(produit, qte, pu, montant), text=str(Stock.ligne), tags=tags)
            
            # Recuperer les montants des articles enregistres
            self.mtn_total = [int("".join(valeur[3].split(','))) for valeur in Stock.db.values()]
            # Recuperer les quantites d'articles enregistres
            self.qte_totale = [int("".join(valeur[1].split(','))) for valeur in Stock.db.values()]

            # Label temporaire pour mettre a jour le montant total des articles du stock
            temp_lab_mtn = Label(self.zone, background=CYAN, text=f'{sum(self.mtn_total):,}  CFA')
            temp_lab_mtn.place(x=90, y=27)
            # Label temporaire pour mettre a jour le nombre de produit total enregistrer
            temp_lab_qte = Label(self.zone, background=CYAN, text=f'{sum(self.qte_totale):,}')
            temp_lab_qte.place(x=90, y=2)
            # Incrementer pour la ligne suivante
            Stock.y_incr += 20
            
            Stock.ligne += 1
            print("DB", Stock.db)
            produit_entry.delete(0, len(produit_entry.get()))
            qte_produit_entry.delete(0, len(qte_produit_entry.get()))
            prix_produit_entry.delete(0, len(prix_produit_entry.get()))

    # Modifier bouton
    def modifierBd(self):
        style = ttk.Style()
        style.configure("Custum.TButton", font=("Helvetica", 8))
        btn_editer = ttk.Button(self, text="Modifier", style="Custum.TButton", state='disabled')
        btn_editer.pack(side='right', fill='none', anchor='nw', pady=3, padx=4)
    
    # Modifier bouton
    def ajouterBd(self):
        style = ttk.Style()
        style.configure("Custum.TButton", font=("Helvetica", 8))
        btn_editer = ttk.Button(self, text="Ajouter", style="Custum.TButton")
        btn_editer.pack(side='right', fill='none', anchor='nw', pady=3, padx=4)

    # Enregistrer le stock
    def enregistrer(self):
        global style
        style = ttk.Style()
        style.configure("Enregistrer.TButton", font=("Helvetica", 8), background=GREEN)
        # creer un fichier de base de donnee
        def creerBaseDeDonnee():
            
            # creer une connexion avec la base
            if len(Stock.db) != 0:
                # Ouvrir la boite de dialogue
                chemin_fichier = filedialog.asksaveasfilename(defaultextension='*.db', \
                filetypes=[("Creer un fichier de base de donnees", "*.db")])
                if chemin_fichier:
                    conn = sqlite3.connect(f'{chemin_fichier}')
                    # creer le curseur
                    curseur = conn.cursor()
                    # Creer la table
                    curseur.execute(f'''
                    CREATE TABLE IF NOT EXISTS articles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nomProduit TEXT,
                        quantiteProduit INTEGER,
                        prixUnitaire INTEGER,
                        montantTotal INTEGER
                        )
                ''')
                    for clef, liste_valeurs in Stock.db.items():
                        print(chemin_fichier, liste_valeurs[0])
                        # Inserer les donnees dans la table
                        curseur.execute(f'''
                        INSERT INTO articles (nomProduit, quantiteProduit, prixUnitaire, montantTotal) VALUES (?, ?, ?, ?)
                        ''', (liste_valeurs[0], int("".join(liste_valeurs[1].split(','))), int("".join(liste_valeurs[2].split(','))), int("".join(liste_valeurs[3].split(',')))))
                        # Valider la transaction
                        conn.commit()
                    # Fermer la connexion
                    conn.close()
            else:
                self.bell()
            Stock.index = 0

        bnt_enregistre = ttk.Button(self, text="Enregistrer", style="Enregistrer.TButton", command=creerBaseDeDonnee)
        bnt_enregistre.place(x=670, y=615)
        
    
    # Annuler le stock
    def quitter(self):
        bnt_quitter = ttk.Button(self, text="Quitter", command=self.destroy)
        bnt_quitter.place(x=590, y=615)

    # Etat du stock
    def etatStock(self):
        # global zone       
        self.zone = LabelFrame(self, text='Etat du stock', background=CYAN, foreground=GREEN, width=150)
        self.zone.place(x=5, y=560)
        fram = Frame(self.zone, width=500, height=58, background=CYAN)
        fram.pack()
        capacite = Label(self.zone, text='Quantite totale: ', background=CYAN, foreground=GREEN)
        capacite.place(x=2, y=2)
        montant_lab = Label(self.zone, text=f'Montant total: ', background=CYAN, foreground=GREEN)
        montant_lab.place(x=2, y=27)
