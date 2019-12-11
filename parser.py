bindings={"Fx":0,
          "Fy":1,
          "Fz":2,
          "Tx":3,
          "Ty":4,
          "Tz":5,}

def parse(name,vals):
    matr =[[float(y[1:-1]) for y in x.split(',')[3:-1]] for x in open(name).read().split('\n')[8:-1]]
    y=[[yaa[i] for yaa in matr] for i in range(6)]
    res={}
    res["length"]=len(matr)
    for val in vals:
        res[val]=y[bindings[val]]
    return res
