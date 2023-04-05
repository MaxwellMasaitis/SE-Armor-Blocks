from enum import Enum
from collections import Counter
import copy

class Edge(Enum):
    VOID = 0
    FULL = 1
    #_ Left Right _
    #   |      |
    #|  _      _  |
    HALF_LEFT = 2
    HALF_RIGHT = 3
    
    SPECIALFULL = 4
    SPECIALTRI = 5
    SPECIALHALF = 6

class FaceKind(object):
    def __init__(self) -> None:
        self.name = ''
        self.budget = []
    def __str__(self) -> str:
        return "Face"
    def __eq__(self, obj: object) -> bool:
        return type(self) == type(obj)
    def __ne__(self, obj: object) -> bool:
        return not self == obj
    def orientationCheck(self, a, b, c, d) -> bool:
        return True

class Square(FaceKind):
    def __init__(self) -> None:
        super().__init__()
        self.budget += 4 * [Edge.FULL]
        self.budget += 2 * [Edge.SPECIALFULL]
    def __str__(self) -> str:
        return "Square"
    def orientationCheck(self, a: Edge, b: Edge, c: Edge, d: Edge) -> bool:
        # opposite sides cannot both be SPECIALFULL
        if a == Edge.SPECIALFULL and d == Edge.SPECIALFULL:
            return False
        elif b == Edge.SPECIALFULL and c == Edge.SPECIALFULL:
            return False
        return True

class Empty(FaceKind):
    def __init__(self) -> None:
        super().__init__()
        self.budget += 4 * [Edge.VOID]
        self.budget += 2 * [Edge.SPECIALFULL]
        self.budget += [Edge.SPECIALTRI]
    def __str__(self) -> str:
        return "Empty"
    def orientationCheck(self, a: Edge, b: Edge, c: Edge, d: Edge) -> bool:
        # opposite sides cannot both be SPECIALFULL
        if a == Edge.SPECIALFULL and d == Edge.SPECIALFULL:
            return False
        elif b == Edge.SPECIALFULL and c == Edge.SPECIALFULL:
            return False
        # cannot contain SPECIALFULL and SPECIALTRI at the same time
        if Edge.SPECIALFULL in [a,b,c,d] and Edge.SPECIALTRI in [a,b,c,d]:
            return False
        #TODO: add cases for half edges
        return True

class Triangle(FaceKind):
    def __init__(self) -> None:
        super().__init__()
        self.budget += 2 * [Edge.FULL]
        self.budget += 2 * [Edge.VOID]
        self.budget += [Edge.SPECIALTRI]
    def __str__(self) -> str:
        return "Triangle"
    # think up a way to lock the orientation of the edges (set up a parent class?)
    def orientationCheck(self, a: Edge, b: Edge, c: Edge, d: Edge) -> bool:
        # opposite sides must have opposite edge types
        if a is not None and d is not None and a == d:
            return False
        elif b is not None and c is not None and b == c:
            return False
        # SPECIALTRI must take the place of a FULL and hence cannot be opposite of a FULL
        if (Edge.SPECIALTRI in (a,d) and Edge.FULL in (a,d)) or (Edge.SPECIALTRI in (b,c) and Edge.FULL in (b,c)):
            return False
        return True

class Face():
    def __init__(self, facekind)-> None:
        self.facekind = facekind
        # a
        #b c
        # d
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.remainingBudget = self.facekind.budget.copy()
    def __str__(self) -> str:
        return str(self.facekind)
    def __repr__(self) -> str:
        # for checking out lists from the cubes
        return str(self.facekind)
    # need to define an eq that works through rotation
    def __eq__(self, obj: object) -> bool:
        if (type(self) != type(obj)):
            return False
        if self.facekind != obj.facekind:
            return False
        if self.remainingBudget != obj.remainingBudget:
            return False
        if [self.a, self.b, self.c, self.d] == [obj.a, obj.b, obj.c, obj.d]:
            return True
        elif [self.a, self.b, self.c, self.d] == [obj.c, obj.a, obj.d, obj.b]:
            return True
        elif [self.a, self.b, self.c, self.d] == [obj.d, obj.c, obj.b, obj.a]:
            return True
        elif [self.a, self.b, self.c, self.d] == [obj.b, obj.d, obj.a, obj.c]:
            return True
        return False
    def __ne__(self, obj: object) -> bool:
        return not self == obj
    def isOrientationOk(self) -> bool:
        return self.facekind.orientationCheck(self.a, self.b, self.c, self.d)

