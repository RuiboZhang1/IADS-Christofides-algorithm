import math
import random

def euclid(p,q):
    x = p[0]-q[0]
    y = p[1]-q[1]
    return math.sqrt(x*x+y*y)


# class Tree:
#
#     def __init__(self):
#         self.node = None
#         self.left = None
#         self.right = None
#
#     def addVertex(self, vertex):
#         self.node = vertex
#
#     def addLeft(self, node):
#         self.left = node
#
#     def addRight(self, node):
#         self.right = node
#
#     def getVertex(self):
#         return self.node
#
#     def getLeft(self):
#         return self.Left
#
#     def getRight(self):
#         return self.right


                
class Graph:

    # Complete as described in the specification, taking care of two cases:
    # the -1 case, where we read points in the Euclidean plane, and
    # the n>0 case, where we read a general graph in a different format.
    # self.perm, self.dists, self.n are the key variables to be set up.
    def __init__(self,n,filename):
        self.dists = []
        self.nodes = None
        f = open(filename, "r")
        lines = f.readlines()
        if (n == -1):
            self.n = len(lines)
            self.dists = [[0] * self.n for i in range(self.n)]
            self.nodes = []
            #temp_points=[]
            for line in lines:
                x, y = map(int, line.split())
                self.nodes.append((x,y))
            for i in range(self.n):
                for j in range(i, self.n):
                    euclid_distance = euclid(self.nodes[i],self.nodes[j])
                    self.dists[i][j] = euclid_distance
                    self.dists[j][i] = euclid_distance
        else:
            self.n = n
            self.dists = [[0] * self.n for i in range(self.n)]
            for line in lines:
                x, y, dist = map(int,line.split())
                self.dists[x][y] = dist
                self.dists[y][x] = dist
        self.perm = [i for i in range(self.n)]


    # Complete as described in the spec, to calculate the cost of the
    # current tour (as represented by self.perm).
    def tourValue(self):
        tourvalue = 0
        for i in range(self.n):
            tourvalue += self.dists[self.perm[i]][self.perm[(i + 1) % self.n]]
        return tourvalue



    # Attempt the swap of cities i and i+1 in self.perm and commit
    # commit to the swap if it improves the cost of the tour.
    # Return True/False depending on success.
    def trySwap(self,i):
        currTourValue = self.tourValue()
        perm_copy = self.perm.copy()
        self.perm[i], self.perm[(i+1) % self.n] = self.perm[(i+1) % self.n], self.perm[i]
        newTourValue = self.tourValue()
        if currTourValue > newTourValue:
            return True
        else:
            self.perm = perm_copy
            return False


    # Consider the effect of reversiing the segment between
    # self.perm[i] and self.perm[j], and commit to the reversal
    # if it improves the tour value.
    # Return True/False depending on success.              
    def tryReverse(self,i,j):
        currentTourValue = self.tourValue()
        perm_copy = self.perm.copy()
        count = i

        while(j>=count):
            self.perm[i] = perm_copy[j]
            i += 1
            j -= 1
        newTourValue = self.tourValue()
        if currentTourValue > newTourValue:
            return True
        else:
            self.perm = perm_copy
            return False

    def swapHeuristic(self,k):
        better = True
        count = 0
        while better and (count < k or k == -1):
            better = False
            count += 1
            for i in range(self.n):
                if self.trySwap(i):
                    better = True

    def TwoOptHeuristic(self,k):
        better = True
        count = 0
        while better and (count < k or k == -1):
            better = False
            count += 1
            for j in range(self.n-1):
                for i in range(j):
                    if self.tryReverse(i,j):
                        better = True

                        
    # Implement the Greedy heuristic which builds a tour starting
    # from node 0, taking the closest (unused) node as 'next'
    # each time.
    def Greedy(self):
        unvisited_node = self.perm.copy()
        unvisited_node.remove(0)
        min_dist = math.inf
        for i in range(self.n-1):
            for j in unvisited_node:
                dist_between_node = self.dists[self.perm[i]][j]
                if(dist_between_node < min_dist):
                    min_dist = dist_between_node
                    node_being_visited = j
            unvisited_node.remove(node_being_visited)
            self.perm[i+1] = node_being_visited
            min_dist = math.inf
        return self.perm



    # Implement the Christofides heuristic
    # first find the minimum spanning tree T
    # Find the set of odd degree vertices O
    # Build minimum-weight perfect matching M from O
    # Combine T and M to form H
    # Form an Eulerian Circuit in H
    # discard repeated path


    def minimumSpanningTree(self):
        tree = []
        visited_nodes = [0]
        unvisited_nodes = [i for i in range(1, self.n)]


        while len(unvisited_nodes) > 0:
            start, end, min_dist = 0, 0, math.inf
            for i in visited_nodes:
                for j in unvisited_nodes:
                    if self.dists[i][j] < min_dist:
                        min_dist = self.dists[i][j]
                        start = i
                        end = j
            tree.append([start, end])
            visited_nodes.append(end)
            unvisited_nodes.remove(end)
        return tree

    def perfectMatching(self, tree):
        nodes = []
        oddNodes = []
        matchingTree = []
        matchedNodes = []
        minimumDist = math.inf
        for edge in tree:
            nodes.append(edge[0])
            nodes.append(edge[1])
        for i in range(self.n):
            if (nodes.count(i) % 2 != 0):
                oddNodes.append(i)

        for i in reversed(oddNodes):
            if (i in matchedNodes):
                continue
            for j in oddNodes:
                if (minimumDist == 1):
                    break
                if(i == j or j in matchedNodes):
                    continue
                else:
                    if(self.dists[i][j] < minimumDist):
                        minimumDist = self.dists[i][j]
                        matching = [i, j]
                        nodeMatched = j
            matchingTree.append(matching)
            matchedNodes.append(i)
            matchedNodes.append(nodeMatched)
            minimumDist = math.inf

        return matchingTree

    def eulerianCircuit(self, tree):
        # eulerian circuit to be returned
        circuit = []
        edge_numbers = [0 for i in range(self.n)]
        for i in tree:
            for j in range(self.n):
                if (j in i):
                    edge_numbers[j]+=1

        return self.dfs(0, tree, edge_numbers, circuit)

    # depth first search helper function
    def dfs(self, node, tree, edge_numbers, circuit):
        while(edge_numbers[node] != 0):
            for i in tree:
                if (node == i[0]):
                    next = i[1]
                    tree.remove(i)
                    edge_numbers[node] -= 1
                    edge_numbers[next] -= 1
                    circuit = self.dfs(next, tree, edge_numbers, circuit)
                elif (node == i[1]):
                    next = i[0]
                    tree.remove(i)
                    edge_numbers[node] -= 1
                    edge_numbers[next] -= 1
                    circuit = self.dfs(next, tree, edge_numbers, circuit)
        circuit.append(node)
        return (circuit)






    def removeDuplicate(self, circuit):
        self.perm = []
        [self.perm.append(i) for i in circuit if not i in self.perm]
        return


    def Christofides(self):

        # work for both case
        minSpanningTree = self.minimumSpanningTree()
        perfectMatch = self.perfectMatching(minSpanningTree)
        graph = minSpanningTree + perfectMatch
        eulerian = self.eulerianCircuit(graph)
        self.removeDuplicate(eulerian)

        return self.perm











