import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import os
import subprocess
import sys
from PIL import Image, ImageTk

from logic import calculer_degats
from scoreboard import charger_scores, sauvegarder_score


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

        self.bg_image_tk = self._preparer_fond("assets/background.png", 0.4)
        self.afficher_menu()

    def _preparer_fond(self, chemin, opacite):
        if os.path.exists(chemin):
            img = Image.open(chemin).convert("RGBA")
            alpha = img.getchannel("A")
            img.putalpha(alpha.point(lambda i: int(i * opacite)))
            return ImageTk.PhotoImage(img)
        return None

    def _nettoyer_fenetre(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- Screens ---

    def afficher_menu(self):
        self._nettoyer_fenetre()
        self.root.configure(bg="#1a1a1a")

        if self.bg_image_tk:
            tk.Label(self.root, image=self.bg_image_tk, bg="#1a1a1a").place(
                x=0, y=0, relwidth=1, relheight=1
            )

        tk.Label(
            self.root,
            text="POKER-DICE BATTLER",
            font=("Arial", 45, "bold"),
            fg="#f1c40f",
            bg="#1a1a1a",
        ).pack(pady=(80, 40))

        options = [
            ("JOUER", self.lancer_partie, "#27ae60"),
            ("RÈGLES", self.afficher_regles, "#2980b9"),
            ("SCOREBOARD", self.afficher_scoreboard, "#8e44ad"),
            ("DICE QUEST ↗", self.lancer_dice_quest, "#c0392b"),
        ]

        for texte, action, couleur in options:
            tk.Button(
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
            ).pack(pady=10)

    def lancer_partie(self):
        self._nettoyer_fenetre()
        bg = "#1E90FF"
        self.root.configure(bg=bg)

        self.pv_boss = 100
        self.lancers = 0

        self.ui_pv = tk.Label(
            self.root,
            text=f"PV DU BOSS : {self.pv_boss}",
            font=("Arial", 35, "bold"),
            fg="#e74c3c",
            bg=bg,
        )
        self.ui_pv.pack(pady=20)

        self.ui_degats = tk.Label(
            self.root,
            text="Dégâts infligés : 0",
            font=("Arial", 25, "bold"),
            fg="#f1c40f",
            bg=bg,
        )
        self.ui_degats.pack(pady=10)

        self.cadre_des = tk.Frame(self.root, bg=bg)
        self.cadre_des.pack(pady=30)

        self.labels_des = [tk.Label(self.cadre_des, bg="#2c3e50") for _ in range(5)]
        for label in self.labels_des:
            label.pack(side="left", padx=15)

        self.ui_info = tk.Label(
            self.root,
            text="Préparez votre attaque !",
            font=("Arial", 20),
            fg="white",
            bg=bg,
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

        self._afficher_des_visuels([random.randint(1, 6) for _ in range(5)])

    def afficher_regles(self):
        messagebox.showinfo(
            "Règles",
            "BUT : Vaincre le Boss (100 PV) avec le moins de lancers.\n\nScore de Poker requis !",
        )

    def afficher_scoreboard(self):
        scores = charger_scores()
        texte = "TOP 3 :\n"
        for r, n, s in scores:
            texte += f"{r}. {n} - {s} coups\n"
        messagebox.showinfo("Scores", texte)

    # --- Game loop ---

    def jouer_tour(self):
        self.lancers += 1
        res = [random.randint(1, 6) for _ in range(5)]
        self._afficher_des_visuels(res)
        nom, dmg = calculer_degats(res)
        self.pv_boss = max(0, self.pv_boss - dmg)
        self.ui_pv.config(text=f"PV DU BOSS : {self.pv_boss}")
        self.ui_degats.config(text=f"Dégâts infligés : {dmg}")
        self.ui_info.config(text=f"Combo : {nom} !")
        if self.pv_boss <= 0:
            messagebox.showinfo("Victoire", f"Gagné en {self.lancers} coups !")
            self._verifier_highscore()
            self.afficher_menu()

    def _afficher_des_visuels(self, resultats):
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

    def _verifier_highscore(self):
        scores = charger_scores()
        if len(scores) < 3 or self.lancers < int(scores[-1][2]):
            nom = simpledialog.askstring("Record", "Ton nom :") or "Anonyme"
            sauvegarder_score(nom, self.lancers)

    # --- External game ---

    def lancer_dice_quest(self):
        src_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "random_hackaton", "src"
        )
        subprocess.Popen([sys.executable, "main.py"], cwd=src_dir)
