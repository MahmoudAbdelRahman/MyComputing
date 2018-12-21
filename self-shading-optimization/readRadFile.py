#!C:/Program Files/Python37/Python.exe

import cgi , cgitb

cgitb.enable()


print("Content-type: text/json\n\n")

import numpy as np


path = 'E:/00-NUS/BUDSLAB/rad/model_mod.rad'

f = open(path, 'r')
t = f.readlines()

for i in t:
    if i[0] == "#":
        currentline = i[:-2]
        currentline = currentline.split(" ")

        
        
allSurfaces = []
for idx, val in enumerate(t[1:]):
    if val[0] == "#":
        allSurfaces.append(t[idx+1:idx+10])

# {"SpaceId":{"bodyNum":int , 'surfaceNo':int, 'surfaceType':'','nVertices': int, 'points':''} }
surfacesData = {}
for indx , i in enumerate(allSurfaces):
    spaceDict = {}
    bodyN = i[0][:-2].split(' ')
    spaceDict['itemType'] = bodyN[1]
    if bodyN[1] == 'Body':
        spaceDict['bodyNum'] = int(bodyN[2])
    if(len(bodyN)>3):
        spaceDict['surface'] = int(bodyN[4])
        spaceDict['spaceId'] = bodyN[6].replace('[', '').replace(']','')
    if(len(bodyN)>9):
        spaceDict['spaceType'] = bodyN[8] + bodyN[9]
    elif (len(bodyN)==9):
        spaceDict['spaceType'] = bodyN[8]
    spaceDict['radId'] = i[1][:-2]
    try:
        dd0 =i[5][1:-2].split('  ')
        dd1 =i[6][1:-2].split('  ')
        dd2 =i[7][1:-2].split('  ')
        dd3 =i[8][1:-2].split('  ')
        tt = np.array([dd0, dd1, dd2, dd3])
        tx = tt.astype(np.float)
        tx = tx.tolist()
        spaceDict['points'] = tx
    except:
        print("problem")
    surfacesData[indx] = spaceDict

import json

star = json.dumps(surfacesData)
print(star)