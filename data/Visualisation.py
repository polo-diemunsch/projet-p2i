import SQL.commandes_bd as cbd
import tkinter as tk
 def tableau_last(connexion_bd,id_musicien,id_morceau):
     data = cbd.get_perf(connexion_bd,id_musicien,id_morceau)[0]
     root = tk.Tk()
     nb_fausses_notes = data[3]
     precision = data[4]
     BPM_moyen = data[5]
     ancien_niv = data[6]
     niv_estime = data[7]
     fenetre = tk.Frame(root)
     fenetre.pack()
     fauxlabel = tk.Label(fenetre,text = f"Nombre de fausses notes \n{nb_fausses_notes}",bg = "#E72E20", font = "Arial 15")
     fauxlabel.grid(row = 0,column = 0,ipadx=74)
     preclabel = tk.Label(fenetre,text = f"Précision \n {precision*100} %",bg = "#FF9900", font = "Arial 15")
     preclabel.grid(row = 0,column = 1,ipadx=172)
     bpmlabel = tk.Label(fenetre,text = f"BPM Moyen \n {BPM_moyen} BPM",bg = "#EFF828", font = "Arial 15")
     bpmlabel.grid(row = 1, column = 0,ipadx = 150)
     if ancien_niv < niv_estime:
            nivlabel = tk.Label(fenetre,text = f"Evolution du niveau \n {ancien_niv} ↗ {niv_estime}",bg = "#50FF00", font = "Arial 15")
            nivlabel.grid(row=1,column=1,ipadx=115)
     elif ancien_niv == niv_estime:
            nivlabel = tk.Label(fenetre,text = f"Evolution du niveau \n {ancien_niv} = {niv_estime}",bg = "#FFFFFF", font = "Arial 15")
            nivlabel.grid(row=1,column=1,ipadx=115)
     else:
            nivlabel = tk.Label(fenetre,text = f"Evolution du niveau \n {ancien_niv} ↘ {niv_estime}",bg = "#DA6262", font = "Arial 15")
            nivlabel.grid(row=1,column=1,ipadx=115)
