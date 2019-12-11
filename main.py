import sys
import numpy as np
import plotter
import filter
import parser
from funcs import ptov
import scipy.fftpack

mode=7

if mode==0:
    compdata={"SaH0Pd":"Vanilla",
             "SbH0Pd1":"Rear spoiler",
             "ScH0Pd":"Rear spoiler + gurney"}
elif mode==1:
    compdata={"SbH0Pd":"Rear spoiler",
             "SbH0Pd1":"Rear spoiler - biased",}
elif mode==2:
    compdata={"SaH0Pa":"15 km/h",
             "SaH0Pb":"40 km/h",
             "SaH0Pc":"54 km/h",
             "SaH0Pd":"74 km/h"}
    pdata={"SaH0Pa":11,
           "SaH0Pb":73,
           "SaH0Pc":142,
           "SaH0Pd":260}
    vdata={key:ptov(px) for key,px in pdata.items()}
elif mode==3:
    compdata={"SbH0Pa":"15 km/h",
             "SbH0Pb":"40 km/h",
             "SbH0Pc":"54 km/h",
             "SbH0Pd":"74 km/h"}
    pdata={"SbH0Pa":11,
           "SbH0Pb":73,
           "SbH0Pc":142,
           "SbH0Pd":254}
    vdata={key:ptov(px) for key,px in pdata.items()}
elif mode==4:
    compdata={"ScH0Pa":"15 km/h",
             "ScH0Pb":"40 km/h",
             "ScH0Pc":"54 km/h",
             "ScH0Pd":"74 km/h"}
    pdata={"ScH0Pa":11,
           "ScH0Pb":70,
           "ScH0Pc":136,
           "ScH0Pd":239}
    vdata={key:ptov(px) for key,px in pdata.items()}
elif mode==5:
    compdata={"SdH0Pa":"15 km/h",
             "SdH0Pb":"40 km/h",
             "SdH0Pc":"54 km/h",
             "SdH0Pd":"74 km/h"}
    pdata={"SdH0Pa":11,
           "SdH0Pb":68,
           "SdH0Pc":127,
           "SdH0Pd":238}
    vdata={key:ptov(px) for key,px in pdata.items()}

elif mode==6:
    compdata={"SaH0Pd":"Vanilla",
             "SbH0Pd":"Spoiler",
             "ScH0Pd":"Spoiler + Gurney flaps",}
    pdata={"SaH0Pd":260,
           "SbH0Pd":260,
           "ScH0Pd":260,}
    vdata={key:ptov(px) for key,px in pdata.items()}

elif mode==7:
    compdata={"SaH0Pd":"Vanilla",
             "ScH0Pd":"Spoiler + Gurney flaps",
             "SdH0Pd":"Spoiler + Gurney flaps + lateral wings"}
    pdata={"SaH0Pd":260,
           "ScH0Pd":260,
           "SdH0Pd":260,}
    vdata={key:ptov(px) for key,px in pdata.items()}


compvals=["Fy","Fz"]
compvaldesc={"Fy":"Drag","Fz":"Lift"}

trange=[5,10]
freq=125
tfrange=[trange[0]*freq,trange[1]*freq]

if __name__=="__main__":
    ###GET DATA
    data={}
    filtered_data={}
    for key,val in compdata.items():
        data[key]={compval:parser.parse("datax/"+key,compvals)[compval] for compval in compvals}
        filtered_data[key]={compval:filter.filter_binding(data[key][compval],(1,125,2))[tfrange[0]:tfrange[1]] for compval in compvals}

    tlen=tfrange[1]-tfrange[0]
    #print(tfrange[1]-tfrange[0])
    #print(len(data["SaH0Pd"]["Fy"]))

    #print(filtered_data["SaH0Pd"]["Fy"])

    t = np.arange(0, tlen)

    for compval in compvals:
        win=plotter.Plotter()
        yData=[]
        yLabels=[]
        for key,val in filtered_data.items():
            #print(len(val[compval]))
            yData.append(val[compval])
            yLabels.append(compdata[key])
        #print(len(yData))
        win.plot(xax=np.divide(t,125),ydata=yData,labels=yLabels,figtitle=compvaldesc[compval],ylim=[-15,5],xlabel="Time [s]",ylabel="Force [N]")

    if mode>=2 and False:
        ###FIND AVERAGE VALUES
        avgdata={}
        vels={}
        for key,val in filtered_data.items():
            avgdata[key]={compval:np.average(val[compval]) for compval in compvals}

        for compval in compvals:
            vels[compval]=[]
            for key,val in avgdata.items():
                vels[compval].append((vdata[key],avgdata[key][compval]))
            win=plotter.Plotter()

            win.plot(xax=[tup[0]*3.6 for tup in vels[compval]],ydata=[[tup[1] for tup in vels[compval]]],labels=[compvaldesc[compval]],figtitle="",ylim=[0,4],xlabel="Velocity [km/h]",ylabel="Force [N]", scatter=True)
        print(vels)
        #print(avgdata)



    plotter.plt.show()
    """
    #print(sys.argv)
    if len(sys.argv) == 2:
        data=parser.parse(sys.argv[1],["Fy","Fz"])
        fourier_data=data.copy()
        filtered_data=data.copy()
        fourier_filtered_data=data.copy()
        t = np.arange(0, data["length"])

        #Prima finestra
        raw=plotter.Plotter()
        raw.plot(xax=t,ydata=[data["Fy"],],figtitle="Raw Drag",ylim=[-10,10])


        #Terza finestra
        raw_fourier=plotter.Plotter()
        # Number of samplepoints
        N = data["length"]
        # sample spacing
        T = 1 / 125
        fourier_t = np.linspace(0.0, 1.0 / (2.0 * T), N / 2)
        fourier_data["Fy"] = scipy.fftpack.fft(data["Fy"])
        fourier_data["Fy"] = 2.0 / N * np.abs(fourier_data["Fy"][:N // 2])
        raw_fourier.plot(xax=fourier_t,ydata=[fourier_data["Fy"],],figtitle="Fourier Drag",ylim=[-2,2])


        #Seconda Finestra
        filtered=plotter.Plotter()
        filtered_data["Fy"]=filter.filter_binding(data["Fy"],(1,125,2))
        filtered.plot(xax=t,ydata=[filtered_data["Fy"],],figtitle="Filtered Drag",ylim=[-10,10])

        filtered_fourier=plotter.Plotter()
        # Number of samplepoints
        N = data["length"]
        # sample spacing
        T = 1 / 125
        fourier_t = np.linspace(0.0, 1.0 / (2.0 * T), N / 2)
        fourier_filtered_data["Fy"] = scipy.fftpack.fft(filtered_data["Fy"])
        fourier_filtered_data["Fy"] = 2.0 / N * np.abs(fourier_filtered_data["Fy"][:N // 2])
        filtered_fourier.plot(xax=fourier_t,ydata=[fourier_filtered_data["Fy"],],figtitle="Filtered Fourier Drag",ylim=[-2,2])
        plotter.plt.show()

    else:
        raise ValueError("Specifica il nome del file")
    """
