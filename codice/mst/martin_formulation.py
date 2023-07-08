import matplotlib.pyplot as plt
import networkx as nx
from pyqubo import Binary, Placeholder, Constraint
from neal import SimulatedAnnealingSampler

#######################################################################################################################
# Nota sui file
# I file contenenti i grafi contengono i dati salvati secondo il formato:
# vertex0,...,vertexN nella prima riga
# source,target,weight nelle righe successive
#######################################################################################################################
edges = {}
with open('4v_5e.txt') as f:
    lines = [l.strip() for l in f.readlines()]
    nodes = {int(v) for v in lines[0].split(',')}
    for e in lines[1:]:
        vals = [int(x) for x in e.split(',')]
        edges[(vals[0], vals[1])] = vals[2]

#######################################################################################################################
# Visualizzazione del grafo in input tramite networkx
#######################################################################################################################
graph = nx.Graph()
for n in nodes:
    graph.add_node(n)
for edge, w in edges.items():
    graph.add_edge(edge[0], edge[1], weight=w)
edge_labels = nx.get_edge_attributes(graph, 'weight')

pos = nx.spring_layout(graph, k=5)
nx.draw(graph, pos, with_labels=True, node_size=500, node_color='lightblue', font_weight='bold')
nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
plt.show()

#######################################################################################################################
# Variabili binarie del problema
#######################################################################################################################
bin_vars = {f'x_{e[0]}_{e[1]}': Binary(f'x_{e[0]}_{e[1]}') for e in edges}

for s, t in edges.keys():
    for n in nodes:
        bin_vars[f'y_{s}_{t}^{n}'] = Binary(f'y_{s}_{t}^{n}')
        bin_vars[f'y_{t}_{s}^{n}'] = Binary(f'y_{t}_{s}^{n}')

#######################################################################################################################
# Vincoli del problema
#######################################################################################################################
for s, t in edges.keys():
    for n in nodes.difference({s, t}):
        bin_vars[f'y_{s}_{n}^{t}'] = Binary(f'y_{s}_{n}^{t}')

obj = sum(w * bin_vars[f'x_{e[0]}_{e[1]}'] for e, w in edges.items())
constraint_1 = Constraint((sum(bin_vars[f'x_{e[0]}_{e[1]}'] for e in edges) - (len(nodes) - 1)) ** 2,
                          label='constraint_1')
constraints_2 = []
i = 1
for s, t in edges.keys():
    for n in nodes:
        constraints_2.append(Constraint((bin_vars[f'y_{s}_{t}^{n}']
                                         + bin_vars[f'y_{t}_{s}^{n}']
                                         - bin_vars[f'x_{s}_{t}']) ** 2,
                                        label=f'constraint_2_{i}'))
        i += 1
constraints_num = 1 + len(constraints_2)
constraints_3 = [
    Constraint(
        (
                sum(bin_vars[f'y_{s}_{n}^{t}'] for n in nodes.difference({s, t}))
                + bin_vars[f'x_{s}_{t}']
                - 1
        )
        ** 2,
        label=f'constraint_3_{i}',
    )
    for i, (s, t) in enumerate(edges.keys(), start=1)
]
constraints_num += len(constraints_3)

print(f'Numero di vincoli del problema: {constraints_num} - G({len(nodes)}, {len(edges)})')

#######################################################################################################################
# Formulazione QUBO
#######################################################################################################################
laplace = Placeholder('L')
ham_function = obj \
               + laplace * constraint_1 \
               + sum(laplace * c2 for c2 in constraints_2) \
               + sum(laplace * c3 for c3 in constraints_3)
bqm = ham_function.compile().to_bqm(feed_dict={'L': 10})

#######################################################################################################################
# Campionamento Simulated Annealing
#######################################################################################################################
simulated_annealing = SimulatedAnnealingSampler()
sample_set = simulated_annealing.sample(bqm, num_reads=15, num_sweeps=100)
print('Sample set:\n', sample_set)
print('\nPrimo sample:')
print(sample_set.first)
