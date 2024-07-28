import osmnx as ox
import networkx as nx
import imageio as io
import matplotlib.pyplot as plt
import os

class Image_Manager:
    """
    The frames_path is the path where the frames are stored to create the gif.
    The save_path is the path where the gif and other important images will be saved.
    The desired_map is the map of the place.
    """
    def __init__(self, frames_path: str, save_path: str, desired_map: nx.MultiDiGraph, fps=30):
        self._frames_path = frames_path
        self._path = save_path
        self._map = map
        self._fps = fps

        self._counter = 0
        self._filenames = list()

        # This is were the nodes will be coloured
        self._fig, self._ax = ox.plot_graph(desired_map, figsize=(25, 25), show=False, close=False)

    def create_gif(self):
        with io.get_writer(f"{self._path}/animation.gif", mode='I', duration=1 / self._fps) as writer:
            for filename in self._filenames:
                image = io.imread(filename)
                writer.append_data(image)

        # for filename in filenames:
        #     os.remove(filename)

    def graph_main_nodes(self, start: dict[str, float], end: dict[str, float]):
        self._ax.scatter(start["x"], start["y"], c='green', s=100, zorder=5)

        self._ax.scatter(end["x"], end["y"], c='blue', s=100, zorder=5)

        plt.savefig(f"{self._frames_path}/{self._counter}.png")
        self._counter += 1
        self._filenames.append(f"{self._frames_path}/{self._counter}.png")

    def graph_new_common_node(self, node: dict[str, float]):
        self._ax.scatter(node["x"], node["y"], c='red', s=15, zorder=5)

        plt.savefig(f"{self._frames_path}/{self._counter}.png")
        self._counter += 1
        self._filenames.append(f"{self._frames_path}/{self._counter}.png")

    def plot_graph_route(self, route: list[int], color: str = 'b', linewidth: int = 6, node_size: int = 0, bgcolor: str = 'k', figsize: tuple[int, int] = (20, 20)):
        fig, ax = ox.plot_graph_route(
            self._map,
            route,
            route_color=color,
            route_linewidth=linewidth,
            node_size=node_size,
            bgcolor=bgcolor,
            figsize=figsize
        )
        plt.savefig(self._path)
