import matplotlib.pyplot as plt
import SQL.commandes_bd as cbd

def graphique_BPM(connexion_bd, id_perf):
    tuples = cbd.get_BPM(connexion_bd, id_perf)
    l_temps, l_BPM = [], []
    l_BPM = []
    for (a,b) in tuples:
        l_BPM.append(a)
        l_temps.append(b)
    plt.title("Evolution du Rythme Cardiaque durant la prestation")
    plt.plot(l_temps, l_BPM)
    plt.xlabel('Temps depuis le début (s)')
    plt.ylabel('BPM')
    plt.show()

def graphique_accelero(connexion_bd, id_perf):
    tuples = cbd.get_accelero(connexion_bd, id_perf)
    l_temps, l_accX, l_accY = [], [], []
    for (a,b,c) in tuples:
        l_accX.append(a)
        l_accY.append(b)
        l_temps.append(c)
        plt.title("Evolution de l'accélération de la main sur les axes x et y")
        plt.plot(l_temps, l_accX, 'b', label='Accélération en X')
        plt.plot(l_temps, l_accY, 'r', label='Accélération en Y')
        plt.legend(loc=8)
        plt.xlabel('Temps depuis le début (s)')
        plt.ylabel("Amplitude de l'accélération")
        plt.show()

def graphique_niveau(connexion_bd, id_perf):
    last_perf, tuples = cbd.get_perf(connexion_bd, id_perf)
    l_date, l_niveau = [], []
    for (a, b, c, d, e, f, g, h) in tuples:
        l_date.append(c)
        l_niveau.append(g)
        plt.title('Evolution du niveau de ' + str(a))
        plt.plot(l_date, l_niveau)
        plt.xlabel('Date de la prestation')
        plt.ylabel('Niveau Estimé')
        plt.show()

def graphique_nb_fausses_notes(connexion_bd, id_perf):
    last_perf, tuples = cbd.get_perf(connexion_bd, id_perf)
    l_date, l_nombre = [], []
    for (a, b, c, d, e, f, g, h) in tuples:
        l_date.append(c)
        l_nombre.append(d)
        plt.title('Evolution du nombre de fausses notes de ' + str(a))
        plt.plot(l_date, l_nombre)
        plt.xlabel('Date de la prestation')
        plt.ylabel('Nombre de fausses notes')
        plt.show()

def graphique_BPM_moyen(connexion_bd, id_perf):
    last_perf, tuples = cbd.get_perf(connexion_bd, id_perf)
    l_date, l_BPMmoy = [], []
    for (a, b, c, d, e, f, g, h) in tuples:
        l_date.append(c)
        l_BPMmoy.append(f)
        plt.title('BPM Moyen de ' + str(a) + ' durant sa prestation')
        plt.bar(l_date, l_BPMmoy)
        plt.xlabel('Date de la prestation')
        plt.ylabel('BPM Moyen')
        plt.show()

def graphique_precision(connexion_bd, id_perf):
    last_perf, tuples = cbd.get_perf(connexion_bd, id_perf)
    l_date, l_ratio = [], []
    for (a, b, c, d, e, f, g, h) in tuples:
        l_date.append(c)
        l_ratio.append(int(e)*100)
        plt.title('Evolution du ratio de précision de ' + str(a))
        plt.bar(l_date, l_ratio)
        plt.xlabel('Date de la prestation')
        plt.ylabel('Ratio de Précision (en %)')
        plt.axis([l_date[0], l_date[-1]], [0, 100])
        plt.show()