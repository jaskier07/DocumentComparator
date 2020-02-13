import ctypes

import dash
import dash_cytoscape as cyto
import dash_html_components as html
from dash.dependencies import Output, Input
from dash_cytoscape import Cytoscape


class GraphDrawer:
    __MIN_EDGE_WEIGHT = 0.04
    __EDGE_WEIGHT_PRECISION = 4
    __MAX_NODE_NAME_LENGTH = 25

    cytoscape: Cytoscape
    similarity_arr: None
    screen_size: None

    __stylesheet = [
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
        # {
        #     'selector': '[weight <= 0.3]',
        #     'style': {
        #         'line-style': 'dotted',
        #     }
        #
        # },
        # {
        #     'selector': '[weight <= 0.1]',
        #     'style': {
        #         'display': 'none'
        #     }
        # }
    ]

    def __init__(self) -> None:
        self.screen_size = self.__get_screen_size()

    def draw(self, arr, filenames):
        self.similarity_arr = arr
        self.cytoscape = self.__get_cytoscape(arr, self.__prepare_file_names(filenames), self.screen_size)

        app = dash.Dash(__name__)
        app.layout = html.Div([
            self.cytoscape,
            html.P(id='cytoscape-tapNodeData-output'),
            html.P(id='cytoscape-tapEdgeData-output'),
            html.P(id='cytoscape-broker')
        ])

        self.__define_callbacks(app)
        app.run_server(debug=True)

        # thread = Thread(target=app.run_server)

    # thread.start()

    def __prepare_file_names(self, file_names):
        short_file_names = []
        for i in range(len(file_names)):
            name = file_names[i][:self.__MAX_NODE_NAME_LENGTH] + '...' \
                if len(file_names[i]) > self.__MAX_NODE_NAME_LENGTH else file_names[i]
            short_file_names.append(name)

        return short_file_names

    def __define_callbacks(self, app):
        @app.callback(Output('container', 'stylesheet'),
                      [Input('container', 'tapNodeData'), Input('container', 'elements')])
        def save_container_elements(selected_node, all_elements):
            new_styles = [
                {
                    'selector': 'edge',
                    'style': {
                        'background-color': 'black'
                    }
                }
            ]

            if selected_node and all_elements:
                for e in all_elements:
                    element = e.get('data')
                    id_condition = 'edge[id = "{}"]'.format(element.get('id'))
                    if element.get('source') == selected_node['id'] or element.get('target') == selected_node['id']:
                        new_styles.append(
                            {
                                'selector': id_condition,
                                'style': {
                                    'weight': '1',
                                    'background-color': 'red',
                                    'font-size': '2px',
                                    'label': 'data(weight)',
                                    'line-color': 'black',
                                    'line-style': 'solid',
                                    'width': '0.5px',
                                    'text-outline-width': '0.3px',
                                    'text-outline-color': 'white',
                                    'text-opacity': '1.0',
                                    'hidden': 'false'
                                }
                            }
                        )
                    elif element.get('source') is not None:
                        new_styles.append(
                            {
                                'selector': id_condition,
                                'style': {
                                    'background-color': 'green',
                                    'hidden': 'true',
                                    'width': '0'
                                }
                            }
                        )

            return self.__stylesheet + new_styles

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
            stylesheet=self.__stylesheet
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
                                          'rgb': rgb
                                          }})

        return elements
