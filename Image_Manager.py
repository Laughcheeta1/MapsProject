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
    def __init__(self, frames_path: str, save_path: str, desired_map: str, fps=30):
        self._map = ox.graph_from_place(desired_map, network_type='drive', simplify=False)

        self._frames_path = frames_path
        self._path = save_path
        self._fps = fps

        self._counter = 0
        self._filenames = list()

        # This is were the nodes will be coloured
        self._fig, self._ax = ox.plot_graph(self._map, figsize=(25, 25), show=False, close=False)

    def create_gif(self, with_path=False, route: list[int]=None):
        writer = io.get_writer(f"{self._path}/animation.gif", mode='I', duration=1 / self._fps, loop=0)

        # with io.get_writer(f"{self._path}/animation.gif", mode='I', duration=1 / self._fps, loop=0) as writer:
        for filename in self._filenames:
            image = io.imread(filename)
            writer.append_data(image)
        
        if with_path:
            # TODO: Create the gif with the path
            print("Entered to create the gif with the path")
            self.plot_graph_route(route)

            final_path = f"{self._path}/finalpath.png"

            i = 0
            while not os.path.exists(final_path):
                time.sleep(0.05)  # Sleep for 50ms
                i += 1
                if i == 100:
                    print("The final image was not created")
                    break

            image = io.imread(f"{self._path}/finalpath.png")
            for _ in range(120):  # 4 seconds
                print("Entered path to the gif")
                writer.append_data(image)

        writer.close()

        for filename in self._filenames:
            if filename == "Why.txt":
                continue
            
            os.remove(filename)

    def graph_main_nodes(self, start: dict[str, float], end: dict[str, float]):
        self._ax.scatter(start["x"], start["y"], c='green', s=100, zorder=5)

        self._ax.scatter(end["x"], end["y"], c='blue', s=100, zorder=5)

        plt.savefig(f"{self._frames_path}/{self._counter}.png")
        self._filenames.append(f"{self._frames_path}/{self._counter}.png")
        self._counter += 1

    def graph_new_common_node(self, node: dict[str, float]):
        self._ax.scatter(node["x"], node["y"], c='red', s=15, zorder=5)

        plt.savefig(f"{self._frames_path}/{self._counter}.png")
        self._filenames.append(f"{self._frames_path}/{self._counter}.png")
        self._counter += 1

    def finish_plot(self):
        plt.close(self._fig)

    def plot_graph_route(self, route: list[int], color: str = 'b', linewidth: int = 6, node_size: int = 0, bgcolor: str = 'k', figsize: tuple[int, int] = (20, 20)):
        print("entered to plot the route")
        fig, ax = ox.plot_graph_route(
            self._map,
            route,
            route_color='b',
            route_linewidth=6,
            node_size=0,
            bgcolor='k',
            figsize=(20, 20),
            show=False,
            close=False
        )
        plt.savefig(f"{self._path}/finalpath.png")
        plt.close(fig)
        
