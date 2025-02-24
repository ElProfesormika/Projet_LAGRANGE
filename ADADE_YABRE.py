import tkinter as tk
from tkinter import messagebox, scrolledtext
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Fonction d'interpolation de Lagrange
def lagrange_inter(x, p, y):
    n = len(p)
    poly = 0 
    L_base = []
    for i in range(n):
        L_i = 1
        for j in range(n):
            if i != j:
               L_i *= (x - p[j]) / (p[i] - p[j])
        L_base.append(sp.simplify(L_i))
        poly += y[i] * L_i
    return sp.simplify(poly), L_base

# Fonction pour afficher les polynômes de base
def display_lagrange_base(L_base, n):
    result = "Les polynômes de base pour {} points sont:\n".format(n)
    for i, L_i in enumerate(L_base):
        result += f"L_{{{i}}}(x) = {sp.latex(L_i)}\n"
    return result

# Fonction pour afficher le polynôme d'interpolation
def display_lagrange_polynomial(P, n):
    return f"P_{n}(x) = {sp.latex(P)}"

# Ajout de la citation sur chaque page
class Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        
        # Ajout de la citation en haut de la page
        self.citation_frame = tk.Frame(self, bg='#F5F5F5')
        self.citation_frame.pack(side="top", fill="x")

        self.left_citation_label = tk.Label(self.citation_frame, text='"Repenser le déjà pensé et recréer \nle non créé tout en lutant pour devenir\n la cause nouvelle qui cause \nla cause de plusieurs autres,\nc\'est là l\'apanage de mon Esprit"\n- El Professor', font=('Arial', 10), anchor="w", bg='#FFFFFF')
        self.left_citation_label.pack(side="left", padx=(10, 4), pady=(10, 0))

        self.right_citation_label = tk.Label(self.citation_frame, text='UE:MTH1422\nProf: Dr AYELEH\nGroupe(BNG):\nADADE Félicité IA&BD\nYABRE Housséni IA&BD', font=('Bodoni MT Black', 10), anchor="e", bg='#f0f0f0')
        self.right_citation_label.pack(side="right", padx=(4, 10), pady=(0, 10))
        self.citation_label = tk.Label(self, text='@[ADADE et YABRE] Tous droits reservés\n #El Professor', bg='#FFFFFF', font=('Arial', 7))
        self.citation_label.pack(side="bottom", fill="x")

    def show(self):
        self.lift()

# Page de garde avec instructions
class WelcomePage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.configure(bg='#ffcccc')  # Fond multicolore

        # Ajouter un label avec le nom de l'application
        title_label = tk.Label(self, text="Interpolation Polynomiale:Méthode de Lagrange", font=('Bodoni MT Black', 30, 'bold'), bg='#FF7F50')
        title_label.pack(pady=20)

        # Ajouter un texte de description
        description_label = tk.Label(self, text=( "\t\t\t GUIDE : \n"
            "Bienvenue dans l'application d'interpolation de Lagrange!\n"
            "Cette application vous permettra d'interpoler un ensemble de points à l'aide du polynôme de Lagrange.\n\n"
            "Instructions d'utilisation:\n"
            "NB: Pour les champs à remplir, \nrassurez vous d'avoir bien remplie le champs avant de valider\n"
            "1. Entrez le nombre de points.(Valeur entière)\n"
            "2. Saisissez les valeurs de x et y pour chaque point.\n"
            "3. Visualisez les polynômes de base et le polynôme d'interpolation.\n"
            "4. Tracez le graphique correspondant.\n"
            "5. Vous pouvez effectuer une autre opération après avoir tracé le graphique.\n"
            ), justify="left", font=('Bodoni MT Black', 14), bg='#FFB6C1'
        )
        description_label.pack(pady=18)

        # Ajouter un bouton pour commencer
        start_button = tk.Button(self, text="Commencer", command=self.on_start, bg='#FF7F50', font=('Arial', 12))
        start_button.pack(pady=18)

    def on_start(self):
        self.controller.show_page(self.controller.point_entry_page)

