import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import csv
import os
from collections import Counter
from PIL import Image, ImageTk


def calculer_degats(des):
    compte = Counter(des)
    valeurs = sorted(compte.values(), reverse=True)
    des_uniques = sorted(set(des))
    est_suite = len(des_uniques) == 5 and (des_uniques[-1] - des_uniques[0] == 4)

    if valeurs == [5]:
        return "YAHTZEE", 50
    if est_suite:
        return "GRANDE SUITE", 35
    if valeurs == [4, 1]:
        return "CARRÉ", 25
    if valeurs == [3, 2]:
        return "FULL HOUSE", 20
    if valeurs == [3, 1, 1]:
        return "BRELAN", 15
    if valeurs == [2, 2, 1]:
        return "DOUBLE PAIRE", 10
    if valeurs == [2, 1, 1, 1]:
        return "PAIRE", 5
    return "CARTE HAUTE", 2


class PokerDiceBattler:
    def __init__(self, root):
        self.root = root
        self.root.title("Poker-Dice Battler")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)

        self.dice_images = []
        for i in range(1, 7):
            chemin = f"assets/dice_{i}.png"
            if os.path.exists(chemin):
                img = tk.PhotoImage(file=chemin)
                self.dice_images.append(img.subsample(3, 3))
            else:
                self.dice_images.append(None)

        self.bg_image_tk = self.preparer_fond("assets/background.png", 0.4)
        self.afficher_menu()

    def preparer_fond(self, chemin, opacite):
        """Charge l'image, applique la transparence et la convertit pour Tkinter."""
        if os.path.exists(chemin):
            img = Image.open(chemin).convert("RGBA")
            # Modification de l'alpha (transparence)
            alpha = img.getchannel("A")
            new_alpha = alpha.point(lambda i: int(i * opacite))
            img.putalpha(new_alpha)
            return ImageTk.PhotoImage(img)
        return None

    def nettoyer_fenetre(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def afficher_menu(self):
        self.nettoyer_fenetre()
        self.root.configure(bg="#1a1a1a")

        if self.bg_image_tk:
            bg_label = tk.Label(self.root, image=self.bg_image_tk, bg="#1a1a1a")
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(
            self.root,
            text="POKER-DICE BATTLER",
            font=("Arial", 45, "bold"),
            fg="#f1c40f",
            bg="#1a1a1a",
        ).pack(pady=(80, 40))

        container = tk.Frame(
            self.root, bg="#1a1a1a"
        )  # Optionnel : mettre bg="" si transparent
        container.pack()

        options = [
            ("JOUER", self.lancer_partie, "#27ae60"),
            ("RÈGLES", self.afficher_regles, "#2980b9"),
            ("SCOREBOARD", self.afficher_scoreboard, "#8e44ad"),
        ]

        for texte, action, couleur in options:
            btn = tk.Button(
                self.root,
                text=texte,
                command=action,
                font=("Arial", 18, "bold"),
                bg=couleur,
                fg="white",
                width=20,
                height=2,
                bd=0,
                cursor="hand2",
            )
            btn.pack(pady=10)

    def lancer_partie(self):
        self.nettoyer_fenetre()
        couleur_fond_jeu = "#1E90FF"
        self.root.configure(bg=couleur_fond_jeu)

        self.pv_boss = 100
        self.lancers = 0

        self.ui_pv = tk.Label(
            self.root,
            text=f"PV DU BOSS : {self.pv_boss}",
            font=("Arial", 35, "bold"),
            fg="#e74c3c",
            bg=couleur_fond_jeu,
        )
        self.ui_pv.pack(pady=20)

        self.ui_degats = tk.Label(
            self.root,
            text="Dégâts infligés : 0",
            font=("Arial", 25, "bold"),
            fg="#f1c40f",
            bg=couleur_fond_jeu,
        )
        self.ui_degats.pack(pady=10)

        self.cadre_des = tk.Frame(self.root, bg=couleur_fond_jeu)
        self.cadre_des.pack(pady=30)

        self.labels_des = [tk.Label(self.cadre_des, bg="#2c3e50") for _ in range(5)]
        for label in self.labels_des:
            label.pack(side="left", padx=15)

        self.ui_info = tk.Label(
            self.root,
            text="Préparez votre attaque !",
            font=("Arial", 20),
            fg="white",
            bg=couleur_fond_jeu,
        )
        self.ui_info.pack(pady=10)

        tk.Button(
            self.root,
            text="LANCER LES DÉS",
            command=self.jouer_tour,
            font=("Arial", 20, "bold"),
            bg="#e67e22",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2",
        ).pack(pady=20)
        tk.Button(
            self.root,
            text="RETOUR MENU",
            command=self.afficher_menu,
            font=("Arial", 10),
            bg="#34495e",
            fg="white",
            cursor="hand2",
        ).pack(side="bottom", pady=20)

        des_initiaux = [random.randint(1, 6) for _ in range(5)]
        self.afficher_des_visuels(des_initiaux)

    def afficher_regles(self):
        regles = "BUT : Vaincre le Boss (100 PV) avec le moins de lancers.\n\nScore de Poker requis !"
        messagebox.showinfo("Règles", regles)

    def charger_scores(self):
        scores = []
        if os.path.exists("scoreboard.csv"):
            with open("scoreboard.csv", "r", encoding="utf-8") as f:
                reader = csv.reader(f, delimiter=";")
                for ligne in reader:
                    if ligne:
                        scores.append(ligne)
        return scores[:3]

    def afficher_scoreboard(self):
        scores = self.charger_scores()
        texte = "TOP 3 :\n"
        for r, n, s in scores:
            texte += f"{r}. {n} - {s} coups\n"
        messagebox.showinfo("Scores", texte)

    def afficher_des_visuels(self, resultats):
        for i in range(5):
            val = resultats[i]
            img = self.dice_images[val - 1]
            if img:
                self.labels_des[i].config(image=img, text="", width=130, height=130)
            else:
                self.labels_des[i].config(
                    image="",
                    text=str(val),
                    font=("Arial", 40),
                    fg="white",
                    width=3,
                    height=1,
                )

    def jouer_tour(self):
        self.lancers += 1
        res = [random.randint(1, 6) for _ in range(5)]
        self.afficher_des_visuels(res)
        nom, dmg = calculer_degats(res)
        self.pv_boss = max(0, self.pv_boss - dmg)
        self.ui_pv.config(text=f"PV DU BOSS : {self.pv_boss}")
        self.ui_degats.config(text=f"Dégâts infligés : {dmg}")
        self.ui_info.config(text=f"Combo : {nom} !")
        if self.pv_boss <= 0:
            messagebox.showinfo("Victoire", f"Gagné en {self.lancers} coups !")
            self.verifier_highscore()
            self.afficher_menu()

    def verifier_highscore(self):
        scores = self.charger_scores()
        if len(scores) < 3 or self.lancers < int(scores[-1][2]):
            nom = simpledialog.askstring("Record", "Ton nom :") or "Anonyme"
            scores.append(["?", nom, str(self.lancers)])
            scores.sort(key=lambda x: int(x[2]))
            final = [[str(i + 1), s[1], s[2]] for i, s in enumerate(scores[:3])]
            with open("scoreboard.csv", "w", newline="", encoding="utf-8") as f:
                csv.writer(f, delimiter=";").writerows(final)


if __name__ == "__main__":
    fenetre = tk.Tk()
    app = PokerDiceBattler(fenetre)
    fenetre.mainloop()
