import random
import networkx as nx
import itertools
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
np.set_printoptions(precision = 2)

def readtxt(path , separator = ',' , decimal = '.'):
    F = open(path, 'r' , encoding='utf8')
    data = []
    data_dict = {}
    for line in F:
        if line != '\n':
            data.append(line.replace(decimal, '.').replace('\n', '').split(separator))
    F.close()
    criteria = data.pop(0)[1:]
    weights = [float(cell) for cell in data.pop(0)[1:]]
    vetos = [float(cell) for cell in data.pop(0)[1:]]
    for i, line in enumerate(data):
        data_dict[i] = [float(cell) for cell in line[1:]]
    return  criteria, weights, vetos, data_dict

def normalize(data, amin = 0, amax = 1):
    max_per_col = [max(col) for col in np.matrix([row for row in data.values()]).T.tolist()]
    min_per_col = [min(col) for col in np.matrix([row for row in data.values()]).T.tolist()]  
    normalized_data = {}
    for key in data:
        normalized_row = []
        for i, cell in enumerate(data[key]):
            normalized_row.append( amin + (amax - amin) * (cell - min_per_col[i]) / (max_per_col[i] - min_per_col[i]) )
        normalized_data[key] = normalized_row
    return normalized_data

def get_delta(data_dict):
    return max([max(col) - min(col) for col in np.matrix([row for row in data_dict.values()]).T.tolist()])

criteria, weights, vetos, data_dict = readtxt('data.csv')
delta = get_delta(data_dict)

concordance_matrix = np.ones((len(data_dict), len(data_dict)))
for pair in itertools.combinations(data_dict, 2):
    # print(pair)
    concordance_f_s = []
    concordance_s_f = []
    for i, w in enumerate(weights):
        if data_dict[pair[0]][i] > data_dict[pair[1]][i]:
            concordance_f_s.append(w)
        elif data_dict[pair[0]][i] < data_dict[pair[1]][i]:
            concordance_s_f.append(w)
        else:
            concordance_f_s.append(w)
            concordance_s_f.append(w)
    concordance_matrix[pair[0], pair[1]] = np.sum(concordance_f_s)
    concordance_matrix[pair[1], pair[0]] = np.sum(concordance_s_f)

discordance_matrix = np.zeros((len(data_dict), len(data_dict)))
for i in range(len(data_dict)):
	for j in range(len(data_dict)):
		for k in range(len(weights)):
			if data_dict[j][k] > data_dict[i][k] + vetos[k]:
				discordance_matrix[i][j] = 1

s = 0.65
concordance_matrix_2 = np.zeros((len(data_dict), len(data_dict)))
for i in range(len(data_dict)):
	for j in range(len(data_dict)):
		for k in range(len(weights)):
			if concordance_matrix[i][j] >= s:
				concordance_matrix_2[i][j] = 1
			else:
				concordance_matrix_2[i][j] = 0

data_dict_2 = {}
for key in data_dict:
	data_dict_2[key+1] = data_dict[key]

G = nx.DiGraph()
for n in data_dict_2:
    G.add_node(n)
dominance_matrix = np.zeros((len(data_dict), len(data_dict)))
for i in range(len(data_dict)):
	for j in range(len(data_dict)):
		if concordance_matrix_2[i, j] == 1 and discordance_matrix[i, j] == 0:
			dominance_matrix[i, j] = 1
			G.add_edge(i+1, j+1)

print('Grades:')
for key in data_dict:
	print(data_dict[key])
print(f'\nWeights: {weights}', '\n')
print(f'Vetos: {vetos}', '\n')
print('Concordance matrix:', '\n', concordance_matrix_2,'\n')
print('Disconcordance matrix:', '\n', discordance_matrix,'\n')
print('Dominance matrix:', '\n',dominance_matrix,'\n')

fig = plt.figure()
nx.draw_shell(G, with_labels = True, node_size=1000, node_color='g')
fig.savefig('dependence_graph.png')
plt.show()
