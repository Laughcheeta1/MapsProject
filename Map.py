from Map_node import Node
from NetworkManager import Manager
import networkx
import queue


class Map:
    def __init__(self,
                 initial_state: dict[str, float],
                 goal_state: dict[str, float],
                 desired_map: networkx.MultiDiGraph
                 ):
        self._manager = Manager(desired_map)

        # Get the node code for the initial_state:

        self._root = Node(
            code=self._manager.get_code(initial_state),
            state=initial_state,
            heuristic=self._calculate_heuristic(initial_state)
        )

        self._goal_state = goal_state
        self._map = desired_map

        self._next = queue.PriorityQueue()

        self._solution = None
        self._final_node = None

    def get_solution(self) -> list[Node]:
        if not self._final_node:
            return list()

        self._path_objective()
        return self._solution

    """
    Search for the best path to the goal with the A* algorithm
    returns True if it found a path, else, False
    """
    def search_path(self) -> bool:
        current_node = self._root

        while not self._is_goal(current_node) and not self._next.empty():
            self._add_children(current_node)
            current_node = self._next.get()

        if self._is_goal(current_node):
            self._final_node = current_node
            return True

        return False

    def _add_children(self, node: Node) -> None:
        code = node.get_code()

        # Iterate through all the neighbours and add them to the queue
        # This method of _map, returns an Iterator to all the neighbours (the codes of the neighbours)
        for neighbour in self._manager.get_neighbours(code):
            coordinates = self._manager.get_coordinates(neighbour)  # Get the neighbour coordinates

            new_node = Node(  # Create the node for the neighbour
                            code=neighbour,
                            state=coordinates,
                            heuristic=self._calculate_heuristic(coordinates),
                            cost=self._calculate_cost(
                                parent=node,
                                distance_traveled=self._manager.get_edge_distance(code, neighbour)
                            ),
                            parent=node
                        )

            if not self._repeated_state(new_node):
                self._next.put(new_node)

    def _is_goal(self, node: Node) -> bool:
        return node.get_state() == self._goal_state

    def _calculate_heuristic(self, state: dict[str, float]) -> float:
        # TODO: Implement a more complex heuristic
        return self._manager.get_circle_distance(state["x"], state["y"], self._goal_state["x"], self._goal_state["y"])

    def _calculate_cost(self, parent: Node, distance_traveled: float) -> float:
        # TODO: Implement a more complex calculation
        return parent.get_cost() + distance_traveled

    def _repeated_state(self, node: Node) -> bool:
        n = node
        while n is not None and n.get_state() != node.get_state():
            n = n.get_parent()

        return n is not None

    def _path_objective(self) -> None:
        n = self._final_node

        result = list()
        while n is not None:
            result.append(n)
            n = n.parent

        self._solution = result
