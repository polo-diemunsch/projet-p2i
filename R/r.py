import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Créer une fenêtre Tkinter
fenetre = tk.Tk()
fenetre.title("Graphique Matplotlib dans Tkinter")

# Créer une figure et des axes
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 2, 3])

# Créer un widget Canvas Tkinter pour le graphique
canvas = FigureCanvasTkAgg(fig, master=fenetre)
canvas.draw()

# Afficher le widget Canvas
canvas.get_tk_widget().pack()

# Lancer la boucle principale Tkinter
fenetre.mainloop()
