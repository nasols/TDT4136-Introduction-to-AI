
import numpy as np
from Map import *
import math

# node object to keep track of the different nodes properties. 
class Node:

    def __init__(self, coordinates, previousNode):
        self.coordinates = coordinates
        self.previousNode = previousNode
        
        self.g = 0
        self.h = 0
        self.f = 0

        self.value = 0
    
    # calculates and sets the f-score
    def setF(self):
        self.f = self.g + self.h

    # stores the value for the point in the map this node belongs to
    def setValue(self):
        self.value = data[self.coordinates[0]][self.coordinates[1]]
        

# calculates the H-score
def calc_H(currentPos, endPos):
    dx = endPos[0] - currentPos[0]
    dy = endPos[1] - currentPos[1]
    return math.sqrt(dx*dx + dy*dy)

# compares coordinates of two input nodes, return true or false depending on if they are equal 
def compareNodes(node1, node2): 
    cord1 = node1.coordinates
    cord2 = node2.coordinates 

    return cord1 == cord2 

# function that returns the node in array with lowest f-cost
def findBestNode(arr): 
    bestNode = arr[0]
    for node in arr: 
        if node.f < bestNode.f: 
            bestNode = node
        
    return bestNode



def a_star(data, start, end): 
   
    path = [] ## path to goal, nodes are put in this array at the end
    consideration = [] ## nodes not visited but under consideration
    visited = [] # nodes done with 

    start = Node(start, None) ## makes start node 
    
    end = Node(end, None) ## makes end node 

    start.h = calc_H(start.coordinates, end.coordinates) ## sets the start node h-score then f-score, g-score = 0 
    start.setF()

    currentNode = start # first node is the start node, currentnode = startnode
    
    ## adds the start point to consideration list to use as the first point we move from. Also adds to the list over visited points
    consideration.append(start)
    visited.append(start)

    ## just to ensure no infinite while loops. This approach wont work for any size map and therefore need to increase i-max value if you increase the map size
    running = True 
    i = 0

    while running:
        # just stops the wile loop 
        i += 1
        if i == 1000:
            for node in consideration:
                data[node.coordinates[0]][node.coordinates[1]] = 5   
                       
            running = False

        #creates the neighboor nodes and gives them the corresponding f, g and h cost, left right up and down 

        list = []
        if currentNode.coordinates[1] - 1 < 39:
            left = Node((currentNode.coordinates[0], currentNode.coordinates[1] - 1), currentNode)
            left.h = calc_H(left.coordinates, end.coordinates)
            left.setValue()
            left.g = currentNode.g + left.value 
    
            left.setF()
            if left.value != -1: 
                list.append(left)
            
        

        if (currentNode.coordinates[1] + 1 < 39): 
            right = Node((currentNode.coordinates[0], currentNode.coordinates[1] + 1) , currentNode)
            right.setValue()
            right.g = currentNode.g + right.value 
            right.h = calc_H(right.coordinates, end.coordinates)
            
            right.setF()
            if right.value != -1: 
                list.append(right)

        
        if currentNode.coordinates[0] - 1 < 47:
            up = Node((currentNode.coordinates[0] - 1, currentNode.coordinates[1]) , currentNode)
            up.setValue()
            up.g = currentNode.g + up.value 
            up.h = calc_H(up.coordinates, end.coordinates)

            up.setF()
            if up.value != -1: 
                list.append(up)
    
        if currentNode.coordinates[0] + 1 < 47:
            down  = Node((currentNode.coordinates[0] + 1, currentNode.coordinates[1]) , currentNode)
            down.setValue()
            down.g = currentNode.g + down.value 
          
            down.h = calc_H(down.coordinates, end.coordinates)

            down.setF()
            if down.value != -1: 
                list.append(down)

        
        # removing if its a wall
        for index, node in enumerate(list): 
            if node.value == -1:
                list.pop(index)
        
        for node in list: 
            check = False

            # removing if up down left or right is already in consideration list 
            for consnode in consideration: 
                
                if compareNodes(node, consnode) == True:
                    check = True 
            
            # removing if up down left or right is already in visited list
            for visitNode in visited:
                if compareNodes(node, visitNode) == True:
                    check = True
            
            # adds point to consideration list if it fulfills the previous conditions (not a wall, not already in consideration or visited)
            if check == False: 
                consideration.append(node)      

       
           
        #finding smallest f cost and setting this node as the current node. 
        # stroring previous node so that we can detect if the algorithm is stuck in some corner. Then the smallest f-cost still would be the same node, so we need to choose the next best node, next lowest f-cost
        prevNode = currentNode
        currentNode = findBestNode(consideration)

        # if current node not equal to previous node: remove from consideration, since we now have chosen this point. Add it to visited
        if currentNode != prevNode: 
            consideration.remove(currentNode)
            visited.append(currentNode)

        # if current node equal to previous node we find the next biggest! (since the consideration list now lacks the point with smallest f-cost, the now lowest f-cost node is the original next best point)
        elif currentNode == prevNode: 
            currentNode = findBestNode(consideration)
            consideration.remove(currentNode)
            visited.append(currentNode)
            

        # if currentNode == endNode, quit, we found our goal
        if currentNode.coordinates[0] == end.coordinates[0] and currentNode.coordinates[1] == end.coordinates[1]:
             
            ## going through all the parent nodes to retrieve the path taken to the goal
            path.append(currentNode)
            previousNode = currentNode.previousNode
            j = 0
            while previousNode != None:
                j += 1
                if j == 100: 
                    break
                
                path.append(previousNode)
                previousNode = previousNode.previousNode
                

            for node in path:
                data[node.coordinates[0], node.coordinates[1]] = 5
                print('g score: ', node.g, ' --- ' + 'h score: ', node.h)

            
            return np.array(data)

        
        

def drawPath(map):
        # Define width and height of image
        width = map.shape[1]
        height = map.shape[0]


        
        # Define scale of the image
        scale = 20
        # Create an all-yellow image
        image = Image.new('RGB', (width * scale, height * scale), (255, 255, 0))
        # Load image
        pixels = image.load()

        # Define what colors to give to different values of the string map (undefined values will remain yellow, this is
        # how the yellow path is painted)
        colors = {
                -1: (255, 0, 0), 
                1: (215, 215, 215), 
                2: (166, 166, 166), 
                3: (96, 96, 96), 
                4: (36, 36, 36),
                5: (255, 251, 0) 
                }
                 

        """{
            ' # ': (255, 0, 0), 
            ' . ': (215, 215, 215), 
            ' , ': (166, 166, 166), 
            ' : ': (96, 96, 96),
            ' ; ': (36, 36, 36), 
            ' S ': (255, 0, 255), 
            ' G ': (0, 128, 255)
        }"""

        # Go through image and set pixel color for every position
        for y in range(height):
            for x in range(width):
                if map[y][x] not in colors: continue
                for i in range(scale):
                    for j in range(scale):
                        pixels[x * scale + i, y * scale + j] = colors[map[y][x]]
        # Show image
        image.show()   
        


map = Map_Obj(task=4) ## adjust this to change the task, also need to change the path string on the next line to load the correct map. 1 = map_1, 2 = map_1, 3 = map_2, 4 = map_Edgar_full, 5 = map_2
data, size = map.read_map("/Users/jonasolsen/Documents/Skole/IIkt/3_Semester/Introduksjon_til_kunstig_intelligens/Øvinger/kunstig_repo/astar/Samfundet_map_Edgar_full.csv")
start = map.get_start_pos()
end = map.get_end_goal_pos()

data = a_star(data, start, end)
#map.show_map()
print(data)
drawPath(data)

















    
   













    
   


    







