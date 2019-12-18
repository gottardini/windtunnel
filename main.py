import sys
import numpy as np
import plotter
import filter
import parser
from funcs import ptov,coeff
import scipy.fftpack

areas={"a":0.01656,"b":0.01718,"c":0.01718,"d":0.02399}
setup_names={"a":"Vanilla","b":"Spoiler","c":"Spoiler + gurney flaps","d":"Spoiler + gurney flaps + wings"}

mode=1
if len(sys.argv)==2:
    mode=int(sys.argv[1])

if mode==0:
    compdata={"SaH0Pd":"Vanilla",
             "SbH0Pd1":"Rear spoiler",
             "ScH0Pd":"Rear spoiler + gurney"}
elif mode==1:
    compdata={"SbH0Pd":"Rear spoiler",
             "SbH0Pd1":"Rear spoiler - biased",}
elif mode==2:
    compdata={"SaH0Pa":"V1",
             "SaH0Pb":"V2",
             "SaH0Pc":"V3",
             "SaH0Pd":"V4"}
    pdata={"SaH0Pa":11,
           "SaH0Pb":73,
           "SaH0Pc":142,
           "SaH0Pd":260}
    vdata={key:ptov(px) for key,px in pdata.items()}
elif mode==3:
    compdata={"SbH0Pa":"V1",
             "SbH0Pb":"V2",
             "SbH0Pc":"V3",
             "SbH0Pd":"V4"}
    pdata={"SbH0Pa":11,
           "SbH0Pb":73,
           "SbH0Pc":142,
           "SbH0Pd":254}
    vdata={key:ptov(px) for key,px in pdata.items()}
elif mode==4:
    compdata={"ScH0Pa":"V1",
             "ScH0Pb":"V2",
             "ScH0Pc":"V3",
             "ScH0Pd":"V4"}
    pdata={"ScH0Pa":11,
           "ScH0Pb":70,
           "ScH0Pc":136,
           "ScH0Pd":239}
    vdata={key:ptov(px) for key,px in pdata.items()}
elif mode==5:
    compdata={"SdH0Pa":"V1",
             "SdH0Pb":"V2",
             "SdH0Pc":"V3",
             "SdH0Pd":"V4"}
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
coeffdesc={"Fy":"Cd","Fz":"Cl"}

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

    if mode>1 and mode <6:
        ###FIND AVERAGE VALUES
        avgdata={}
        vels={}
        coeffs={}
        for key,val in filtered_data.items():
            avgdata[key]={compval:np.average(val[compval]) for compval in compvals}

        for compval in compvals:
            vels[compval]=[]
            coeffs[coeffdesc[compval]]=[]
            for key,val in avgdata.items():
                vels[compval].append((vdata[key],avgdata[key][compval]))
                coeffs[coeffdesc[compval]].append((vdata[key],coeff(avgdata[key][compval]*(-1 if compval=="Fy" else 1),areas[key[1]],pdata[key])))
            win=plotter.Plotter()
            #win.plot(xax=[tup[0]*3.6 for tup in vels[compval]],ydata=[[tup[1] for tup in vels[compval]]],labels=[compvaldesc[compval]],figtitle="",ylim=[0,4],xlabel="Velocity [km/h]",ylabel="Force [N]", scatter=True)
            win.plot(xax=[tup[0]*3.6 for tup in vels[compval]],ydata=[[tup[1] for tup in coeffs[coeffdesc[compval]]]],labels=[coeffdesc[compval]],figtitle=setup_names[key[1]]+" setup",ylim=[-5,5],xlabel="Velocity [km/h]",ylabel="", scatter=True)

        print(vels)
        print(coeffs)
        print("\n\n")

        #print(avgdata)



    plotter.plt.show()
