from Map_Node import Node
from Network_Manager import Manager
from Image_Manager import Image_Manager

import networkx


class Map:
    def __init__(self,
                 initial_state: dict[str, float],
                 goal_state: dict[str, float],
                 desired_map: networkx.MultiDiGraph,
                 fps=30,
                 create_gif=False
                 ):
        self.visited_print: set[int] = set()

        self._manager = Manager(desired_map)
        if create_gif:
            self._image_manager = Image_Manager("frames", "Final_Products", desired_map, fps)

        self._map = desired_map
        self._create_gif = create_gif

        """
        Since the coordinates of the nearest node to the goal state and the goal state 
        are not necessarily the same, we have to work with the coordinates (therefore code) of the
        nearest node to the goal state
        """
        # Get the code of the goal state node
        self._goal_state_code = self._manager.get_code(goal_state)
        # Get the coordinates of the goal state node
        self._goal_state_coordinates = self._manager.get_coordinates(self._goal_state_code)
        self._root = Node(
            code=self._manager.get_code(initial_state),
            state=initial_state,
            heuristic=self._calculate_heuristic(initial_state)
        )

        # Remember that the initial_state and goal_state are different from the actual nodes
        if create_gif:
            self._image_manager.graph_main_nodes(self._root.get_state(), self._goal_state_coordinates)

        """
        Not using a priority queue, since it is not iterable nor
        possible to get a specific element from it (proces I need in the _add_new_node method)
        
        It specifically is a map, since it still searches in O(1) like a set, and I can access a specific value.
        More info about the why in the why in the _add_new_node method. 
        """
        self._frontier: dict[int, Node] = dict()
        self._frontier[self._root.get_code()] = self._root
        self._visited: set[int] = set()  # All the nodes that have been visited

        # The variables where we will input the solutions
        self._solution = None
        self._final_node = None

    def get_solution(self) -> list[Node]:
        if self._create_gif:
            # Re-place the main nodes, so they are not overshadowed by the common nodes
            self._image_manager.graph_main_nodes(self._root.get_state(), self._goal_state_coordinates)

        if not self._final_node:
            if self._create_gif:
                self._image_manager.create_gif()  # Create the gif without the path
            return list()

        self._path_objective()

        if self._create_gif:
            self._image_manager.create_gif(True, self._solution)  # Create the gif with the path

        return self._solution

    """
    Search for the best path to the goal with the A* algorithm
    returns True if it found a path, else, False
    """
    def search_path(self) -> bool:
        current_node = None
        counter = 1
        while not self._is_goal(current_node) and len(self._frontier) != 0:
            current_node = self._get_next_node()
            self._visited.add(current_node.get_code())
            self._add_children(current_node)

            self.visited_print.add(current_node.get_code())
            if self._create_gif:
                self._image_manager.graph_new_common_node(current_node.get_state())
            counter += 1

        print(counter)
        
        if self._is_goal(current_node):
            self._final_node = current_node
            return True

        return False

    def _add_children(self, node: Node) -> None:
        code = node.get_code()

        # Iterate through all the neighbours and add them to the queue
        # This method of _map, returns an Iterator to all the neighbours (the codes of the neighbours)
        for neighbour in self._manager.get_neighbours(code):
            if neighbour in self._visited:
                continue  # If the neighbour has already been visited, then skip it
                # This because if we have visited it before, it means we have found a better path to it

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

            self._add_new_node(new_node)

    def _is_goal(self, node: Node) -> bool:
        if not node:  # Node is null
            return False  # TODO optimize this

        return node.get_code() == self._goal_state_code

    def _calculate_heuristic(self, state: dict[str, float]) -> float:
        # TODO: Implement a more complex heuristic
        return self._manager.get_distance_nodes(
            state["x"],
            state["y"],
            self._goal_state_coordinates["x"],
            self._goal_state_coordinates["y"]
        )

    def _calculate_cost(self, parent: Node, distance_traveled: float) -> float:
        # TODO: Implement a more complex calculation
        return parent.get_cost() + distance_traveled

    """
    Returns the list of the nodes (nodes represented in just the codes, to be able to graph_it)
    """
    def _path_objective(self) -> None:
        n: Node = self._final_node

        result = list()
        while n is not None:
            result.insert(0, n.get_code())
            n = n.get_parent()

        self._solution = result

    """
    Returns the next node to visit
    """
    def _get_next_node(self) -> Node:
        return self._frontier.pop(
            min(self._frontier.values()).get_code(),
            None
        )

    """
    It has this name because apparently is was overriding a method in a library

    This method is used to add a new node to the frontier. If this node has been visited before, then keep
    the state with the lowest f. If it has not been visited, then add it to the frontier.

    This because that way we optimize the search, since we are not saving (or potentially exploring) two states
    that point to the same node, instead we only keep the one that is probably going to give us the best result.
    """
    def _add_new_node(self, node):
        code = node.get_code()
        # If the node has already been visited, keep the one with the lowest f.
        # If it has not been visited, then add it
        if (code in self._frontier and node < self._frontier[code]) or code not in self._frontier:
            self._frontier[code] = node
