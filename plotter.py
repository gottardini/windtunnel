import matplotlib
import matplotlib.pyplot as plt
import numpy as np

class Plotter:
    def __init__(self):
        pass

    def plot(self,xax,yax,titles,ylim=(-3,3)):
        fig, axes = plt.subplots(2,3)
        for i in range(len(yax)):
            axes[int(i/3),i%3 ].plot(xax,yax[i])
            ''' crea un vettore che contiene una forza
                o un momento per ogni acquisizione:
                con x[i] for x in matr prende
                l'iesimo elemento di ogni array x in
                matr (che è un array di array):
                primo array->i-esimo elemento
                secondo array->i-esimo elemento
                ...'''

            axes[int(i/3),i%3].set(title=titles[i])
            axes[int(i/3),i%3].set_ylim(ylim[0],ylim[1])
