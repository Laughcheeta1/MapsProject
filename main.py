import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from Map import Map


G = ox.graph_from_place('Los Angeles, California, USA', network_type='drive', simplify=False)

print("Finished charging map")
start = {
    "x": -118.28370394467963,  # Cabrillo beach LA
    "y": 33.71031030523406
}

end = {
    "x": -118.64884798691931,  # Woodland hills LA
    "y": 34.18071555750413
}

map_solver = Map(start, end, G)

print("Mapper created")

result = map_solver.search_path()

if result:
    print("Path successfully found")
    solution_path = map_solver.get_solution()
    ox.plot_graph_route(
        G,
        solution_path,
        route_color='b',
        route_linewidth=6,
        node_size=0,
        bgcolor='k',
        figsize=(20, 20)
    )
else:
    print("Path not found")


fig, ax = ox.plot_graph(G, figsize=(25, 25), show=False, close=False)

for node in map_solver.visited_print:
    x, y = G.nodes[node]['x'], G.nodes[node]['y']
    ax.scatter(x, y, c='red', s=20, zorder=5)

x, y = G.nodes[map_solver._root.get_code()]['x'], G.nodes[map_solver._root.get_code()]['y']
ax.scatter(x, y, c='green', s=100, zorder=5)

x, y = G.nodes[map_solver._goal_state_code]['x'], G.nodes[map_solver._goal_state_code]['y']
ax.scatter(x, y, c='blue', s=100, zorder=5)

plt.show()