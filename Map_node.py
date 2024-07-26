class Node:
    """
    code: the code if the networkx map
    state: the actual coordinates
    heuristic: the heuristic
    cost: the cost of getting to this node
    parent: the previous node
    """

    def __init__(self, code: int, state: dict[str, float], heuristic: float, cost: float = 0, parent: 'Node' = None):
        self._code = code
        self._state = state
        self._heuristic = heuristic
        self._cost = cost
        self._parent = parent

        self._children = list()

    def add_child(self, code: int, state: dict[str, float], heuristic: float, cost: float, parent: 'Node') -> 'Node':
        self._children.append(Node(code, state, heuristic, cost, parent))
        return self._children[-1]

    def get_code(self):
        return self._code

    def get_children(self) -> list['Node']:
        return self._children

    def get_state(self) -> dict[str, float]:
        return self._state

    def get_f(self) -> float:
        return self._heuristic + self._cost

    def get_cost(self) -> float:
        return self._cost

    def get_parent(self) -> 'Node':
        return self._parent

    def __eq__(self, other: 'Node') -> bool:
        return self._state == other.get_state()

    def __lt__(self, other: 'Node') -> bool:
        return self.get_f() < other.get_f()
