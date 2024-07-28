import networkx
import osmnx.distance as osd


"""
We create this manager app to do all the important operations with the networkx and osmnx libraries.
So basically, to follow SOLID principles
"""


class Manager:
    def __init__(self, desired_map: networkx.MultiDiGraph):
        self._map = desired_map

    """
    Returns the coordinates of a node in the map
    """
    def get_coordinates(self, code) -> dict[str, float]:
        return {
            "x": self._map.nodes[code]["x"],
            "y": self._map.nodes[code]["y"]
        }

    """
    Returns the distance of the edge between two nodes
    """
    def get_edge_distance(self, node1: int, node2: int) -> float:
        return self._map.edges[node1, node2, 0]["length"]

    """
    Returns an iterable to the node's neighbours
    """
    def get_neighbours(self, code: int):
        return self._map.neighbors(code)

    """
    Get the code for the nearest node in the graph to the specified coordinates
    """
    def get_code(self, coordinates: dict[str, float]) -> int:
        return osd.nearest_nodes(self._map, X=coordinates["x"], Y=coordinates["y"])

    """
    Returns the great circle distance between two coordinates
    """
    def get_distance_nodes(self, x1, y1, x2, y2):
        return osd.great_circle(x1, y1, x2, y2)