class Cube():
    def __init__(self, top:Face=None, bottom:Face=None, front:Face=None, back:Face=None, left:Face=None, right:Face=None) -> None:
        self.top = top
        self.bottom = bottom
        self.front = front
        self.back = back
        self.left = left
        self.right = right
    def __eq__(self, obj: object) -> bool:
        # unhashable
        #if Counter(self.get_face_list()) != Counter(obj.get_face_list()):
        #   return False
        for cube in [obj, obj.bottom_to_top(), obj.front_to_top(), obj.back_to_top(), obj.left_to_top(), obj.right_to_top()]:
            for rota in [cube, cube.rotate_top_face_90(), cube.rotate_top_face_90().rotate_top_face_90(), cube.rotate_top_face_90().rotate_top_face_90().rotate_top_face_90()]:
                if self.get_face_list() == rota.get_face_list():
                    return True
        return False
    def __ne__(self, obj: object) -> bool:
        return not self == obj
    def get_face_list(self):
        return [self.top, self.bottom, self.front, self.back, self.left, self.right]
    # set a face to be the top, then check all 4 rotations
    # return Cube(self.top, self.bottom, self.front, self.back, self.left, self.right)
    def rotate_top_face_90(self):
        return Cube(self.top, self.bottom, self.right, self.left, self.front, self.back)
    
    def bottom_to_top(self):
        return Cube(self.bottom, self.top, self.back, self.front, self.left, self.right)
    def front_to_top(self):
        return Cube(self.front, self.back, self.bottom, self.top, self.left, self.right)
    def back_to_top(self):
        return Cube(self.back, self.front, self.top, self.bottom, self.left, self.right)
    def left_to_top(self):
        return Cube(self.left, self.right, self.front, self.back, self.bottom, self.top)
    def right_to_top(self):
        return Cube(self.right, self.left, self.front, self.back, self.top, self.bottom)

def cullCubes(cubeList: list) -> list:
    tempCubes = []
    for cube in cubeList:
        flag = False
        for reverseCube in tempCubes:
            if cube == reverseCube:
                flag = True
        if not flag:
            tempCubes.append(cube)
    return tempCubes

