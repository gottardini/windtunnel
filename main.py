import sys
import numpy as np
import plotter
import filter
import scipy.fftpack

vals=["Fx","Fy","Fz","Tx","Ty","Tz",]
filters=[(5,125,1),
         (5,125,1),
         (5,125,1),
         (5,125,1),
         (5,125,1),
         (5,125,1),]

if __name__=="__main__":
    #print(sys.argv)
    if len(sys.argv) == 2:
        matr =[[float(y[1:-1]) for y in x.split(',')[3:-1]] for x in open(sys.argv[1]).read().split('\n')[8:-1]]
        #print(matr)
        ###ANALISI DATI
        x = np.arange(0, len(matr))

        #Prima finestra
        prima=plotter.Plotter()
        y=[[yaa[i] for yaa in matr] for i in range(6)]
        prima.plot(x,y,vals)

        #Seconda Finestra
        seconda=plotter.Plotter()
        yfiltered=[filter.filter_binding(y[i],filters[i]) for i in range(6)]
        seconda.plot(x,yfiltered,vals)
        """
        #Seconda finestra
        seconda=plotter.Plotter()
        # Number of samplepoints
        N = len(matr)
        # sample spacing
        T = 1 / 125
        yf = [scipy.fftpack.fft(y[i]) for i in range(6)]
        yf = [2.0 / N * np.abs(yf[i][:N // 2]) for i in range(6)]
        xf = np.linspace(0.0, 1.0 / (2.0 * T), N / 2)
        seconda.plot(xf,yf,vals)

        yf1filtrato=[(sig if sig>0.05 else 0) for sig in yf[0]]
        y1filtrato=scipy.fftpack.ifft(yf1filtrato)
        y[0]=y1filtrato

        """
        plotter.plt.show()

    else:
        raise ValueError("Specifica il nome del file")

"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Data for plotting
t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2 * np.pi * t)

fig, ax = plt.subplots()
ax.plot(t, s)

ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='About as simple as it gets, folks')
ax.grid()

fig.savefig("test.png")
plt.show()
"""
