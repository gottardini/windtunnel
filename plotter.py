import matplotlib
import matplotlib.pyplot as plt
import numpy as np

class Plotter:
    def __init__(self):
        pass

    def plot(self,xax,ydata,labels,figtitle,ylim=(-6,6),xlabel="",ylabel="",scatter=False):
        fig, ax = plt.subplots()
        #print("aa",len(ydata[0]))
        for i in range(len(ydata)):
            if scatter:
                ax.scatter(xax,ydata[i],label=labels[i])
            else:
                ax.plot(xax,ydata[i],label=labels[i])
        ax.legend()
        ax.set(title=figtitle)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_ylim(ylim[0],ylim[1])
