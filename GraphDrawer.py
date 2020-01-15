import matplotlib.pyplot as plt
import networkx as nx


class GraphDrawer:
    __MIN_EDGE_WEIGHT = 0.04
    __EDGE_WEIGHT_PRECISION = 4
    __MAX_NODE_NAME_LENGTH = 25

    def draw(self, array, file_names):
        g = self.__get_graph(array, self.__prepare_file_names(file_names))

        plt.figure(figsize=(10, 10))

        pos = nx.spring_layout(g)
        edges = g.edges()
        weights = [g[u][v]['weight'] * 10 for u, v in edges]

        nx.draw(g, pos, with_labels=True, node_size=1200, node_color="skyblue", node_shape="h", font_size=11, alpha=0.8,
                width=weights)

        weights = [round(g[u][v]['weight'], self.__EDGE_WEIGHT_PRECISION) for u, v in edges]
        edges = dict(zip(edges, weights))

        nx.draw_networkx_edge_labels(g, pos, edge_labels=edges)

        plt.show()

    def __get_graph(self, array, titles):
        g = nx.Graph()
        for i in range(len(array[0])):
            for j in range(i + 1, len(array[0])):
                edge_weight = array[i][j]
                if edge_weight > self.__MIN_EDGE_WEIGHT:
                    g.add_edge(titles[i], titles[j], weight=edge_weight)
        return g

    def __prepare_file_names(self, file_names):
        short_file_names = []
        for i in range(len(file_names)):
            name = file_names[i][:self.__MAX_NODE_NAME_LENGTH] + '...' \
                if len(file_names[i]) > self.__MAX_NODE_NAME_LENGTH else file_names[i]
            short_file_names.append(name)

        return short_file_names
