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
        plt.plot(l_temps, l_accX, 'b')
        plt.plot(l_temps, l_accY, 'r')
        plt.xlabel('Temps depuis le début (s)')
        plt.ylabel("Amplitude de l'accélération")
        plt.show()
