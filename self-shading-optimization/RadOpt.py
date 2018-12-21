import copy
import numpy as np
import cgi
import cgitb
import time
import sys
import subprocess
from multiprocessing import Pool


def readRadFile(path_):
    f = open(path_, 'r')
    t = f.readlines()

    allData = {}
    allSurfaces = {}
    frameInt = 0
    for indx, i in enumerate(t):
        if(indx > 0):
            if i[0] == "#":
                thisSurf = {}
                firstLine = t[indx][:-2]
                secondLine = t[indx+1][:-2]
                mat = t[indx+1][:-2].split(' ')[0].split(':')
                code = t[indx+1][:-2].split(' ')[-1].split('_')
                codeDict = {'Space': code[1],
                            'Surface': code[2], 'id': code[3]}
                points = np.array([np.fromstring(t[indx+5][:-2], dtype=np.float, sep=' '),
                                   np.fromstring(t[indx+6][:-2],
                                                 dtype=np.float, sep=' '),
                                   np.fromstring(t[indx+7][:-2],
                                                 dtype=np.float, sep=' '),
                                   np.fromstring(t[indx+8][:-2], dtype=np.float, sep=' ')])
                points = points.tolist()
                thisSurf = {'radLines': firstLine + '\n'+secondLine,
                            'mat': mat, 'code': codeDict, 'points': points, 'Ylim': 0.0}
                try:
                    if(mat[1] == 'frm'):
                        allData['frm_'+str(frameInt)] = thisSurf
                        frameInt += 1
                    else:
                        allData[int(codeDict['id'])] = thisSurf
                except:
                    allData[int(codeDict['id'])] = thisSurf

    return allData


def editRadFile(dataFile, x):
    
    for k, v in dataFile.items():
        if v['code']['Surface'] == '00':
            ylim = v['points'][1][1]
            for k2, v2 in dataFile.items():
                if int(v2['code']['Space']) == int(v['code']['Space']):
                    v2['Ylim'] = ylim

    for k, v in dataFile.items():
        thisP = v['points']
        for p in thisP:
            if p[1] == v['Ylim'] or (p[1] > v['Ylim'] - 0.2 and p[1] < v['Ylim']+0.2):
                p[1] = v['Ylim'] + x[int(v['code']['Space'])]
        v['points'] = thisP

    return dataFile


def writeModifiedRadFile(dataFile, x):
    tempmat = ['CNCR0000', 'BRCK0000', 'DBLG0000', 'SPHL0000', 'GRYC0000', 'PLST0000']
    ptText = ""
    txt = "#Radiance Geometry file: IES Ltd. \n"
    jsontxt = "vertices = ["
    for k, v in dataFile.items():
        txt += v['radLines']+"\n0 \n0 \n12 \n"
        
        if v['mat'][0] == 'DBLG0000':
            minx = np.min([v['points'][0][0], v['points'][1][0], v['points'][2][0], v['points'][3][0]])
            maxy = np.max([v['points'][0][1], v['points'][1][1], v['points'][2][1], v['points'][3][1]])
            minz = np.min([v['points'][0][2], v['points'][1][2], v['points'][2][2], v['points'][3][2]])
            xs =  np.round([minx, minx+ 0.766, minx+ 2.*0.766, minx + 3.*0.766], 3)
            ys =  np.round([maxy, maxy- 0.766, maxy- 2.*0.766, maxy - 3.*0.766], 3)
            zs =  round(minz + 0.2, 3)
            for row in range(4):
                for col in range(4):
                    ptText += str(xs[row]) + "\t"+ str(ys[col])+"\t"+str(zs)+"\t0.000\t0.000\t1.000\n"
    
        for p in v['points']:
            txt += str(p[0]) + "   " + str(round(p[1], 4)) + \
                "   " + str(p[2]) + "\n"

        p0 = str(v['points'][0]).replace('[', '').replace(']', '')
        p1 = str(v['points'][1]).replace('[', '').replace(']', '')
        p2 = str(v['points'][2]).replace('[', '').replace(']', '')
        p3 = str(v['points'][3]).replace('[', '').replace(']', '')
        jsontxt += p0 + "," + p1 + "," + p2 + "," + p0 + "," + p2 + "," + p3 + ","
    jsontxt = jsontxt[:-1] + "]"
    return txt, jsontxt, x, ptText

def readRadResultFile(filepath):
    results = np.loadtxt(filepath)
    return np.average(results)



def RunRadiance(filename):
    try:
        mainfolder = 'D:\\BUDSLAB\\spatial-temporal-tool\\ThreeJs\\'
        # mainfolder = 'E:\\00-NUS\\BUDSLAB\\spatial-temporal-tool\\ThreeJs\\'
        matpath = mainfolder+'radmains\\mat.mat'
        skypath = mainfolder+'radmains\\skyfile.sky'
        radpath = 'C:\\Radiance\\lib\\'
        vfpath = mainfolder+'radmains\\vf.vf'

        newradfileName = mainfolder+"generatedRad\\"+filename+".rad"
        newOctFileName = mainfolder+"generatedOct\\"+filename+".oct"
        newResFileName = mainfolder+"generatedRes\\"+filename+".res"
        newBatFileName = mainfolder+"generatedBat\\"+filename+".bat"
        newHdrFilename = mainfolder+"generatedHDR\\"+filename+".hdr"
        newHdrFilename2 = mainfolder+"generatedHDR\\"+filename+"2.hdr"
        newGifFilename = mainfolder+"generatedGIF\\"+filename+".gif"
        newpTsFilename = mainfolder+"generatedPts\\"+filename+".pts"

        f = open(mainfolder+"batfile.bat", 'r')
        oldbatch = f.read()
        f.close()

        newbatText = oldbatch.replace("##!MainFolder!##", mainfolder)
        newbatText = newbatText.replace("##!matfile!##", matpath)
        newbatText = newbatText.replace("##!skyfile!##", skypath)
        newbatText = newbatText.replace("##!vffile!##", vfpath)
        newbatText = newbatText.replace("##!radfile!##", newradfileName)
        newbatText = newbatText.replace("##!octFile!##", newOctFileName)
        newbatText = newbatText.replace("##!resfile!##", newResFileName)
        newbatText = newbatText.replace("#!respic!#", newHdrFilename)
        newbatText = newbatText.replace("##!giffile!##", newGifFilename)
        newbatText = newbatText.replace("#!respic_h!#", newHdrFilename2)
        newbatText = newbatText.replace("##!ptsfile!##", newpTsFilename)
        
        batchfile = open(newBatFileName, 'w')
        batchfile.write(newbatText)
        batchfile.close()
        p = subprocess.Popen([newBatFileName],
                        stdout=subprocess.PIPE)
        p.wait()

        res = readRadResultFile(newResFileName)
        theprint = '<div class="res ##id##"><a href="">'+str(res)+'</a><img class="previewImages" src="./generatedGIF/'+filename+'.gif"></div><hr>'
        return [float(res) , theprint]
        
        # TODO Specify the return of this radiance, for example, the average of the daylight illuminance of the whole points.  done
        # TODO We still need a function to calculate the average of all points. 
        # TODO Another function to write the data, plot the data . 
    except Exception as e:
        print(str(e))

