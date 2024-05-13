import tkinter as tk
import random
from tkinter import ttk



# Créer la fenêtre principale
fenetre = tk.Tk()

# Maximiser la fenêtre
fenetre.state("zoomed")

# Ajouter un titre
fenetre.title("Fenêtre en Plein Écran avec Barre 'Range'")

# Personnalisation du style pour les boutons plus grands
style = ttk.Style()
style.configure("Large.TButton", font=("Helvetica", 14))  # Augmentation de la taille de la police

def start(start_value):
    # Fonction utilitaire pour convertir une valeur numérique en code couleur hexadécimal
    def color_from_value(value, valeur_max):
        ratio = value / valeur_max
        red = int(255 * ratio)
        green = int(255 * (1 - ratio))
        color = f"#{red:02x}{green:02x}00"
        return color

    valeur_max1 = 60

    # Créer un cadre pour organiser les widgets
    frame = tk.Frame(fenetre, padx=40, pady=40)  # Augmentation du padding
    frame.grid(row=0, column=0, padx=40, pady=40)  # Plus de padding entre le cadre et la fenêtre principale


    value = 0
    # Fonction pour mettre à jour la difficulté
    def update_difficulty(val):
        global value

        value = int(val)
        value2 = value - 10
        valeur_max = valeur_max1 - 10
        color = color_from_value(value2, valeur_max - 10)

        if value2 < valeur_max / 5:
            text = "DÉBUTANT"
        elif valeur_max / 5 <= value2 < valeur_max / 5 * 2:
            text = "AMATEUR"
        elif valeur_max / 5 * 2 <= value2 < valeur_max / 5 * 3:
            text = "INTERMÉDIAIRE"
        elif valeur_max / 5 * 3 <= value2 < valeur_max / 5 * 4:
            text = "CONFIRMÉ"
        else:
            text = "EXPERT"

        difficulty_label.config(text=text, bg=color)

    # Échelle pour ajuster la difficulté
    range_scale = tk.Scale(
        frame,
        from_=10,
        to=valeur_max1,
        orient="horizontal",
        label="Régler la Difficulté",
        command=update_difficulty,
        showvalue=True,  # Afficher la valeur sur l'échelle
        length=600,  # Allongement de l'échelle
        font=("Helvetica", 14),  # Taille de la police de l'étiquette
    )

    # Positionnement initial du curseur
    range_scale.set(start_value)

    range_scale.grid(row=1, column=0, columnspan=2, pady=20)

    # Étiquette pour afficher la difficulté
    difficulty_label = tk.Label(
        frame, text="DÉBUTANT", font=("Helvetica", 18), bg=color_from_value(10, valeur_max1), padx=10, pady=10
    )
    difficulty_label.grid(row=2, column=0, columnspan=2, pady=20)

    value_sudoku = 11
    # Fonction de rappel pour le bouton "Valider"
    def valider():
        global value, value_sudoku

        try:
            if value >= 10:
                value_sudoku = value
            else:
                value_sudoku = 30
        except:
            value_sudoku = 10

        value_sudoku = value
        # Supprimer tout le contenu du cadre sauf le bouton de quitter
        for widget in frame.winfo_children():
            widget.grid_forget()  # Effacement des widgets utilisant grid()


        sudoku_app(value_sudoku)


    # Bouton "Valider"
    valider_button = ttk.Button(
        frame, text="Valider", command=valider, style="Large.TButton"
    )
    valider_button.grid(row=3, column=0, columnspan=2, pady=20)