# Page de saisie du nombre de points
class PointEntryPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.configure(bg='#e6f7ff')  # Couleur de fond

        tk.Label(self, text="Entrez le Nombre de points(Valeur Entière):", bg='#e6f7ff', font=('Arial', 14)).pack(pady=10)
        self.points_entry = tk.Entry(self)
        self.points_entry.pack(pady=10)
        
        next_button = tk.Button(self, text="Suivant>>", command=self.on_next, bg='#80ccff', font=('Arial', 14))
        next_button.pack(pady=10)
    
    def on_next(self):
        try:
            n = int(self.points_entry.get())
            if n <= 0:
                raise ValueError("Le nombre de points doit être positif (valeur entière).")
            self.controller.n = n
            self.controller.create_value_entries(n)
            self.controller.show_page(self.controller.value_entry_page)
        except ValueError as ve:
            messagebox.showerror("Erreur", str(ve))

# Page de saisie des valeurs de x et y
class ValueEntryPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.configure(bg='#e6ffe6')  # Couleur de fond
        
        self.entries_frame = tk.Frame(self, bg='#e6ffe6')
        self.entries_frame.pack(pady=10)
        
        next_button = tk.Button(self, text="Suivant>>", command=self.on_next, bg='#80ffaa', font=('Arial', 14))
        next_button.pack(pady=10)
    
    def on_next(self):
        try:
            self.controller.x_vals = [float(entry.get()) for entry in self.controller.x_entries]
            self.controller.y_vals = [float(entry.get()) for entry in self.controller.y_entries]
            self.controller.show_page(self.controller.polynomial_display_page)
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides pour x et y.")
    
    def reset_entries(self):
        for entry in self.controller.x_entries + self.controller.y_entries:
            entry.delete(0, tk.END)

# Page d'affichage des polynômes
class PolynomialDisplayPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.configure(bg='#ffffcc')  # Couleur de fond
        
        tk.Label(self, text="Les Polynômes de Lagrange", bg='#ffffcc', font=('Bodoni MT Black', 20)).pack(pady=10)
        
        self.base_polys_text = scrolledtext.ScrolledText(self, width=80, height=10, wrap=tk.WORD)
        self.base_polys_text.pack(pady=10)
        
        self.interpolation_poly_text = scrolledtext.ScrolledText(self, width=80, height=5, wrap=tk.WORD)
        self.interpolation_poly_text.pack(pady=10)
        
        next_button = tk.Button(self, text="Tracer le Graphique", command=self.on_next, bg='#ffcc99', font=('Arial', 14))
        next_button.pack(pady=10)
        
    def on_next(self):
        self.controller.show_page(self.controller.plot_page)
    
    def display(self):
        x = sp.symbols('x')
        P, L_base = lagrange_inter(x, self.controller.x_vals, self.controller.y_vals)
        self.controller.P = P

        self.base_polys_text.delete(1.0, tk.END)
        self.base_polys_text.insert(tk.END, display_lagrange_base(L_base, self.controller.n))
        
        self.interpolation_poly_text.delete(1.0, tk.END)
        self.interpolation_poly_text.insert(tk.END, display_lagrange_polynomial(P, self.controller.n))

    def clear_display(self):
        self.base_polys_text.delete(1.0, tk.END)
        self.interpolation_poly_text.delete(1.0, tk.END)

