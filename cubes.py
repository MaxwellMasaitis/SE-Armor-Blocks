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

class Round(Triangle):
    def __init__(self) -> None:
        super().__init__()
    def __str__(self) -> str:
        return "Round"

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
        return True
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

        self.topBackEdge = None
        self.topLeftEdge = None
        self.topFrontEdge = None
        self.topRightEdge = None

        self.backLeftEdge = None
        self.frontLeftEdge = None
        self.frontRightEdge = None
        self.backRightEdge = None

        self.bottomBackEdge = None
        self.bottomLeftEdge = None
        self.bottomFrontEdge = None
        self.bottomRightEdge = None

    def __eq__(self, obj: object) -> bool:
        # unhashable
        #if Counter(self.get_face_list()) != Counter(obj.get_face_list()):
        #   return False
        for cube in [obj, obj.bottom_to_top(), obj.front_to_top(), obj.back_to_top(), obj.left_to_top(), obj.right_to_top()]:
            for rota in [cube, cube.rotate_top_face_90(), cube.rotate_top_face_90().rotate_top_face_90(), cube.rotate_top_face_90().rotate_top_face_90().rotate_top_face_90()]:
                if self.get_face_list() == rota.get_face_list() and self.get_edge_list() == rota.get_edge_list():
                    return True
        return False
    def __ne__(self, obj: object) -> bool:
        return not self == obj
    def get_face_list(self) -> list:
        return [self.top, self.bottom, self.front, self.back, self.left, self.right]
    def get_edge_list(self) -> list:
        return [self.topBackEdge, self.topLeftEdge, self.topFrontEdge, self.topRightEdge, self.backLeftEdge, self.backRightEdge, self.frontLeftEdge, self.frontRightEdge,
                self.bottomBackEdge, self.bottomLeftEdge, self.bottomFrontEdge, self.bottomRightEdge]
    # set a face to be the top, then check all 4 rotations
    # return Cube(self.top, self.bottom, self.front, self.back, self.left, self.right)
    def rotate_top_face_90(self):
        # clockwise rotation
        cube = Cube(self.top, self.bottom, self.right, self.left, self.front, self.back)

        cube.topBackEdge = self.topLeftEdge
        cube.topLeftEdge = self.topFrontEdge
        cube.topFrontEdge = self.topRightEdge
        cube.topRightEdge = self.topBackEdge

        cube.backLeftEdge = self.frontLeftEdge
        cube.frontLeftEdge = self.frontRightEdge
        cube.frontRightEdge = self.backRightEdge
        cube.backRightEdge = self.backLeftEdge

        cube.bottomBackEdge = self.bottomLeftEdge
        cube.bottomLeftEdge = self.bottomFrontEdge
        cube.bottomFrontEdge = self.bottomRightEdge
        cube.bottomRightEdge = self.bottomBackEdge

        return cube
    
    # all these could be just front_to_top and rotate_top_face_90 in various combinations...
    def bottom_to_top(self):
        # could also do front_to_top twice. or anything twice?
        cube = Cube(self.bottom, self.top, self.back, self.front, self.left, self.right)

        cube.topBackEdge = self.bottomFrontEdge
        cube.topLeftEdge = self.bottomLeftEdge
        cube.topFrontEdge = self.bottomBackEdge
        cube.topRightEdge = self.bottomRightEdge

        cube.backLeftEdge = self.frontLeftEdge
        cube.frontLeftEdge = self.backLeftEdge
        cube.frontRightEdge = self.backRightEdge
        cube.backRightEdge = self.frontRightEdge

        cube.bottomBackEdge = self.topFrontEdge
        cube.bottomLeftEdge = self.topLeftEdge
        cube.bottomFrontEdge = self.topBackEdge
        cube.bottomRightEdge = self.topRightEdge
        
        return cube
    
    def front_to_top(self):
        cube = Cube(self.front, self.back, self.bottom, self.top, self.left, self.right)

        cube.topBackEdge = self.topFrontEdge
        cube.topLeftEdge = self.frontLeftEdge
        cube.topFrontEdge = self.bottomFrontEdge
        cube.topRightEdge = self.frontRightEdge

        cube.backLeftEdge = self.topLeftEdge
        cube.frontLeftEdge = self.bottomLeftEdge
        cube.frontRightEdge = self.bottomRightEdge
        cube.backRightEdge = self.topRightEdge

        cube.bottomBackEdge = self.topBackEdge
        cube.bottomLeftEdge = self.backLeftEdge
        cube.bottomFrontEdge = self.bottomBackEdge
        cube.bottomRightEdge = self.backRightEdge
        
        return cube
    
    def back_to_top(self):
        cube = Cube(self.back, self.front, self.top, self.bottom, self.left, self.right)

        cube.topBackEdge = self.bottomBackEdge
        cube.topLeftEdge = self.backLeftEdge
        cube.topFrontEdge = self.topBackEdge
        cube.topRightEdge = self.backRightEdge

        cube.backLeftEdge = self.bottomLeftEdge
        cube.frontLeftEdge = self.topLeftEdge
        cube.frontRightEdge = self.topRightEdge
        cube.backRightEdge = self.bottomRightEdge

        cube.bottomBackEdge = self.bottomFrontEdge
        cube.bottomLeftEdge = self.frontLeftEdge
        cube.bottomFrontEdge = self.topFrontEdge
        cube.bottomRightEdge = self.frontRightEdge
        
        return cube
    
    def left_to_top(self):
        cube = Cube(self.left, self.right, self.front, self.back, self.bottom, self.top)

        cube.topBackEdge = self.backLeftEdge
        cube.topLeftEdge = self.bottomLeftEdge
        cube.topFrontEdge = self.frontLeftEdge
        cube.topRightEdge = self.topLeftEdge

        cube.backLeftEdge = self.bottomBackEdge
        cube.frontLeftEdge = self.bottomFrontEdge
        cube.frontRightEdge = self.topFrontEdge
        cube.backRightEdge = self.topBackEdge

        cube.bottomBackEdge = self.backRightEdge
        cube.bottomLeftEdge = self.bottomRightEdge
        cube.bottomFrontEdge = self.frontRightEdge
        cube.bottomRightEdge = self.topRightEdge
        
        return cube
    
    def right_to_top(self):
        cube = Cube(self.right, self.left, self.front, self.back, self.top, self.bottom)

        cube.topBackEdge = self.backRightEdge
        cube.topLeftEdge = self.topRightEdge
        cube.topFrontEdge = self.frontRightEdge
        cube.topRightEdge = self.bottomRightEdge

        cube.backLeftEdge = self.topBackEdge
        cube.frontLeftEdge = self.topFrontEdge
        cube.frontRightEdge = self.bottomFrontEdge
        cube.backRightEdge = self.bottomBackEdge

        cube.bottomBackEdge = self.backLeftEdge
        cube.bottomLeftEdge = self.topLeftEdge
        cube.bottomFrontEdge = self.frontLeftEdge
        cube.bottomRightEdge = self.bottomLeftEdge
        
        return cube
    
    def areFacesValid(self) -> bool:
        okFaceCount = 0
        for face in self.get_face_list():
            if face and face.isOrientationOk():
                okFaceCount += 1
            elif face is None:
                okFaceCount += 1
        return okFaceCount == 6
    
    def addEdge(self, faces: tuple, edge: Edge) -> None:
        if ("top" in faces):
            if ("back" in faces):
                self.topBackEdge = edge
            elif ("left" in faces):
                self.topLeftEdge = edge
            elif ("front" in faces):
                self.topFrontEdge = edge
            elif ("right" in faces):
                self.topRightEdge = edge
        elif ("bottom" in faces):
            if ("back" in faces):
                self.bottomBackEdge = edge
            elif ("left" in faces):
                self.bottomLeftEdge = edge
            elif ("front" in faces):
                self.bottomFrontEdge = edge
            elif ("right" in faces):
                self.bottomRightEdge = edge
        elif ("back" in faces):
            if ("left" in faces):
                self.backLeftEdge = edge
            elif ("right" in faces):
                self.backRightEdge = edge
        elif ("front" in faces):
            if ("left" in faces):
                self.frontLeftEdge = edge
            elif ("right" in faces):
                self.frontRightEdge = edge

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