def sudoku_app(num_clues):
    global value_sudoku
    rejouer_valeur = num_clues


    # Création de la fenêtre principale
    #fenetre = tk.Tk()
    #fenetre.title("Sudoku")

    # Taille des cases et de la grille
    TAILLE_CASE = 55  # Taille des cases
    TAILLE_BORDURE = 2  # Taille des bordures
    GRILLE_TAILLE = TAILLE_CASE * 9  # Taille totale de la grille

    # Création du canevas
    canvas = tk.Canvas(fenetre, width=GRILLE_TAILLE, height=GRILLE_TAILLE)
    canvas.grid(row=0, column=0, padx=10, pady=10)

    # Fonction pour dessiner des lignes
    def draw_line(x1, y1, x2, y2, width):
        canvas.create_line(x1, y1, x2, y2, width=width, fill="black")


    def est_sudoku_valide2(grille, ligne, colonne, chiffre):

        if grille[ligne][colonne] == 'X':
            # Vérifier la ligne
            if chiffre in grille[ligne]:
                return False

            # Vérifier la colonne
            for i in range(9):
                if grille[i][colonne] == chiffre:
                    return False

            # Vérifier le carré 3x3
            # Trouver le début du carré 3x3
            debut_ligne = (ligne // 3) * 3
            debut_colonne = (colonne // 3) * 3
            for i in range(3):
                for j in range(3):
                    if grille[debut_ligne + i][debut_colonne + j] == chiffre:
                        return False

            return True
        else:
            print('un élément est déjà dans cette case')
            return True

    def sudoku_creat(num_clues):
        nombre_none = 0

        grille = [[None for _ in range(9)] for _ in range(9)]

        l = 0

        while l <= 8:
            c = 0
            while c <= 8:

                choice = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                # print(f"grille {grille}")

                # print("test colonne :")
                # récupérer la colonne
                colonne = [ligne[c] for ligne in grille if ligne[c] is not None]

                # print(f"colonne : {colonne}")

                # supprimer des chois la colonne
                choice = [x for x in choice if x not in colonne]

                # print("\n")
                # print("test 3x3 :")

                start_row = (l // 3) * 3
                start_col = (c // 3) * 3

                for i in range(3):
                    for j in range(3):
                        element_carre = grille[start_row + i][start_col + j]
                        if element_carre != None:
                            # print(" ")
                            # print(f"choice3X3 : {choice}")
                            # print(element_carre)
                            if element_carre in choice:
                                choice.remove(element_carre)
                                # print(f"choice3X3_ : {choice}")

                # print("\n")
                # print("test ligne :")

                choice = [x for x in choice if x not in grille[l]]

                # print(f"choice : {choice}")

                if len(choice) >= 1:
                    # choisire un chiffre
                    chiffre = random.choice(choice)

                    # ajouter un chiffre
                    grille[l][c] = chiffre


                else:
                    nombre_none += 1
                    grille[l] = [None, None, None, None, None, None, None, None, None]
                    c = -1

                if nombre_none > 2000:
                    grille = [[None for _ in range(9)] for _ in range(9)]

                # if nombre_none % 5000 == 0:
                #    print("\n")
                #    for ligne in grille:
                #        print(ligne)

                c += 1
            l += 1

        def est_sudoku_valide(grille):
            # Vérifier les rangées
            for row in grille:
                if len(set(row)) != 9:  # La longueur de l'ensemble doit être 9 (chiffres uniques)
                    return False

            # Vérifier les colonnes
            for col in range(9):
                colonne = [grille[row][col] for row in range(9)]
                if len(set(colonne)) != 9:
                    return False

            # Vérifier les blocs 3x3
            for i in range(3):
                for j in range(3):
                    start_row = i * 3
                    start_col = j * 3
                    bloc = [
                        grille[start_row + r][start_col + c]
                        for r in range(3)
                        for c in range(3)
                    ]
                    if len(set(bloc)) != 9:
                        return False

            # Si tout est correct, la grille est un Sudoku valide
            return True

        def sudoku(grille, num_clues2):

            indices = [(r, c) for r in range(9) for c in range(9)]
            random.shuffle(indices)
            for i in range(num_clues2):
                row, col = indices.pop()
                grille[row][col] = "X"

            return grille

        if est_sudoku_valide(grille):

            return sudoku(grille, num_clues)
        else:
            print("X")


    # Dessin de la grille
    for i in range(10):
        width = 4 if i % 3 == 0 else 1
        draw_line(0, i * TAILLE_CASE, GRILLE_TAILLE, i * TAILLE_CASE, width)
        draw_line(i * TAILLE_CASE, 0, i * TAILLE_CASE, GRILLE_TAILLE, width)

    # Dessin des bordures extérieures
    draw_line(0, 3, 500, 3, 4)
    draw_line(3, 0, 3, 500, 4)

    # Grille de Sudoku
    sudoku_grid = sudoku_creat(num_clues)

    # Fonction pour valider le texte saisi et mettre à jour la grille
    def valider_texte(event, row, col):
        texte = event.widget.get()  # Récupère le texte du champ d'entrée

        #if texte == "":
        #    event.widget.config(bg="white")  # Couleur de fond blanche si valide

        if texte.isdigit() and 1 <= int(texte) <= 9 or texte == "":  # Vérifie si c'est un chiffre valide
            if texte != "":
                chiffre_tester = int(texte)
                print("teste")
                if est_sudoku_valide2(sudoku_grid, row, col, chiffre_tester):
                    event.widget.config(bg="#f0f0f0")  # Couleur de fond blanche si valide
                    sudoku_grid[row][col] = chiffre_tester


                else:
                    print("faut")
                    event.widget.config(bg="red")  # Couleur de fond rouge si invalide
            else:
                sudoku_grid[row][col] = texte
                event.widget.config(bg="#f0f0f0")  # Couleur de fond blanche si valide

        else:
            sudoku_grid[row][col] = 'X'  # Remet à 'X' si l'entrée est invalide
            event.widget.config(bg="red")  # Couleur de fond rouge si invalide

    # Placement des champs d'entrée ou des étiquettes selon la grille
    for row in range(9):  # Correctement utiliser la variable 'row' pour la ligne
        for col in range(9):  # Correctement utiliser 'col' pour la colonne
            if sudoku_grid[row][col] == 'X':  # Si la case est vide
                entry = tk.Entry(
                    canvas,
                    width=2,
                    font=("Arial", 18),
                    fg="black",
                    justify="center",
                    bg="#f0f0f0"
                )
                # Utilisez row pour la coordonnée y et col pour la coordonnée x
                canvas.create_window(
                    col * TAILLE_CASE + TAILLE_CASE // 2,  # 'col' détermine la position x
                    row * TAILLE_CASE + TAILLE_CASE // 2,  # 'row' détermine la position y
                    window=entry
                )
                # Ajout d'un événement pour la validation du texte
                entry.bind("<KeyRelease>", lambda event, r=row, c=col: valider_texte(event, r, c))
            else:
                canvas.create_text(
                    col * TAILLE_CASE + TAILLE_CASE // 2,  # 'col' pour la position x
                    row * TAILLE_CASE + TAILLE_CASE // 2,  # 'row' pour la position y
                    text=str(sudoku_grid[row][col]),
                    font=("Arial", 18)
                )

    def rejouer():
        print(value_sudoku)
        canvas.delete("all")

        start(value_sudoku)

    # Créer un cadre pour organiser les widgets
    frame2 = tk.Frame(fenetre, padx=40, pady=10)  # Augmentation du padding
    frame2.grid(row=0, column=10, padx=20, pady=40)  # Plus de padding entre le cadre et la fenêtre principale

    # Personnalisation du style pour le bouton "Rejouer"
    style.configure("LargeRejouer.TButton",
                    font=("Helvetica", 16))  # Ajustement de la taille de la police pour le bouton "Rejouer"

    # Ajouter le bouton "Rejouer"
    rejouer_button = ttk.Button(
        frame2, text="Rejouer", command=rejouer, style="LargeRejouer.TButton"
    )
    rejouer_button.grid(row=10, column=0, columnspan=2, pady=20)

start(10)
# Lancement de la boucle principale
fenetre.mainloop()
