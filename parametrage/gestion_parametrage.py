import tkinter


class Parametrage(tkinter.Toplevel):

    def __init__(self, parent, titre_principal):
        super().__init__(parent)
        self.titre_principal = titre_principal
        self.wm_title(self.titre_principal + "  -  Parametrage")
        self.wm_transient(parent)
        self.wm_geometry("720x600+50+50")