def recursiveEdgeCheck(cube: Cube, newestFace: str, connectedFaces: list):
    validCubes = []
    # connectedFaces must be a list of tuples containing 3 elements: the X side, the X side's target edge, and the Y side's target edge, all strings
    cubeNewestFace = getattr(cube, newestFace)
    connectedFacesCopy = copy.deepcopy(connectedFaces)
    targetTuple = connectedFacesCopy.pop(0)
    cubeTargetFace = getattr(cube, targetTuple[0])
    sharedBudget = list(set(cubeTargetFace.remainingBudget) & set(cubeNewestFace.remainingBudget))
    if Edge.SPECIALFULL in sharedBudget and cubeNewestFace.facekind == cubeTargetFace.facekind:
        sharedBudget = [i for i in sharedBudget if i != Edge.SPECIALFULL]
    if Edge.SPECIALTRI in sharedBudget and cubeNewestFace.facekind == cubeTargetFace.facekind:
        sharedBudget = [i for i in sharedBudget if i != Edge.SPECIALTRI]
    for edge in sharedBudget:
        nextCube = copy.deepcopy(cube)
        nextCubeNewestFace = getattr(nextCube, newestFace)
        nextCubeTargetFace = getattr(nextCube, targetTuple[0])
        nextCube.addEdge((newestFace, targetTuple[0]), edge)
        #nextCubeTargetFace.x = edge
        setattr(nextCubeTargetFace, targetTuple[1], edge)
        nextCubeTargetFace.remainingBudget.remove(edge)
        #nextCubeNewestFace.y = edge
        setattr(nextCubeNewestFace, targetTuple[2], edge)
        nextCubeNewestFace.remainingBudget.remove(edge)

        # check and append cube, or recur
        if connectedFacesCopy:
            # recur
            validCubes.extend(recursiveEdgeCheck(nextCube, newestFace, connectedFacesCopy))
        else:
            # check and append if valid
            if nextCube.areFacesValid():
                validCubes.append(nextCube)
    return validCubes

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
            modCube = copy.deepcopy(cube)
            modCube.back = Face(face)
            cubeBacks.extend(recursiveEdgeCheck(modCube, "back", [("bottom", "a", "d")]))
    
    # find a way to drop cubes where the faces AND EDGES are the same
    cubeBacks = cullCubes(cubeBacks)

    cubeLefts = []
    for face in facekinds:
        for cube in cubeBacks:
            modCube = copy.deepcopy(cube)
            modCube.left = Face(face)
            cubeLefts.extend(recursiveEdgeCheck(modCube, "left", [("bottom", "b", "d"), ("back", "b", "c")]))

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
            modCube = copy.deepcopy(cube)
            modCube.front = Face(face)
            cubeFronts.extend(recursiveEdgeCheck(modCube, "front", [("bottom", "d", "d"), ("left", "b", "b")]))
    
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
            modCube = copy.deepcopy(cube)
            modCube.right = Face(face)
            cubeRights.extend(recursiveEdgeCheck(modCube, "right", [("bottom", "c", "d"), ("front", "c", "b"), ("back", "c", "c")]))
    
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
            modCube = copy.deepcopy(cube)
            modCube.top = Face(face)
            cubeTops.extend(recursiveEdgeCheck(modCube, "top", [("back", "a", "a"), ("left", "a", "b"), ("front", "a", "d"), ("right", "a", "c")]))
    
    cubeTops = cullCubes(cubeTops)
    for cube in cubeTops:
        print()
        print(cube.bottom.facekind, cube.back.facekind, cube.left.facekind, cube.front.facekind, cube.right.facekind, cube.top.facekind)
        # print(cube.bottom.a, cube.bottom.b, cube.bottom.d, cube.bottom.c)
        # print(cube.back.b)
        # print(cube.left.b)
        # print(cube.front.c)
        # print(cube.right.c)
        # print(cube.top.a, cube.top.b, cube.top.d, cube.top.c)
        print(cube.bottomBackEdge, cube.bottomLeftEdge, cube.bottomFrontEdge, cube.bottomRightEdge)
        print(cube.backLeftEdge)
        print(cube.frontLeftEdge)
        print(cube.frontRightEdge)
        print(cube.backRightEdge)
        print(cube.topBackEdge, cube.topLeftEdge, cube.topFrontEdge, cube.topRightEdge)
    print(len(cubeTops))
    
    #TODO: should I legalize the inverse of the 2 triangle 4 void blocks? solution should be to give squares the specialtri rules like voids
    #TODO: or, remove specialtri?