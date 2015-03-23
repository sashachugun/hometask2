import time
from xml.dom.minidom import parse, parseString
import sys
import csv
import matrixops
import copy
 
def count_resistance(Edges, n):
    d = [float('Inf')]*n
    for i in range(n):
        d[i] = [float('Inf')]*n
    for i in range(n):
        d[i][i] = 0
    for key in Edges:
        for i in Edges[key]:
            v = int(i[0])-1
            weigth = float(i[1])
            u = int(key)-1
            d[u][v] = 1/(1/float(d[u][v])+1/weigth)
    return d
 
 
def count_full_resistance(resis, n):
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if resis[i][j] == 0:
                    a = float('Inf')
                else:
                    a = 1/float(resis[i][j])
                if float(resis[i][k])+float(resis[k][j]) == 0:
                    b = float('Inf')
                else:
                    b = 1/(float(resis[i][k])+float(resis[k][j]))
                if (a + b) == 0:
                    resis[i][j] = float('Inf')
                else:
                    resis[i][j] = 1/(a+b)
    return resis
 
 
def make_csv(filename, resis_matrix):
    f = open(filename, 'w')
    for r in resis_matrix:
        for el in r:
            f.write('%.6f,' % el)
        f.write('\n')
    f.close()
 

input_file = sys.argv[1]
output_file = sys.argv[2]
 
doc = parse(input_file)
nodes = doc.getElementsByTagName("net")
length = len(nodes)
 
edges = dict()
for d in doc.getElementsByTagName("diode"):
    if not d.getAttribute("net_from") in edges:
        edges[d.getAttribute("net_from")] = []
    edges[d.getAttribute("net_from")] += [[d.getAttribute("net_to"), d.getAttribute("resistance")]]
 
    if not d.getAttribute("net_to") in edges:
        edges[d.getAttribute("net_to")] = []
    edges[d.getAttribute("net_to")] += [[d.getAttribute("net_from"), d.getAttribute("reverse_resistance")]]
 
for r in doc.getElementsByTagName("resistor"):
    if not r.getAttribute("net_from") in edges:
        edges[r.getAttribute("net_from")] = []
    edges[r.getAttribute("net_from")] += [[r.getAttribute("net_to"), r.getAttribute("resistance")]]
 
    if not r.getAttribute("net_to") in edges:
        edges[r.getAttribute("net_to")] = []
    edges[r.getAttribute("net_to")] += [[r.getAttribute("net_from"), r.getAttribute("resistance")]]
 
for c in doc.getElementsByTagName("capactor"):
    if not c.getAttribute("net_from") in edges:
        edges[c.getAttribute("net_from")] = []
    edges[c.getAttribute("net_from")] += [[c.getAttribute("net_to"), c.getAttribute("resistance")]]
    if not c.getAttribute("net_to") in edges:
        edges[c.getAttribute("net_to")] = []
    edges[c.getAttribute("net_to")] += [[c.getAttribute("net_from"), c.getAttribute("resistance")]]
resistance_matrix = count_resistance(edges, length)
r_m =copy.deepcopy(resistance_matrix)
 
time_start = time.clock()
full_resistance_matrix = count_full_resistance(r_m, length)
time_finish = time.clock()
 
time_start_cpp = time.clock()
res_by_cpp = matrixops.Floyd_Warshall(resistance_matrix)
time_finish_cpp = time.clock()
 
make_csv('python.csv',full_resistance_matrix) 
make_csv(output_file,res_by_cpp )
 
print((time_finish- time_start)/(time_finish_cpp - time_start_cpp))