# Page du graphique
class PlotPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.configure(bg='#e6e6ff')  # Couleur de fond
        
        self.plot_frame = tk.Frame(self, bg='#e6e6ff')
        self.plot_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        self.plot_button = tk.Button(self, text="Cliquez ici pour continuer", command=self.plot, bg='#b3b3ff', font=('Arial', 14))
        self.plot_button.pack(pady=5)
        self.plot_message_label = tk.Label(self, text="", bg='#e6e6ff')  # Ajout d'un label pour le message
        self.plot_message_label.pack(pady=5)  # Placement du label sous le bouton "Tracer"

    def plot(self):
        self.plot_frame.pack_forget()
        self.plot_frame.pack(fill=tk.BOTH, expand=True)
        x = sp.symbols('x')
        p_func = sp.lambdify(x, self.controller.P, modules=['numpy'])
        x_vals = np.linspace(min(self.controller.x_vals), max(self.controller.x_vals), 400)
        y_vals = p_func(x_vals)
        
        # Efface l'ancienne courbe avant de tracer la nouvelle
        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals, label="Polynôme d'interpolation")
        ax.scatter(self.controller.x_vals, self.controller.y_vals, color='red', label='Points')
        ax.legend()
        ax.set_title('Graphique du polynôme d\'interpolation')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        
        # Efface l'ancien graphique s'il existe
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True) 
        
        # Modification du texte du label
        self.plot_message_label.config(text=" Puis Cliquez ↓↓ ")

        # Bouton pour revenir à la page de saisie des points
        back_button = tk.Button(self, text="Faire une autre interpolation", command=self.on_back, bg='#b3b3ff', font=('Arial', 14))
        back_button.pack(pady=5)

    def on_back(self):
        self.controller.show_page(self.controller.loop_page)

# Page pour effectuer une nouvelle interpolation
class LoopPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.configure(bg='#f0e6ff')  # Couleur de fond
        
        self.message_label = tk.Label(self, text="Voulez-vous effectuer une autre interpolation ?", bg='#f0e6ff', font=('Bodoni MT Black', 14))
        self.message_label.pack(pady=20)
        
        yes_button = tk.Button(self, text="Oui", command=self.on_yes, bg='#d9b3ff', font=('Arial', 14))
        yes_button.pack(side="top", pady=(50, 10))

        no_button = tk.Button(self, text="Non", command=self.on_no, bg='#d9b3ff', font=('Arial', 14))
        no_button.pack(side="top", pady=(10, 50))
    
    def on_yes(self):
        self.controller.clear_all()
        self.controller.show_page(self.controller.point_entry_page)
    
    def on_no(self):
        self.controller.root.destroy()

# Gestionnaire de pages principal
class MainApplication(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.pack(side="top", fill="both", expand=True)
        self.root = root
        
        self.n = 0
        self.x_vals = []
        self.y_vals = []
        self.P = None
        
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        
        # Pages
        self.welcome_page = WelcomePage(self.container, self)
        self.point_entry_page = PointEntryPage(self.container, self)
        self.value_entry_page = ValueEntryPage(self.container, self)
        self.polynomial_display_page = PolynomialDisplayPage(self.container, self)
        self.plot_page = PlotPage(self.container, self)
        self.loop_page = LoopPage(self.container, self)
        
        for page in (self.welcome_page, self.point_entry_page, self.value_entry_page, self.polynomial_display_page, self.plot_page, self.loop_page):
            page.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        
        self.show_page(self.welcome_page)
    
    def show_page(self, page):
        page.show()
        if page == self.polynomial_display_page:
            page.display()
        elif page == self.plot_page:
            page.plot()
    
    def clear_all(self):
        self.value_entry_page.reset_entries()
        self.polynomial_display_page.clear_display()

    def create_value_entries(self, n):
        # Détruire les anciens widgets
        for widget in self.value_entry_page.entries_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.value_entry_page.entries_frame, text="Valeurs de x:", bg='#e6ffe6', font=('Arial', 14)).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self.value_entry_page.entries_frame, text="Valeurs de y:", bg='#e6ffe6', font=('Arial', 14)).grid(row=0, column=1, padx=5, pady=5)
        
        self.x_entries = []
        self.y_entries = []
        for i in range(n):
            x_entry = tk.Entry(self.value_entry_page.entries_frame)
            x_entry.grid(row=i + 1, column=0, padx=5, pady=5)
            self.x_entries.append(x_entry)
            y_entry = tk.Entry(self.value_entry_page.entries_frame)
            y_entry.grid(row=i + 1, column=1, padx=5, pady=5)
            self.y_entries.append(y_entry)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Interpolation de Lagrange")
    app = MainApplication(root)
    app.mainloop()

