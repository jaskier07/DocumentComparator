import networkx as nx
import matplotlib.pyplot as plt


class GraphDrawer:

    def draw(self, array, filenames):
        g = self.__getGraph(array, filenames)

        plt.figure(figsize=(10, 10))

        pos = nx.spring_layout(g)
        edges = g.edges()
        weights = [g[u][v]['weight'] * 10 for u, v in edges]

        nx.draw(g, pos, with_labels=True, node_size=400, node_color="skyblue", node_shape=".", font_size=11,
                width=weights)

        weights = [round(g[u][v]['weight'], 4) for u, v in edges]
        edges = dict(zip(edges, weights))

        nx.draw_networkx_edge_labels(g, pos, edge_labels=edges)
        plt.show()

    def __getGraph(self, array, titles):
        g = nx.Graph()
        for i in range(len(array[0])):
            for j in range(i + 1, len(array[0])):
                g.add_edge(titles[i], titles[j], weight=array[i][j])
        return g
