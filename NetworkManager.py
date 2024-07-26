import networkx


"""
We create this manager app to do all the important operations with the networkx library.
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
    def get_node_distance(self, node1: int, node2: int) -> float:
        pass

    def get_neighbours(self, code):
        self._map.neighbors(code)
