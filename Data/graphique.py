import matplotlib.pyplot as plt
import SQL.commandes_bd as cbd
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def graphique_BPM(connexion_bd, id_perf, main):
    fig = Figure(figsize=(4, 3), dpi=100)
    ax = fig.add_subplot(111)
    tuples = cbd.get_BPM(connexion_bd, id_perf)
    l_temps, l_BPM = [], []
    for (a,b) in tuples:
        l_BPM.append(a)
        l_temps.append(b)
    ax.plot(l_temps, l_BPM)
    ax.set_title("Evolution du Rythme Cardiaque durant la prestation")
    ax.set_xlabel('Temps depuis le début (s)')
    ax.set_ylabel('BPM')

    canvas = FigureCanvasTkAgg(fig, master=main)
    canvas.draw()
    canvas.get_tk_widget().pack()


def graphique_accelero(connexion_bd, id_perf, main):
    fig = Figure(figsize=(8, 3), dpi=100)
    ax = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    tuples = cbd.get_accelero(connexion_bd, id_perf)
    l_temps, l_accX, l_accY = [], [], []
    for (a,b,c) in tuples:
        l_accX.append(a)
        l_accY.append(b)
        l_temps.append(c)
    ax.plot(l_temps, l_accX, 'b', label='Accélération en X')
    ax2.plot(l_temps, l_accY, 'r', label='Accélération en Y')
    ax.set_title("Evolution de l'accélération de la main sur les axes x et y")
    ax.set_xlabel('Temps depuis le début (s)')
    ax.set_ylabel("Amplitude de l'accélération")
    ax2.set_xlabel('Temps depuis le début (s)')
    ax2.set_ylabel("Amplitude de l'accélération")

    canvas = FigureCanvasTkAgg(fig, master=main)
    canvas.draw()
    canvas.get_tk_widget().pack()


def graphique_niveau(connexion_bd, id_musicien, id_morceau, main):
    fig = Figure(figsize=(4, 3), dpi=100)
    ax = fig.add_subplot(111)
    tuples = cbd.get_perf(connexion_bd, id_musicien, id_morceau)
    l_date, l_niveau = [], []
    for (a, b, c, d, e, f, g, h) in tuples:
        l_date.append(c)
        l_niveau.append(h)
    ax.plot(l_date, l_niveau)
    ax.set_title('Evolution du niveau de ' + tuples[0][0])
    ax.set_xlabel('Date de la prestation')
    ax.set_ylabel('Niveau Estimé')

    canvas = FigureCanvasTkAgg(fig, master=main)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)


def graphique_nb_fausses_notes(connexion_bd, id_musicien, id_morceau,main):
    fig = Figure(figsize=(4, 3), dpi=100)
    ax = fig.add_subplot(111)
    tuples = cbd.get_perf(connexion_bd, id_musicien, id_morceau)
    l_date, l_nombre = [], []
    for (a, b, c, d, e, f, g, h) in tuples:
        l_date.append(c)
        l_nombre.append(d)
    ax.plot(l_date, l_nombre)
    ax.set_title('Evolution du nombre de fausses notes de ' + tuples[0][0])
    ax.set_xlabel('Date de la prestation')
    ax.set_ylabel('Nombre de fausses notes')

    canvas = FigureCanvasTkAgg(fig, master=main)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=1)


def graphique_BPM_moyen(connexion_bd, id_musicien, id_morceau, main):
    fig = Figure(figsize=(4, 3), dpi=100)
    ax = fig.add_subplot(111)
    tuples = cbd.get_perf(connexion_bd, id_musicien, id_morceau)
    l_date, l_BPMmoy = [], []
    for (a, b, c, d, e, f, g, h) in tuples:
        l_date.append(c)
        l_BPMmoy.append(f)
    ax.plot(l_date, l_BPMmoy)
    ax.set_title('BPM Moyen de ' + tuples[0][0] + ' durant sa prestation')
    ax.set_xlabel('Date de la prestation')
    ax.set_ylabel('BPM Moyen')

    canvas = FigureCanvasTkAgg(fig, master=main)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0)


def graphique_precision(connexion_bd, id_musicien, id_morceau, main):
    fig = Figure(figsize=(4, 3), dpi=100)
    ax = fig.add_subplot(111)
    tuples = cbd.get_perf(connexion_bd, id_musicien, id_morceau)
    l_date, l_ratio = [], []
    for (a, b, c, d, e, f, g, h) in tuples:
        l_date.append(c)
        l_ratio.append(int(((e - d) / e if e != 0 else 0) * 100))
    ax.plot(l_date, l_ratio)
    ax.set_title('Evolution du ratio de précision de ' + tuples[0][0])
    ax.set_xlabel('Date de la prestation')
    ax.set_ylabel('Ratio de Précision (en %)')
    ax.set_xlim(l_date[0], l_date[-1])
    ax.set_ylim(0, 100)

    canvas = FigureCanvasTkAgg(fig, master=main)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=1)


def tableau_last(connexion_bd,id_musicien, id_morceau, main):
    data = cbd.get_perf(connexion_bd, id_musicien, id_morceau)[-1]
    nb_fausses_notes = data[3]
    precision = (data[4] - nb_fausses_notes) / data[4] if data[4] != 0 else 0
    BPM_moyen = data[5]
    ancien_niv = data[6]
    niv_estime = data[7]
    fenetre = tk.Frame(main)
    fenetre.pack()
    fauxlabel = tk.Label(fenetre, text=f"Nombre de fausses notes \n{nb_fausses_notes}", bg="#E72E20", font="Arial 15")
    fauxlabel.grid(row=0,column=0, ipadx=74)
    preclabel = tk.Label(fenetre,text=f"Précision \n {int(precision*100)} %",bg="#FF9900", font="Arial 15")
    preclabel.grid(row=0,column=1, ipadx=172)
    bpmlabel = tk.Label(fenetre,text=f"BPM Moyen \n {BPM_moyen} BPM",bg="#EFF828", font="Arial 15")
    bpmlabel.grid(row=1, column=0, ipadx=150)
    if ancien_niv < niv_estime:
        nivlabel = tk.Label(fenetre, text=f"Evolution du niveau \n {ancien_niv} ↗ {niv_estime}", bg="#50FF00", font="Arial 15")
        nivlabel.grid(row=1, column=1, ipadx=115)
    elif ancien_niv == niv_estime:
        nivlabel = tk.Label(fenetre,text=f"Evolution du niveau \n {ancien_niv} = {niv_estime}", bg="#FFFFFF", font="Arial 15")
        nivlabel.grid(row=1, column=1, ipadx=115)
    else:
        nivlabel = tk.Label(fenetre,text=f"Evolution du niveau \n {ancien_niv} ↘ {niv_estime}", bg="#DA6262", font="Arial 15")
        nivlabel.grid(row=1, column=1, ipadx=115)
