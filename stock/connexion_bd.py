import tkinter
import sqlite3
from tkinter import Entry, ttk, Label, Button, filedialog, Listbox, messagebox
from stock import gestion_stock
from param import *


instance_stock = None
modifieur, ajouteur, ajouts, quantite, mont = [None for _ in range(5)]
entrees, id_tree = None, None


class BaseDeDonnee(tkinter.Toplevel):
    """ Classe BaseDeDonnee pour gerer les articles: nom, quantite, prix unitaire, montant """
    qte, mtn = [], []

    def __init__(self, parent, titre_principal):
        super().__init__(parent)
        # Titre principale de la fenetre principale
        self.titre_principal = titre_principal
        self.wm_title(self.titre_principal + "  -  BASE DE DONNEE")
        self.wm_transient(parent)
        # Configurer la geometrie de la fenetre
        self.wm_geometry("500x150+350+150")
        # Impecher l'utilisateur de redimentionner la fenetre
        self.wm_resizable(False, False)
        self.config(background=CYAN)
        self.fichier_bd = None
        self.setMenu()
        self.creerUneBd()
        self.ouvrirUneBd()

    # menu pour enregistrer les stocks
    def setMenu(self):
        titre = Label(self, font=(FONT_TYPE, FONT_SIZE, TITLE_FONT_WEIGHT),
                      text="BASES DE DONNEE".upper(), background=LIGHTGREEN, height=3)
        titre.pack(side="top", fill="x")
    
    # Creer une base de donnee
    def creerUneBd(self):
        # global startStock
        instance_stock = None

        # methode pour creer l'instance de la fenetre qui gere la BD
        def startStock():
            global instance_stock
            # instance_stock = None
            if instance_stock is None or not instance_stock.winfo_exists():
                instance_stock = gestion_stock.Stock(self, self.titre_principal)
            
            for widget in instance_stock.winfo_children():
                if "button" in widget.widgetName:
                    if widget.cget('text') == 'Ajouter':
                        widget.forget()

        btn_creer = ttk.Button(self, text="Nouveau", command=startStock)
        btn_creer.pack(side="left", fill='x', expand=1, padx=50)

    # Ouvrir une base de donnee
    def ouvrirUneBd(self):
        # global startStock
        instance_stock = None

        def startStock():
            global instance_stock, modifieur, ajouteur, ajouts, quantite, mont
            instance_stock = None
            ajouts = []
            quantite = []
            mont = []

            if instance_stock is None or not instance_stock.winfo_exists():
                instance_stock = gestion_stock.Stock(self, self.titre_principal)

                # Ajouteur
                def ajouteur():
                    # global ajouterElement
                    data = []
                    entrees = []
                    # nomProd, qteProd, prixProd, mtnProd = None, None, None, None
                    
                    def ajouterElement():
                        
                        conn = sqlite3.connect(f"{self.fichier_bd}")
                        cur = conn.cursor()
                        if len(ajouts) != 0:
                            for ligne in ajouts:
                                cur.execute(
                                    """INSERT INTO articles (nomProduit, quantiteProduit, prixUnitaire, montantTotal) 
                                    VALUES (?, ?, ?, ?)
                                    """, (ligne[0], ligne[1], ligne[2], ligne[3]))
                            conn.commit()
                        conn.close()
                        
                        messagebox.showinfo(parent=instance_stock, title="Sauvegarde",
                                            message="Sauvegarder avec succes.")

                    for widget in instance_stock.winfo_children():
                        if "entry" in widget.widgetName:
                            if widget.get() != "":
                                if widget.get().isnumeric():
                                    data.append(f"{int(widget.get()):,}")
                                else:
                                    data.append(widget.get())
                                entrees.append(widget)
                                for autre_widget in instance_stock.winfo_children():
                                    if "button" in autre_widget.widgetName and autre_widget.cget('text') == 'OK':
                                        autre_widget.config(command=ajouterElement, text='Enregistrer')
                            else:
                                instance_stock.bell()

                    if len(data) != 0:
                        instance_stock.tree.tag_configure("evenrow", background=LIGHTGREY)
                        instance_stock.tree.tag_configure("oddrow", background=LIGHTCYAN)
                        tags = ("evenrow",) if instance_stock.ligne % 2 == 0 else ("oddrow",)
                        # qte = int(f"{''.join(data[1].split(','))}")
                        montant = int(f"{''.join(data[1].split(','))}") * int(f"{''.join(data[2].split(','))}")
                        instance_stock.tree.insert('', 'end', text=instance_stock.ligne, values=(
                            data[0], data[1], data[2], f'{montant:,}'), tags=tags)
                        nomProd, qteProd, prixProd, mtnProd = data[0], data[1], data[2], montant
                        ajouts.append([
                            nomProd,
                            int(''.join(qteProd.split(','))),
                            int(''.join(prixProd.split(','))),
                            montant
                            ])
                        mont.append(ajouts[instance_stock.index][3])
                        quantite.append(ajouts[instance_stock.index][1])

                        entrees[0].delete(0, len(entrees[0].get()))
                        entrees[1].delete(0, len(entrees[1].get()))
                        entrees[2].delete(0, len(entrees[2].get()))
                        instance_stock.ligne += 1
                        
                        # Ouvrir une connexion sqlite3 pour recalculer la qte totale et le montant total
                        if self.fichier_bd:
                            con = sqlite3.connect(f"{self.fichier_bd}")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM articles")
                            data = cur.fetchall()
                            qte_totale, mtn_total = [], []
                            for d in data:
                                qte_totale.append(d[2])
                                mtn_total.append(d[4])
                            con.close()
                            
                            # print("data:", data)
                            # print("Avant append - QTE:", qte_totale)
                            # qte_totale.append(qte)
                            # print("Qte total: ", qte_totale + quantite)
                            # print("Mtn total:", mtn_total + mont)
                            # mtn_total.append(montant)
                            # print("Apres append - QTE:", qte_totale)
                            # print("Nouvel QTE dans ajouts:", ajouts[instance_stock.index][1])
                            # print("Ajouts:", ajouts)
                            # print("Index:", instance_stock.index)
                            instance_stock.index += 1

                            BaseDeDonnee.qte, BaseDeDonnee.mtn = qte_totale + quantite, mtn_total  + mont                          
                            # Label quantite totale
                            c = " "*50
                            clean_lab_qte = Label(instance_stock.zone, background=CYAN, text=f'{c}')
                            clean_lab_qte.place(x=90, y=2)
                            
                            temp_lab_qte = Label(instance_stock.zone, background=CYAN,
                                                 text=f'{sum(BaseDeDonnee.qte):<20,}')
                            temp_lab_qte.place(x=90, y=2)
                            # Label montant total
                            clean_lab_mtn = Label(instance_stock.zone, background=CYAN, text=f'{c}')
                            clean_lab_mtn.place(x=90, y=27)
                            
                            temp_lab_mtn = Label(instance_stock.zone, background=CYAN,
                                                 text=f'{sum(BaseDeDonnee.mtn):<20,}FCFA')
                            temp_lab_mtn.place(x=90, y=27)
                            temp_lab_mtn.forget()

                # Parcourir les widgets
                for widget in instance_stock.winfo_children():
                    # chercher les widget de type Button
                    if "button" in widget.widgetName:
                        # chercher les widget de type Button avec des noms specifiques
                        if widget.cget('text') == "Enregistrer":
                            widget.config(text="OK")
                            widget.config(command=instance_stock.destroy)
                        elif widget.cget('text') == "Valider":
                            widget.forget()
                        elif widget.cget("text") == "Ajouter":
                            widget.config(command=ajouteur)

                # modifier la base de donnee
                def modifieur(event):
                    # global editer
                    # l'id de la selection
                    item_id = instance_stock.tree.identify("item", event.x, event.y)
                    id_selectionner = instance_stock.tree.selection()[0]
                    # print(instance_stock.tree.item(item_id, "values"))
                    entries = iter(list(instance_stock.tree.item(item_id, "values")))
                    
                    # modifier la base de donnee
                    def editer():
                        global entrees, id_tree
                        id_tree = instance_stock.tree.item(id_selectionner, "text")
                        entrees = [widget for widget in instance_stock.winfo_children() if "entry" in widget.widgetName]

                        instance_stock.tree.item(item_id,
                                                 values=((instance_stock.tree.item(item_id, "values")[0],
                                                          instance_stock.tree.item(item_id, "values")[1],
                                                          instance_stock.tree.item(item_id, "values")[2],
                                                          f"""{(int(''.join((entrees[1].get()).split(','))) * 
                                                                int(''.join((entrees[2].get()).split(',')))):,}""")))
                        instance_stock.tree.item(item_id,
                                                 values=((instance_stock.tree.item(item_id, "values")[0],
                                                          instance_stock.tree.item(item_id, "values")[1],
                                                          f"""{int(''.join((entrees[2].get()).split(','))):,}""",
                                                          instance_stock.tree.item(item_id, "values")[3])))
                        instance_stock.tree.item(item_id, values=((instance_stock.tree.item(item_id, "values")[0],
                                                                   f"""{int(''.join((entrees[1].get()).split(','))):,}
""", instance_stock.tree.item(item_id, "values")[2], instance_stock.tree.item(item_id, "values")[3])))
                        instance_stock.tree.item(item_id, values=((entrees[0].get(),
                                                                   instance_stock.tree.item(item_id, "values")[1],
                                                                   instance_stock.tree.item(item_id, "values")[2],
                                                                   instance_stock.tree.item(item_id, "values")[3])))
                        # Vider les entrees apres validation de la modification
                        # for data in entrees:
                        #     data.delete(0, len(data.get()))
                        # print('editer')
                        # ## Mettre a jour la base de donnee apres modification de la Treeview
                        if self.fichier_bd is not None:
                            conn = sqlite3.connect(f'{self.fichier_bd}')
                            if self.fichier_bd:
                                # Cre le curseur
                                cur = conn.cursor()
                                entree = iter(entrees)
                                cur.execute("UPDATE articles SET nomProduit = ? WHERE id = ?", (entree.__next__().get(), int(id_tree)))
                                cur.execute("UPDATE articles SET quantiteProduit = ? WHERE id = ?", (str("".join((entree.__next__().get()).split(','))), int(id_tree)))
                                cur.execute("UPDATE articles SET prixUnitaire = ? WHERE id = ?", (str("".join((entree.__next__().get()).split(','))), int(id_tree)))
                                cur.execute("UPDATE articles SET montantTotal = ? WHERE id = ?", (int("".join((entrees[1].get()).split(',')))*int("".join((entrees[2].get()).split(','))), int(id_tree)))
                                conn.commit()
                                conn.close()
            
                                # Vider les entrees apres validation de la modification
                                for data in entrees:
                                    data.delete(0, len(data.get()))

                                # Nouvelle connexion
                                conn = sqlite3.connect(f'{self.fichier_bd}')
                                curseur = conn.cursor()
                                curseur.execute(f"SELECT * FROM articles")
                                data = curseur.fetchall()
                                qte_totale, mtn_total = [], []
                                for colonne in data:
                                    qte_totale.append(colonne[2])
                                    mtn_total.append(colonne[4])
                                conn.close()

                                BaseDeDonnee.qte, BaseDeDonnee.mtn = qte_totale, mtn_total                           
                                # Label quantite totale
                                c = " "*50
                                clean_lab_qte = Label(instance_stock.zone, background=CYAN, text=f'{c}')
                                clean_lab_qte.place(x=90, y=2)
                                
                                temp_lab_qte = Label(instance_stock.zone, background=CYAN, text=f'{sum(BaseDeDonnee.qte):<20,}')
                                temp_lab_qte.place(x=90, y=2)
                                # Label montant total
                                clean_lab_mtn = Label(instance_stock.zone, background=CYAN, text=f'{c}')
                                clean_lab_mtn.place(x=90, y=27)
                                
                                temp_lab_mtn = Label(instance_stock.zone, background=CYAN, text=f'{sum(BaseDeDonnee.mtn):<20,}FCFA')
                                temp_lab_mtn.place(x=90, y=27)
                                temp_lab_mtn.forget()
                    
                    for widget in instance_stock.winfo_children():
                        # chercher les widget de type Entry
                        if "entry" in widget.widgetName:
                            widget.config(state="normal")
                            print(widget.widgetName)
                            if widget.get() is not None:
                                widget.delete(0, len(widget.get()))
                                try:
                                    widget.insert('end', "".join(entries.__next__().split(',')))
                                except StopIteration:
                                    widget.bell()
                        elif "button" in widget.widgetName:
                            widget.config(state='normal')
                            if widget.cget('text') == 'Modifier':
                                widget.config(command=editer)
                                print(instance_stock.tree.item(item_id, "values"))

                    
                instance_stock.tree.bind('<Double-1>', modifieur)

                # Ouvrir le fichier de base de donnees
                chemin_fichier = filedialog.askopenfilename(
                    title="Choisir une base de donnee",
                    filetypes=[("Fichiers base de donnee", "*.db")]
                    )
                self.fichier_bd = chemin_fichier
                instance_stock.focus()
                # Ouvrir une connexion
                conn = sqlite3.connect(f'{chemin_fichier}')
                if chemin_fichier:
                    curseur = conn.cursor()
                    curseur.execute(f"SELECT * FROM articles")
                    data = curseur.fetchall()
                    qte_totale, mtn_total = [], []
                    for valeurs in data:
                        # Définissez des configurations de balises pour les arrière-plans
                        instance_stock.tree.tag_configure("evenrow", background=LIGHTGREY)
                        instance_stock.tree.tag_configure("oddrow", background=LIGHTCYAN)
                        tags = ("evenrow",) if instance_stock.ligne % 2 == 0 else ("oddrow",)
                        instance_stock.tree.insert("", "end", text=str(valeurs[0]), values=(valeurs[1], f'{valeurs[2]:,}', f'{valeurs[3]:,}', f'{valeurs[4]:,}'), tags=tags)
                        instance_stock.ligne += 1
                        qte_totale.append(valeurs[2])
                        mtn_total.append(valeurs[4])
                    conn.close()

                    BaseDeDonnee.qte, BaseDeDonnee.mtn = qte_totale, mtn_total
                    # Label quantite totale
                    temp_lab_qte = Label(instance_stock.zone, background=CYAN, text=f'{sum(BaseDeDonnee.qte):<20,}')
                    temp_lab_qte.place(x=90, y=2)
                    # Label montant total
                    temp_lab_mtn = Label(instance_stock.zone, background=CYAN, text=f'{sum(BaseDeDonnee.mtn):<20,}FCFA')
                    temp_lab_mtn.place(x=90, y=27)
                    temp_lab_mtn.forget()

        btn_ouvrir = ttk.Button(self, text="Ouvrir", command=startStock)
        btn_ouvrir.pack(side="left", fill='x', expand=1, padx=50)
