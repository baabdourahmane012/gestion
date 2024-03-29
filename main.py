# -*- encoding: utf-8 -*-
import tkinter
from param import *
from tkinter import Label, Button, PhotoImage
from vente import gestion_vente
from achat import gestion_achat
from stock import connexion_bd
from commande import gestion_commande


instance_vente = None
instance_achat = None
instance_stock, instance_bd = None, None
instance_command = None


class App(tkinter.Tk):
    """ Class App """
    
    def __init__(self):
        super().__init__()
        self.titre = 'PyCommerciale'
        self.wm_title(self.titre)
        self.wm_manage(self)
        self.wm_geometry("720x600+300+50")
        self.wm_resizable(False, False)
        self.config(background="cyan")
        self.setMainTitle()
        # self.setButtons(im)
        self.focus()

    # Titre principale
    def setMainTitle(self):
        titre = Label(self, font=(TITLE_FONT_TYPE, TITLE_FONT_SIZE, TITLE_FONT_WEIGHT),
                      text="Application de gestion".upper(), background=LIGHTGREEN, padx=250, pady=80)
        titre.place(x=0, y=0)
    
    # Menu vente
    def setVente(self, vente_image):
        global instance_vente
        # instance_vente = None

        def startVente():
            global instance_vente
            if instance_vente is None or not instance_vente.winfo_exists():
                instance_vente = gestion_vente.Vente(self, self.titre)
                instance_vente.focus()
            
        vente = Button(self, text="Ventes", background=LIGHTCYAN, command=startVente, padx=50, pady=50,
                       font=(BTN_FONT_TYPE, 15, 'normal', 'underline'), relief='groove')
        vente.place(x=190+15, y=250)
        vente.config(image=vente_image)

    # Menu achat
    def setAchat(self, achat_image):
        global instance_achat
        # instance_achat = None

        def startAchat():
            global instance_achat
            if instance_achat is None or not instance_achat.winfo_exists():
                instance_achat = gestion_achat.Achat(self, self.titre)
                instance_achat.focus()

        achat = Button(self, text="Achats", background=LIGHTCYAN, padx=50, pady=50,
                       font=(BTN_FONT_TYPE, 15, 'normal', 'underline'), command=startAchat, relief='groove')
        achat.place(x=385-25, y=250)
        achat.config(image=achat_image)
    
    # Menu stocks
    def setStock(self, stock_image):
        global instance_stock, instance_bd
        # instance_stock, instance_bd = None, None

        def acces_bd():
            global instance_bd
            if instance_bd is None or not instance_bd.winfo_exists():
                instance_bd = connexion_bd.BaseDeDonnee(self, self.titre)
                instance_bd.focus()
        stock = Button(self, text="Stocks", background=LIGHTCYAN, padx=50, pady=50,
                       font=(BTN_FONT_TYPE, 15, 'normal', 'underline'), command=acces_bd, relief='groove')
        stock.place(x=190+15, y=400)
        stock.config(image=stock_image)
    
    # Menu commandes
    def setCommand(self, commande_image):
        global instance_command
        # instance_command = None

        def startCommande():
            global instance_command
            if instance_command is None or not instance_command.winfo_exists():
                instance_command = gestion_commande.Commande(self, self.titre)
                instance_command.focus()

        command = Button(self, text="Commandes", background=LIGHTCYAN, padx=33, pady=50,
                         font=(BTN_FONT_TYPE, 15, 'normal', 'underline'), command=startCommande, relief='groove')
        command.place(x=385-25, y=400)
        command.config(image=commande_image)

    # Make buttons
    def setButtons(self, stock_image, achat_image, vente_image, commande_image):
        self.setStock(stock_image)
        self.setAchat(achat_image)
        self.setVente(vente_image)
        self.setCommand(commande_image)
        # self.setParametrage()
        # self.setComptabilite()


if __name__ == '__main__':
    app = App()
    stock_img = PhotoImage(file="icons/stock.png")
    achat_img = PhotoImage(file="icons/achat.png")
    vente_img = PhotoImage(file="icons/vente.png")
    commande_img = PhotoImage(file="icons/commande.png")
    app.setButtons(stock_img, achat_img, vente_img, commande_img)
    app.mainloop()
