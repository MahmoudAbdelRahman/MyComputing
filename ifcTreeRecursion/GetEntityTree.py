"""
Ifcopenshell Example by by: Mahmoud M. Abdelrahman
<arch.mahmoud.ouf111[at]gmail.com>
Copyright (c) 2018, Mahmoud AbdelRahman
All rights reserved.
https://github.com/MahmoudAbdelRahman/Scientific-computing/edit/master/ifcTreeRecursion/GetEntityTree.py
"""

import ifcopenshell
#Note : PyIfcOpenShell is required.



def getEntitiesTree(ParentIntity, round=-1, element=None, gt=None, printIt=True, text=None):
    """
    This function gets the IfcEntity, and prints a tree of the children

    :param ParentIntity: The ParentEntity of the tree
    :param round: index of the tree branch
    :param element:(string) if you are looking for specific element example: 'IfcPolyline'
    :param gt: (list)  if you need to return a list of the
    :param printIt: if you want to print the tree
    :param text: if you want to save the output tree in a separated text variable to be written on your pc
    :return:
    """
    round += 1
    iter = False
    try:
        _ = (j for j in ParentIntity)
        iter = True
    except Exception as e:
        pass
    if iter:
        if not isinstance(ParentIntity, unicode) and not isinstance(ParentIntity, basestring):
            for j in ParentIntity:
                if j is not None and j != "":
                    if printIt:
                        print(str(round) + " |_" + round * "_" + str(j))
                    if text is not None:
                        text.append(str(round) + " |_" + round * "_" + str(j))
                    else:
                        pass
                try:
                    if j.is_a(element):
                        gt.append(j)
                except:
                    pass
                if gt is not None and element is None:
                    gt.append(j)
                getEntitiesTree(j, round, element, gt, printIt, text)

        else:
            pass

    else:
        pass


#EXAMPLE:

# ifcFile = ifcopenshell.open("example.ifc")
# polyline = ifcFile.by_type("IFCSPACE")[0]
#
# print(polyline)
# getEntitiesTree(polyline)