if __name__ == "__main__":
    facekinds = [Empty(), Triangle(), Square()]

    cubeBottoms = []
    for face in facekinds:
        cube = Cube()
        cube.bottom = Face(face)
        cubeBottoms.append(cube)
    
    cubeBacks = []
    for face in facekinds:
        for cube in cubeBottoms:
            #sharedBudget = list((Counter(bottom,remainingBudget) & Counter(faceBack.budget)).elements())
            sharedBudget = list(set(cube.bottom.remainingBudget) & set(face.budget))
            if sharedBudget:
                if Edge.SPECIALFULL in sharedBudget and face == cube.bottom.facekind:
                    sharedBudget = [i for i in sharedBudget if i != Edge.SPECIALFULL]
                if Edge.SPECIALTRI in sharedBudget and face == cube.bottom.facekind:
                    sharedBudget = [i for i in sharedBudget if i != Edge.SPECIALTRI]
                cube.back = Face(face)
                for edge in sharedBudget:
                    cubeEdges = copy.deepcopy(cube)

                    cubeEdges.bottom.a = edge
                    cubeEdges.bottom.remainingBudget.remove(edge)
                    cubeEdges.back.d = edge
                    cubeEdges.back.remainingBudget.remove(edge)

                    cubeBacks.append(cubeEdges)
    
    # find a way to drop cubes where the faces AND EDGES are the same
    cubeBacks = cullCubes(cubeBacks)

    cubeLefts = []
    for face in facekinds:
        for cube in cubeBacks:
            sharedBudgetBottom = list(set(cube.bottom.remainingBudget) & set(face.budget))
            if sharedBudgetBottom:
                if Edge.SPECIALFULL in sharedBudgetBottom and face == cube.bottom.facekind:
                    sharedBudgetBottom = [i for i in sharedBudgetBottom if i != Edge.SPECIALFULL]
                if Edge.SPECIALTRI in sharedBudgetBottom and face == cube.bottom.facekind:
                    sharedBudgetBottom = [i for i in sharedBudgetBottom if i != Edge.SPECIALTRI]
                for bottomLeftEdge in sharedBudgetBottom:
                    faceBottomBudget = face.budget.copy()
                    faceBottomBudget.remove(bottomLeftEdge)
                    sharedBudgetBack = list(set(cube.back.remainingBudget) & set(faceBottomBudget))
                    if Edge.SPECIALFULL in sharedBudgetBack and face == cube.back.facekind:
                        sharedBudgetBack = [i for i in sharedBudgetBack if i != Edge.SPECIALFULL]
                    if Edge.SPECIALTRI in sharedBudgetBack and face == cube.back.facekind:
                        sharedBudgetBack = [i for i in sharedBudgetBack if i != Edge.SPECIALTRI]
                    cube.left = Face(face)
                    for backLeftEdge in sharedBudgetBack:
                        cubeEdges = copy.deepcopy(cube)

                        cubeEdges.bottom.b = bottomLeftEdge
                        cubeEdges.bottom.remainingBudget.remove(bottomLeftEdge)
                        cubeEdges.left.d = bottomLeftEdge
                        cubeEdges.left.remainingBudget.remove(bottomLeftEdge)

                        cubeEdges.back.b = backLeftEdge
                        cubeEdges.back.remainingBudget.remove(backLeftEdge)
                        cubeEdges.left.c = backLeftEdge
                        cubeEdges.left.remainingBudget.remove(backLeftEdge)

                        okFaceCount = 0
                        for cubeFace in cubeEdges.get_face_list():
                            if cubeFace and cubeFace.isOrientationOk():
                                okFaceCount += 1
                            elif cubeFace is None:
                                okFaceCount += 1
                        if okFaceCount == 6:
                            cubeLefts.append(cubeEdges)

    cubeLefts = cullCubes(cubeLefts)
    # for cube in cubeLefts:
    #     print()
    #     print(cube.bottom.facekind, cube.back.facekind, cube.left.facekind)
    #     print(cube.bottom.a, cube.bottom.b)
    #     print(cube.back.b)
    # print(len(cubeLefts))

    cubeFronts = []
    for face in facekinds:
        for cube in cubeLefts:
            sharedBudgetBottom = list(set(cube.bottom.remainingBudget) & set(face.budget))
            if sharedBudgetBottom:
                if Edge.SPECIALFULL in sharedBudgetBottom and face == cube.bottom.facekind:
                    sharedBudgetBottom = [i for i in sharedBudgetBottom if i != Edge.SPECIALFULL]
                if Edge.SPECIALTRI in sharedBudgetBottom and face == cube.bottom.facekind:
                    sharedBudgetBottom = [i for i in sharedBudgetBottom if i != Edge.SPECIALTRI]
                for bottomFrontEdge in sharedBudgetBottom:
                    faceBottomBudget = face.budget.copy()
                    faceBottomBudget.remove(bottomFrontEdge)
                    sharedBudgetLeft = list(set(cube.left.remainingBudget) & set(faceBottomBudget))
                    if Edge.SPECIALFULL in sharedBudgetLeft and face == cube.left.facekind:
                        sharedBudgetLeft = [i for i in sharedBudgetLeft if i != Edge.SPECIALFULL]
                    if Edge.SPECIALTRI in sharedBudgetLeft and face == cube.left.facekind:
                        sharedBudgetLeft = [i for i in sharedBudgetLeft if i != Edge.SPECIALTRI]
                    cube.front = Face(face)
                    for frontLeftEdge in sharedBudgetLeft:
                        cubeEdges = copy.deepcopy(cube)

                        cubeEdges.bottom.d = bottomFrontEdge
                        cubeEdges.bottom.remainingBudget.remove(bottomFrontEdge)
                        cubeEdges.front.d = bottomFrontEdge
                        cubeEdges.front.remainingBudget.remove(bottomFrontEdge)

                        cubeEdges.left.b = frontLeftEdge
                        cubeEdges.left.remainingBudget.remove(frontLeftEdge)
                        cubeEdges.front.b = frontLeftEdge
                        cubeEdges.front.remainingBudget.remove(frontLeftEdge)

                        okFaceCount = 0
                        for cubeFace in cubeEdges.get_face_list():
                            if cubeFace and cubeFace.isOrientationOk():
                                okFaceCount += 1
                            elif cubeFace is None:
                                okFaceCount += 1
                        if okFaceCount == 6:
                            cubeFronts.append(cubeEdges)
    
    cubeFronts = cullCubes(cubeFronts)
    # for cube in cubeFronts:
    #     print()
    #     print(cube.bottom.facekind, cube.back.facekind, cube.left.facekind, cube.front.facekind)
    #     print(cube.bottom.a, cube.bottom.b, cube.bottom.d)
    #     print(cube.back.b)
    #     print(cube.left.b)
    # print(len(cubeFronts))

    cubeRights = []
    for face in facekinds:
        for cube in cubeFronts:
            sharedBudgetBottom = list(set(cube.bottom.remainingBudget) & set(face.budget))
            if sharedBudgetBottom:
                if Edge.SPECIALFULL in sharedBudgetBottom and face == cube.bottom.facekind:
                    sharedBudgetBottom = [i for i in sharedBudgetBottom if i != Edge.SPECIALFULL]
                if Edge.SPECIALTRI in sharedBudgetBottom and face == cube.bottom.facekind:
                    sharedBudgetBottom = [i for i in sharedBudgetBottom if i != Edge.SPECIALTRI]
                for bottomRightEdge in sharedBudgetBottom:
                    faceBottomBudget = face.budget.copy()
                    faceBottomBudget.remove(bottomRightEdge)
                    sharedBudgetFront = list(set(cube.front.remainingBudget) & set(faceBottomBudget))
                    if Edge.SPECIALFULL in sharedBudgetFront and face == cube.front.facekind:
                        sharedBudgetFront = [i for i in sharedBudgetFront if i != Edge.SPECIALFULL]
                    if Edge.SPECIALTRI in sharedBudgetFront and face == cube.front.facekind:
                        sharedBudgetFront = [i for i in sharedBudgetFront if i != Edge.SPECIALTRI]
                    for frontRightEdge in sharedBudgetFront:
                        faceFrontBudget = faceBottomBudget.copy()
                        faceFrontBudget.remove(frontRightEdge)
                        sharedBudgetBack = list(set(cube.back.remainingBudget) & set(faceFrontBudget))
                        if Edge.SPECIALFULL in sharedBudgetBack and face == cube.back.facekind:
                            sharedBudgetBack = [i for i in sharedBudgetBack if i != Edge.SPECIALFULL]
                        if Edge.SPECIALTRI in sharedBudgetBack and face == cube.back.facekind:
                            sharedBudgetBack = [i for i in sharedBudgetBack if i != Edge.SPECIALTRI]
                        cube.right = Face(face)
                        for backRightEdge in sharedBudgetBack:
                            cubeEdges = copy.deepcopy(cube)

                            cubeEdges.bottom.c = bottomRightEdge
                            cubeEdges.bottom.remainingBudget.remove(bottomRightEdge)
                            cubeEdges.right.d = bottomRightEdge
                            cubeEdges.right.remainingBudget.remove(bottomRightEdge)

                            cubeEdges.front.c = frontRightEdge
                            cubeEdges.front.remainingBudget.remove(frontRightEdge)
                            cubeEdges.right.b = frontRightEdge
                            cubeEdges.right.remainingBudget.remove(frontRightEdge)

                            cubeEdges.back.c = backRightEdge
                            cubeEdges.back.remainingBudget.remove(backRightEdge)
                            cubeEdges.right.c = backRightEdge
                            cubeEdges.right.remainingBudget.remove(backRightEdge)

                            okFaceCount = 0
                            for cubeFace in cubeEdges.get_face_list():
                                if cubeFace and cubeFace.isOrientationOk():
                                    okFaceCount += 1
                                elif cubeFace is None:
                                    okFaceCount += 1
                            if okFaceCount == 6:
                                cubeRights.append(cubeEdges)
    
    cubeRights = cullCubes(cubeRights)
    # for cube in cubeRights:
    #     print()
    #     print(cube.bottom.facekind, cube.back.facekind, cube.left.facekind, cube.front.facekind, cube.right.facekind)
    #     print(cube.bottom.a, cube.bottom.b, cube.bottom.d, cube.bottom.c)
    #     print(cube.back.b)
    #     print(cube.left.b)
    #     print(cube.right.b)
    #     print(cube.right.c)
    # print(len(cubeRights))

    cubeTops = []
    for face in facekinds:
        for cube in cubeRights:
            sharedBudgetBack = list(set(cube.back.remainingBudget) & set(face.budget))
            if sharedBudgetBack:
                if Edge.SPECIALFULL in sharedBudgetBack and face == cube.back.facekind:
                    sharedBudgetBack = [i for i in sharedBudgetBack if i != Edge.SPECIALFULL]
                if Edge.SPECIALTRI in sharedBudgetBack and face == cube.back.facekind:
                    sharedBudgetBack = [i for i in sharedBudgetBack if i != Edge.SPECIALTRI]
                for topBackEdge in sharedBudgetBack:
                    faceBackBudget = face.budget.copy()
                    faceBackBudget.remove(topBackEdge)
                    sharedBudgetLeft = list(set(cube.left.remainingBudget) & set(faceBackBudget))
                    if Edge.SPECIALFULL in sharedBudgetLeft and face == cube.left.facekind:
                        sharedBudgetLeft = [i for i in sharedBudgetLeft if i != Edge.SPECIALFULL]
                    if Edge.SPECIALTRI in sharedBudgetLeft and face == cube.left.facekind:
                        sharedBudgetLeft = [i for i in sharedBudgetLeft if i != Edge.SPECIALTRI]
                    for topLeftEdge in sharedBudgetLeft:
                        faceLeftBudget = faceBackBudget.copy()
                        faceLeftBudget.remove(topLeftEdge)
                        sharedBudgetFront = list(set(cube.front.remainingBudget) & set(faceLeftBudget))
                        if Edge.SPECIALFULL in sharedBudgetFront and face == cube.front.facekind:
                            sharedBudgetFront = [i for i in sharedBudgetFront if i != Edge.SPECIALFULL]
                        if Edge.SPECIALTRI in sharedBudgetFront and face == cube.front.facekind:
                            sharedBudgetFront = [i for i in sharedBudgetFront if i != Edge.SPECIALTRI]
                        for topFrontEdge in sharedBudgetFront:
                            faceFrontBudget = faceLeftBudget.copy()
                            faceFrontBudget.remove(topFrontEdge)
                            sharedBudgetRight = list(set(cube.right.remainingBudget) & set(faceFrontBudget))
                            if Edge.SPECIALFULL in sharedBudgetRight and face == cube.right.facekind:
                                sharedBudgetRight = [i for i in sharedBudgetRight if i != Edge.SPECIALFULL]
                            if Edge.SPECIALTRI in sharedBudgetRight and face == cube.right.facekind:
                                sharedBudgetRight = [i for i in sharedBudgetRight if i != Edge.SPECIALTRI]
                            cube.top = Face(face)
                            for topRightEdge in sharedBudgetRight:
                                cubeEdges = copy.deepcopy(cube)

                                cubeEdges.back.a = topBackEdge
                                cubeEdges.back.remainingBudget.remove(topBackEdge)
                                cubeEdges.top.a = topBackEdge
                                cubeEdges.top.remainingBudget.remove(topBackEdge)

                                cubeEdges.left.a = topLeftEdge
                                cubeEdges.left.remainingBudget.remove(topLeftEdge)
                                cubeEdges.top.b = topLeftEdge
                                cubeEdges.top.remainingBudget.remove(topLeftEdge)

                                cubeEdges.front.a = topFrontEdge
                                cubeEdges.front.remainingBudget.remove(topFrontEdge)
                                cubeEdges.top.d = topFrontEdge
                                cubeEdges.top.remainingBudget.remove(topFrontEdge)

                                cubeEdges.right.a = topRightEdge
                                cubeEdges.right.remainingBudget.remove(topRightEdge)
                                cubeEdges.top.c = topRightEdge
                                cubeEdges.top.remainingBudget.remove(topRightEdge)

                                okFaceCount = 0
                                for cubeFace in cubeEdges.get_face_list():
                                    if cubeFace and cubeFace.isOrientationOk():
                                        okFaceCount += 1
                                    elif cubeFace is None:
                                        okFaceCount += 1
                                if okFaceCount == 6:
                                    cubeTops.append(cubeEdges)
    
    cubeTops = cullCubes(cubeTops)
    for cube in cubeTops:
        print()
        print(cube.bottom.facekind, cube.back.facekind, cube.left.facekind, cube.front.facekind, cube.right.facekind, cube.top.facekind)
        print(cube.bottom.a, cube.bottom.b, cube.bottom.d, cube.bottom.c)
        print(cube.back.b)
        print(cube.left.b)
        print(cube.front.c)
        print(cube.right.c)
        print(cube.top.a, cube.top.b, cube.top.d, cube.top.c)
    print(len(cubeTops))
    
    #TODO: fix the cube equality checker? there should be two 'all-triangle' cubes but we have one and not the inverse
    #TODO: cube equality checker doesn't seem to be picking up dupes with specialtri sides?
    #TODO: move edges into the cubes so we can do the equality with rotation better
    #TODO: this should also eliminate the confusion of the abcd format
    #TODO: make the repeated code a function, recursive