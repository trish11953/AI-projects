import os
import math
import heapq


if os.path.isfile("output.txt"):
    os.remove("output.txt")

file = open('input7.txt')
lines = file.read()
lines = lines.split('\n')

size, parent = [], {}
for i in lines[1].split(' '):
    size.append(int(i))

searchtype, start, end, numofnodes = lines[0], lines[2], lines[3], int(lines[4])


def move(place, p):
    global size
    if p == 1 or p == 7 or p == 8 or p == 11 or p == 12:
        place[0] = place[0] + 1
    if p == 2 or p == 9 or p == 10 or p == 13 or p == 14:
        place[0] = place[0] - 1
    if p == 3 or p == 7 or p == 9 or p == 15 or p == 16:
        place[1] = place[1] + 1
    if p == 4 or p == 8 or p == 10 or p == 17 or p == 18:
        place[1] = place[1] - 1
    if p == 5 or p == 11 or p == 13 or p == 15 or p == 17:
        place[2] = place[2] + 1
    if p == 6 or p == 12 or p == 14 or p == 16 or p == 18:
        place[2] = place[2] - 1
    if size[0] > place[0] >= 0 and size[1] > place[1] >= 0 and size[2] > place[2] >= 0:
        return place
    return None


def Graph(inputs) -> {}:
    adjacencylist = {}
    global numofnodes
    e = 5 + numofnodes
    for i in range(5, e):
        t = []
        for k in inputs[i].split(' '):
            t.append(int(k))
        position = []
        position.append(t[0])
        position.append(t[1])
        position.append(t[2])
        ls = [str(i) for i in position]
        node = ' '.join(ls)
        inp = t[3:]
        for k in inp:
            cur = list(position)
            position_new = move(cur, k)
            if position_new is not None:
                t = [str(i) for i in position_new]
                newnode = ' '.join(t)
                try:
                    adjacencylist[node].append(newnode)
                except KeyError:
                    adjacencylist[node] = [newnode]
    return adjacencylist


graph = Graph(lines)


def UniformCostSearch(start, end, graph):
    global parent
    visited, beginning = set(), []
    parent = {start: (None, 0)}
    front = {start: 0}
    heapq.heappush(beginning, (0, start))

    while True:
        if not beginning:
            return "FAIL"
        else:
            totalcost, currentnode = heapq.heappop(beginning)
            front.pop(currentnode)

        if end != currentnode:
            visited.add(currentnode)
            for n in graph.get(currentnode, []):
                newtotalcost = heuristic(currentnode, n) + totalcost
                if n in front:
                    if front[n] > newtotalcost:
                        front[n], parent[n] = newtotalcost, (currentnode, heuristic(currentnode, n))
                        b = len(beginning)
                        for temp in range(b):
                            if n == beginning[temp][1]:
                                beginning[temp] = (newtotalcost, n)
                        heapq.heapify(beginning)
                if n not in front:
                    if n not in visited:
                        parent[n] = (currentnode, heuristic(currentnode, n))
                        front[n] = newtotalcost
                        heapq.heappush(beginning, (newtotalcost, n))
        else:
            return totalcost


def BreadthFirstSearch(start, end, graph):
    global parent
    beginning, priority, visited = [], 0, set()
    heapq.heappush(beginning, (0, start, 0))
    parent[start] = (None, 0)
    visited.add(start)
    while True:
        if not beginning:
            return "FAIL"
        else:
            prioritynow, currentnode, totalcost = heapq.heappop(beginning)
        if currentnode != end:
            for n in graph.get(currentnode, []):
                if n not in visited:
                    visited.add(n)
                    parent[n] = (currentnode, 1)
                    heapq.heappush(beginning, (priority, n, 1 + totalcost))
                    priority = priority + 1
        else:
            return totalcost


def Astar(start, end, graph):
    beginning, visited = [], set()
    global parent
    parent = {start: (None, 0)}
    heapq.heappush(beginning, (heuristic(start, end), 0, start))
    while True:
        if not beginning:
            return "FAIL"
        else:
            heu, totalcost, current = heapq.heappop(beginning)
        if current != end:
            for i in graph.get(current, []):
                if i not in visited:
                    newcost, newheu = heuristic(current, i), heuristic(i, end)
                    parent[i] = (current, newcost)
                    estimate = newcost + totalcost + newheu
                    c = totalcost + newcost
                    heapq.heappush(beginning, (estimate, c, i))
                    visited.add(current)
        else:
            return totalcost


def heuristic(a, b):
    a = [int(i) for i in a.split(' ')]
    b = [int(i) for i in b.split(' ')]
    sq = math.sqrt(pow((10 * (a[0] - b[0])), 2) + pow((10 * (a[1] - b[1])), 2) + pow((10 * (a[2] - b[2])), 2))  # set formula
    euclidiandistance = math.floor(sq)
    return euclidiandistance


if searchtype == "BFS":
    shortestlength = BreadthFirstSearch(start, end, graph)
elif searchtype == "UCS":
    shortestlength = UniformCostSearch(start, end, graph)
else:
    shortestlength = Astar(start, end, graph)

file = open("output.txt", "w")
if shortestlength != "FAIL":
    present, pth, cost = end, [], []
    while present is not None:
        par, cst = parent[present]
        pth.append(present)
        present = par
        cost.append(cst)
    pth, cost = pth[::-1], cost[::-1]
    s = len(cost)
    st = str(shortestlength)
    l = str(len(pth))
    file.write(st + '\n' + l + '\n')
    for i in range(s):
        strin = str(cost[i])
        file.write(pth[i] + ' ' + strin + '\n')
else:
    file.write(shortestlength)
file.close()