#OUTPUT :
#784=IfcSpace('1ENKexldP1MB3N9fhk0nCN',#2,'Room I','Description of Space',$,#785,#790,$,$,$,$)
# 0 |_1ENKexldP1MB3N9fhk0nCN
# 0 |_#2=IfcOwnerHistory(#3,#6,$,.ADDED.,$,$,$,1262765552)
# 1 |__#3=IfcPersonAndOrganization(#4,#5,$)
# 2 |___#4=IfcPerson('ID001','Bonsma','Peter',$,$,$,$,$)
# 3 |____ID001
# 3 |____Bonsma
# 3 |____Peter
# 2 |___#5=IfcOrganization($,'TNO','TNO Building Innovation',$,$)
# 3 |____TNO
# 3 |____TNO Building Innovation
# 1 |__#6=IfcApplication(#5,'0.10','Test Application','TA 1001')
# 2 |___#5=IfcOrganization($,'TNO','TNO Building Innovation',$,$)
# 3 |____TNO
# 3 |____TNO Building Innovation
# 2 |___0.10
# 2 |___Test Application
# 2 |___TA 1001
# 1 |__ADDED
# 1 |__1262765552
# 0 |_Room I
# 0 |_Description of Space
# 0 |_#785=IfcLocalPlacement(#36,#786)
# 1 |__#36=IfcLocalPlacement(#30,#37)
# 2 |___#30=IfcLocalPlacement(#24,#31)
# 3 |____#24=IfcLocalPlacement($,#25)
# 4 |_____#25=IfcAxis2Placement3D(#26,#27,#28)
# 5 |______#26=IfcCartesianPoint((0.,0.,0.))
# 6 |_______(0.0, 0.0, 0.0)
# 7 |________0.0
# 7 |________0.0
# 7 |________0.0
# 5 |______#27=IfcDirection((0.,0.,1.))
# 6 |_______(0.0, 0.0, 1.0)
# 7 |________0.0
# 7 |________0.0
# 7 |________1.0
# 5 |______#28=IfcDirection((1.,0.,0.))
# 6 |_______(1.0, 0.0, 0.0)
# 7 |________1.0
# 7 |________0.0
# 7 |________0.0
# 3 |____#31=IfcAxis2Placement3D(#32,#33,#34)
# 4 |_____#32=IfcCartesianPoint((0.,0.,0.))
# 5 |______(0.0, 0.0, 0.0)
# 6 |_______0.0
# 6 |_______0.0
# 6 |_______0.0
# 4 |_____#33=IfcDirection((0.,0.,1.))
# 5 |______(0.0, 0.0, 1.0)
# 6 |_______0.0
# 6 |_______0.0
# 6 |_______1.0
# 4 |_____#34=IfcDirection((1.,0.,0.))
# 5 |______(1.0, 0.0, 0.0)
# 6 |_______1.0
# 6 |_______0.0
# 6 |_______0.0
# 2 |___#37=IfcAxis2Placement3D(#38,#39,#40)
# 3 |____#38=IfcCartesianPoint((0.,0.,0.))
# 4 |_____(0.0, 0.0, 0.0)
# 5 |______0.0
# 5 |______0.0
# 5 |______0.0
# 3 |____#39=IfcDirection((0.,0.,1.))
# 4 |_____(0.0, 0.0, 1.0)
# 5 |______0.0
# 5 |______0.0
# 5 |______1.0
# 3 |____#40=IfcDirection((1.,0.,0.))
# 4 |_____(1.0, 0.0, 0.0)
# 5 |______1.0
# 5 |______0.0
# 5 |______0.0
# 1 |__#786=IfcAxis2Placement3D(#787,#788,#789)
# 2 |___#787=IfcCartesianPoint((300.,1350.,0.))
# 3 |____(300.0, 1350.0, 0.0)
# 4 |_____300.0
# 4 |_____1350.0
# 4 |_____0.0
# 2 |___#788=IfcDirection((0.,0.,1.))
# 3 |____(0.0, 0.0, 1.0)
# 4 |_____0.0
# 4 |_____0.0
# 4 |_____1.0
# 2 |___#789=IfcDirection((1.,0.,0.))
# 3 |____(1.0, 0.0, 0.0)
# 4 |_____1.0
# 4 |_____0.0
# 4 |_____0.0
# 0 |_#790=IfcProductDefinitionShape($,$,(#791))
# 1 |__(#791=IfcShapeRepresentation(#20,'Body','SweptSolid',(#792)),)
# 2 |___#791=IfcShapeRepresentation(#20,'Body','SweptSolid',(#792))
# 3 |____#20=IfcGeometricRepresentationContext($,'Model',3,1.000E-5,#21,$)
# 4 |_____Model
# 4 |_____3
# 4 |_____1e-05
# 4 |_____#21=IfcAxis2Placement3D(#22,$,$)
# 5 |______#22=IfcCartesianPoint((0.,0.,0.))
# 6 |_______(0.0, 0.0, 0.0)
# 7 |________0.0
# 7 |________0.0
# 7 |________0.0
# 3 |____Body
# 3 |____SweptSolid
# 3 |____(#792=IfcExtrudedAreaSolid(#793,#800,#804,2800.),)
# 4 |_____#792=IfcExtrudedAreaSolid(#793,#800,#804,2800.)
# 5 |______#793=IfcArbitraryClosedProfileDef(.AREA.,$,#794)
# 6 |_______AREA
# 6 |_______#794=IfcPolyline((#795,#796,#797,#798,#799))
# 7 |________(#795=IfcCartesianPoint((0.,0.)), #796=IfcCartesianPoint((0.,4500.)), #797=IfcCartesianPoint((3500.,4500.)), #798=IfcCartesianPoint((3500.,0.)), #799=IfcCartesianPoint((0.,0.)))
# 8 |_________#795=IfcCartesianPoint((0.,0.))
# 9 |__________(0.0, 0.0)
# 10 |___________0.0
# 10 |___________0.0
# 8 |_________#796=IfcCartesianPoint((0.,4500.))
# 9 |__________(0.0, 4500.0)
# 10 |___________0.0
# 10 |___________4500.0
# 8 |_________#797=IfcCartesianPoint((3500.,4500.))
# 9 |__________(3500.0, 4500.0)
# 10 |___________3500.0
# 10 |___________4500.0
# 8 |_________#798=IfcCartesianPoint((3500.,0.))
# 9 |__________(3500.0, 0.0)
# 10 |___________3500.0
# 10 |___________0.0
# 8 |_________#799=IfcCartesianPoint((0.,0.))
# 9 |__________(0.0, 0.0)
# 10 |___________0.0
# 10 |___________0.0
# 5 |______#800=IfcAxis2Placement3D(#801,#802,#803)
# 6 |_______#801=IfcCartesianPoint((0.,0.,0.))
# 7 |________(0.0, 0.0, 0.0)
# 8 |_________0.0
# 8 |_________0.0
# 8 |_________0.0
# 6 |_______#802=IfcDirection((0.,0.,1.))
# 7 |________(0.0, 0.0, 1.0)
# 8 |_________0.0
# 8 |_________0.0
# 8 |_________1.0
# 6 |_______#803=IfcDirection((1.,0.,0.))
# 7 |________(1.0, 0.0, 0.0)
# 8 |_________1.0
# 8 |_________0.0
# 8 |_________0.0
# 5 |______#804=IfcDirection((0.,0.,1.))
# 6 |_______(0.0, 0.0, 1.0)
# 7 |________0.0
# 7 |________0.0
# 7 |________1.0
# 5 |______2800.0


