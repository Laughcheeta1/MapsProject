import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from Map import Map


place_name = "Los Angeles, California, USA"

print("Finished charging map")
start = {
    "x": -118.28370394467963,  # Cabrillo beach LA
    "y": 33.71031030523406
}

end = {
    "x": -118.64884798691931,  # Woodland hills LA
    "y": 34.18071555750413
}

map_solver = Map(start, end, place_name, create_gif=True)

print("Mapper created")

result = map_solver.search_path()

if result:
    print("Path successfully found")
    map_solver.get_solution()
else:
    print("Path not found")
