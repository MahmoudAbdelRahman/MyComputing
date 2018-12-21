#!C:/Python27/Python.exe

import copy
import numpy as np
import cgi
import cgitb
import time
import RadOpt as ra
from scipy.optimize import differential_evolution
import sys



# cgitb.enable()


# print("Content-type: text/json\n\n")

bounds = [(-2., 2.)]*104
mainpath = 'D:/'
# mainpath = 'E:/00-NUS/'
path = mainpath+'BUDSLAB/spatial-temporal-tool/ThreeJs/python/model_mod.rad'

iterId = 0

def callableFunction(x, *args):
    global iterId
    '''main callable function for the optimization 
    
    Arguments:
        x {the argument} -- the main arugment in the form of a 1-D arrray
        argz[0] -- the path to the file
    '''
    mainpath = 'D:/'
    # mainpath = 'E:/00-NUS/'

    d = ra.readRadFile(args[0])
    newD = ra.editRadFile(d, x)
    Radtxt, jsontxt, randVals, ptText = ra.writeModifiedRadFile(newD, x)
    newFilesNames = str(time.time()).replace(".", "_")
    new3dJsfilePath = "/generatedRad/" + newFilesNames + ".json"
    newRadFilePath = mainpath + "BUDSLAB/spatial-temporal-tool/ThreeJs/generatedRad/" + newFilesNames + ".rad"
    newPtsPath = mainpath + "BUDSLAB/spatial-temporal-tool/ThreeJs/generatedPts/" + newFilesNames + ".pts"



    with open(newRadFilePath, 'w') as newrad:
        newrad.write(Radtxt)

    with open(newPtsPath, 'w') as pts:
        pts.write(ptText)


    open(mainpath+'BUDSLAB/spatial-temporal-tool/ThreeJs' +
        new3dJsfilePath, 'w').write(jsontxt)
    res, theprint = ra.RunRadiance(str(newFilesNames))

    print(theprint.replace("##id##", str(iterId)))
    sys.stdout.flush()
    with open("allRestuls.json", 'a') as f:
        f.write('{"id":'+str(iterId)+', "fname":"'+newFilesNames+'","x": '+str(x.tolist())+', "av_val": '+str(res)+'},\n')
        iterId += 1 
    return res



args = [path]
result = differential_evolution(callableFunction, bounds,args, maxiter=1000)



with open("allRestuls.json", 'a') as f:
        f.write(']')