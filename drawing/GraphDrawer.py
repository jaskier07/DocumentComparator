import ctypes
from threading import Thread

import dash
import dash_cytoscape as cyto
import dash_html_components as html
import dash_core_components as core
from dash_cytoscape import Cytoscape

from drawing.CallbackProvider import CallbackProvider
from drawing.StylesheetProvider import StylesheetProvider


class GraphDrawer:
    __MIN_EDGE_WEIGHT = 0.04
    __EDGE_WEIGHT_PRECISION = 4
    __MAX_NODE_NAME_LENGTH = 25
    __DEFAULT_DROPDOWN_VALUE = '-1'

    filename_per_node_id = dict()
    similarity_arr: None
    screen_size: None
    demo_mode: bool
    stylesheetProvider = StylesheetProvider()

    def __init__(self, demo_mode: bool) -> None:
        self.screen_size = self.__get_screen_size()
        self.demo_mode = demo_mode

    def draw(self, arr, filenames):
        self.similarity_arr = arr
        prepared_filenames = self.__prepare_file_names(filenames)

        app = dash.Dash(__name__)
        elements, nodes_per_id, filename_per_node = self.__get_elements_and_filename_dict(arr, prepared_filenames)
        self.filename_per_node_id = filename_per_node

        app.layout = html.Div([
            self.__get_cytoscape(elements),
            self.__get_dropdown_with_documents(self.filename_per_node_id),
            html.P(id='cytoscape-tapNodeData-output'),
            html.P(id='cytoscape-tapEdgeData-output'),
            html.P(id='cytoscape-broker'),
            self.__get_dropdown_with_view()
        ])

        self.callbackProvider = CallbackProvider(self.__DEFAULT_DROPDOWN_VALUE, nodes_per_id)
        self.callbackProvider.define_callbacks(app)
        # TODO Moving thread creation to method in Application.py
        if self.demo_mode:
            app.run_server(debug=True)
        else:
            thread = Thread(target=app.run_server)
            thread.start()

    def __prepare_file_names(self, file_names):
        short_file_names = []
        for i in range(len(file_names)):
            name = file_names[i][:self.__MAX_NODE_NAME_LENGTH] + '...' \
                if len(file_names[i]) > self.__MAX_NODE_NAME_LENGTH else file_names[i]
            short_file_names.append(name)

        return short_file_names

    def __get_cytoscape(self, elements):
        return cyto.Cytoscape(
            id='container',
            elements=elements,
            style={
                'width': self.screen_size[0],
                'height': self.screen_size[1],
            },
            layout={
                'name': 'concentric',
            },
            stylesheet=self.stylesheetProvider.get_stylesheet(),
            maxZoom=10,
            minZoom=1
        )

    @staticmethod
    def __get_screen_size():
        user32 = ctypes.windll.user32
        return user32.GetSystemMetrics(0) - 100, user32.GetSystemMetrics(1) - 100

    def __get_elements_and_filename_dict(self, arr, filenames):
        elements = []
        node_per_id = dict()
        id_per_filename = dict()
        filename_per_node_id = dict()

        curr_id = 0
        for filename in filenames:
            node = {'data': {'id': curr_id, 'label': filename}}
            elements.append(node)
            node_per_id[curr_id] = node
            id_per_filename[filename] = curr_id
            filename_per_node_id[curr_id] = filename
            curr_id += 1

        for (i, row) in enumerate(range(1, len(arr))):
            for col in range(0, i + 1):
                rgb_val = int((1.0 - arr[row][col]) * 256)
                rgb = 'rgb(' + str(rgb_val) + ',' + str(rgb_val) + ',' + str(rgb_val) + ')'
                elements.append({'data': {'source': id_per_filename.get(filenames[row]),
                                          'target': id_per_filename.get(filenames[col]),
                                          'label': arr[row][col],
                                          'weight': self.__get_rounded_weight(arr[row][col]),
                                          'size': 1,
                                          'rgb': rgb
                                          }})

        return elements, node_per_id, filename_per_node_id

    @staticmethod
    def __get_rounded_weight(num):
        return round(num, 2)

    @staticmethod
    def __get_dropdown_with_view():
        return core.Dropdown(
            id='dropdown-view',
            value='concentric',
            clearable=False,
            options=[
                {'label': name.capitalize(), 'value': name}
                for name in ['grid', 'random', 'circle', 'cose', 'concentric']
            ]
        )

    def __get_dropdown_with_documents(self, filename_per_node_id):
        filename_per_node_id[self.__DEFAULT_DROPDOWN_VALUE] = 'All documents'
        return core.Dropdown(
            id='dropdown-documents',
            value=self.__DEFAULT_DROPDOWN_VALUE,
            clearable=False,
            options=[
                {'label': name, 'value': id}
                for id, name in filename_per_node_id.items()
            ]
        )
