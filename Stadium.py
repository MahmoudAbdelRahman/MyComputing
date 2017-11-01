#Stadium covering using RhinoPython script
#Design and implementation of this code was done by:
#Mahmoud Mohamed AbdelRahman
#arch.mahmoud.ouf111@gmail.com
#www.m-ouf.com

import rhinoscriptsyntax as rs


def curve(p1, p2, param=0.5, pointheight=5.0):
    points = []

    rs.AddPoint(p1)
    rs.AddPoint(p2)

    l1 = rs.AddLine(p1, p2)

    v1 = rs.VectorCreate(p2, p1)
    v3 = (0, 0, 0)
    p1 = rs.CurveParameter(l1, param)

    midpoint = rs.EvaluateCurve(l1, p1)
    rs.AddPoint(midpoint)

    vec2 = (v1[2], v1[1], - v1[0])
    vec2 = rs.VectorUnitize(vec2)
    vec2 *= -pointheight
    vec2 = rs.VectorAdd(vec2, midpoint)

    l3 = rs.AddLine(vec2, midpoint)
    p3 = rs.AddPoint(vec2)
    points = (v1, vec2, v3)

    c1 = rs.AddInterpCurve(points)
    return c1


p1 = (0, 0, 0)
p2 = (30.0, 0, 10)
c1 = curve(p1, p2, 0.2, 7.)
c2 = curve(p1, p2, 0.2, 20.)
c3 = curve(p1, p2, 0.2, 20.)

newl = rs.VectorCreate(p2, p1)
c2 = rs.RotateObject(c2, p1, 50.0, newl)
c3 = rs.RotateObject(c3, p2, -50.0, newl)

points1 = rs.DivideCurve(c1, 20, True, True)
points2 = rs.DivideCurve(c2, 20, True, True)
points3 = rs.DivideCurve(c3, 20, True, True)

newcurves = []
for i in range(len(points1)):
    pointlist = points2[i], points1[i], points3[i]
    newc = rs.AddInterpCurve(pointlist)
    newcurves.append(newc)

axis = rs.VectorCreate((100, 0, 20), (100, 0, 0))

for i in range(20):
    pipe = rs.AddPipe(c2, 0, 0.5)
    pipe2 = rs.AddPipe(c3, 0, 0.5)
    surfaces = rs.AddLoftSrf(newcurves)
    rs.RotateObject(surfaces, (100, 0, 0), (360. / 20) * i, axis)
    rs.RotateObject(pipe, (100, 0, 0), (360. / 20) * i, axis)
    rs.RotateObject(pipe2, (100, 0, 0), (360. / 20) * i, axis)

c4 = rs.RotateObject(c3, (100, 0, 0), (360. / 20), axis)
newcurves2 = (c2, c4)

for i in range(20):
    newsurf = rs.AddLoftSrf(newcurves2)
    rs.RotateObject(newsurf, (100, 0, 0), (360. / 20.) * i, axis)
