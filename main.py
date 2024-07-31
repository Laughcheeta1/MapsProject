import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

from Map import Map


DESIRED_MAP = os.getenv("DESIRED_MAP")
START_COORDINATES = os.getenv("START_COORDINATES").split(" ")
END_COORDINATES = os.getenv("END_COORDINATES").split(" ")

print("Finished charging map")
start = {
    "x":START_COORDINATES[0] ,  # Cerca de la Universidad del Sur de California (USC)
    "y": START_COORDINATES[1]
}

end = {
    "x": END_COORDINATES[0],  # Cerca del Museo de Historia Natural del Condado de Los Ángeles
    "y": END_COORDINATES[1]
}

map_solver = Map(start, end, DESIRED_MAP, create_gif=False)

print("Mapper created")

result = map_solver.search_path()

if result:
    print("Path successfully found")
    map_solver.get_solution()
else:
    print("Path not found")
