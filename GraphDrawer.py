import matplotlib.pyplot as plt
import networkx as nx

import dash
import dash_cytoscape as cyto
import plotly
import plotly.graph_objects as go
import ctypes

import networkx as nx
import dash_html_components as html
from dash.dependencies import Output, Input
from flask import Flask, render_template, json


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

    def draw2(self, arr, filenames):
        screen_size = self.__get_screen_size()
        filenames = self.__prepare_file_names(filenames)

        app = dash.Dash(__name__)
        app.layout = html.Div([
            self.__get_cytoscape(arr, filenames, screen_size),
            html.P(id='cytoscape-tapNodeData-output'),
            html.P(id='cytoscape-tapEdgeData-output'),
            html.P(id='cytoscape-mouseoverNodeData-output'),
            html.P(id='cytoscape-mouseoverEdgeData-output')
        ])

        self.__define_callbacks(app)

        app.run_server(debug=True)

    def __define_callbacks(self, app):
        @app.callback(Output('cytoscape-tapNodeData-output', 'children'),
                      [Input('container', 'tapNodeData')])
        def displayTapNodeData(data):
            if data:
                print("You recently clicked/tapped the city: " + data['label'])

        @app.callback(Output('cytoscape-tapEdgeData-output', 'children'),
                      [Input('container', 'tapEdgeData')])
        def displayTapEdgeData(data):
            if data:
                print("You recently clicked/tapped the edge between " + data['source'].upper() + " and " + data[
                    'target'].upper())

        @app.callback(Output('cytoscape-mouseoverNodeData-output', 'children'),
                      [Input('container', 'mouseoverNodeData')])
        def displayTapNodeData(data):
            if data:
                print("You recently hovered over the city: " + data['label'])

        @app.callback(Output('cytoscape-mouseoverEdgeData-output', 'children'),
                      [Input('container', 'mouseoverEdgeData')])
        def displayTapEdgeData(data):
            if data:
                print("You recently hovered over the edge between " + data['source'].upper() + " and " + data[
                    'target'].upper())

    def __get_cytoscape(self, arr, filenames, screen_size):
        return cyto.Cytoscape(
            id='container',
            elements=self.__get_elements(arr, filenames),
            style={
                'width': screen_size[0],
                'height': screen_size[1],
            },
            layout={
                'name': 'concentric',
            },
            stylesheet=self.__get_stylesheet()
        )

    def __get_screen_size(self):
        user32 = ctypes.windll.user32
        return user32.GetSystemMetrics(0) - 100, user32.GetSystemMetrics(1) - 100

    def __get_elements(self, arr, filenames):
        elements = []
        id_per_filename = dict()

        curr_id = 0
        for filename in filenames:
            elements.append({'data': {'id': curr_id, 'label': filename}})
            id_per_filename[filename] = curr_id
            curr_id += 1

        for (i, row) in enumerate(range(1, len(arr))):
            for col in range(0, i + 1):
                rgb_val = int((1.0 - arr[row][col]) * 256)
                rgb = 'rgb(' + str(rgb_val) + ',' + str(rgb_val) + ',' + str(rgb_val) + ')'
                elements.append({'data': {'source': id_per_filename.get(filenames[row]),
                                          'target': id_per_filename.get(filenames[col]),
                                          'label': arr[row][col],
                                          'weight': round(arr[row][col], 2),
                                          'size': 1,
                                          'rgb': rgb}})

        return elements

    def __get_stylesheet(self):
        return [
            {
                'selector': 'node',
                'style': {
                    'width': '7px',
                    'height': '7px',
                    'color': 'black',
                    'label': 'data(label)',
                    'font-size': '2px',
                    'text-outline-width': '0.3px',
                    'text-outline-color': 'white'
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'font-size': '2px',
                    'label': 'data(weight)',
                    'line-color': 'data(rgb)',
                    'line-style': 'solid',
                    'width': '0.5px',
                    'text-outline-width': '0.3px',
                    'text-outline-color': 'white',
                    'text-opacity': '1.0'
                }
            },
            {
                'selector': '[weight <= 0.3]',
                'style': {
                    'line-style': 'dotted',
                }

            },
            {
                'selector': '[weight <= 0.04]',
                'style': {
                     #'display': 'none'
                }
            }
        ]
