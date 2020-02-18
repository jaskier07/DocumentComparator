from dash.dependencies import Output, Input

from drawing.StylesheetProvider import StylesheetProvider

import dash_html_components as html


class CallbackProvider:
    stylesheetProvider = StylesheetProvider()
    default_dropdown_value = None
    nodes_per_id: dict

    def __init__(self, default_dropdown_value, nodes_per_id) -> None:
        self.default_dropdown_value = default_dropdown_value
        self.nodes_per_id = nodes_per_id

    def define_callbacks(self, app):
        @app.callback(Output('container', 'layout'), [Input('dropdown-view', 'value')])
        def update_layout(layout):
            return {
                'name': layout,
                'animate': True
            }

        @app.callback(Output('container', 'tapNodeData'), [Input('dropdown-documents', 'value')])
        def update_graph_on_document_selection(selected_document):
            if selected_document is None or selected_document == self.default_dropdown_value:
                return None
            return self.nodes_per_id.get(int(selected_document))['data']

        @app.callback([Output('slider-value', 'children'),
                       Output('container', 'stylesheet'),
                       Output('pdf-viewer', 'children')],
                      [Input('slider-similarity', 'value'),
                       Input('container', 'elements'),
                       Input('container', 'layout'),
                       Input('container', 'tapNodeData')])
        def update_slider(value, all_elements, layout, selected_node):
            new_styles = []
            hidden_edge_ids = []
            nodes = set()

            hidden_edge_ids_per_node_id = dict()

            if selected_node is not None:
                node_id = str(selected_node['id'])
                if node_id is not None and all_elements:
                    for e in all_elements:
                        element = e.get('data')
                        edge_id = element.get('id')
                        id_condition_edge = 'edge[id = "{}"]'.format(edge_id)
                        if element.get('source') == node_id or element.get('target') == node_id:
                            new_styles.append(
                                {
                                    'selector': id_condition_edge,
                                    'style': {
                                        'width': self.stylesheetProvider.get_edge_width(layout['name']),
                                        'hidden': 'false'
                                    }
                                }
                            )
                        elif element.get('source') is not None:
                            hidden_edge_ids.append(edge_id)
                            if element.get('source') not in hidden_edge_ids_per_node_id:
                                hidden_edge_ids_per_node_id[element.get('source')] = set()
                            hidden_edge_ids_per_node_id[element.get('source')].add(edge_id)

                            if element.get('target') not in hidden_edge_ids_per_node_id:
                                hidden_edge_ids_per_node_id[element.get('target')] = set()
                            hidden_edge_ids_per_node_id[element.get('target')].add(edge_id)

                            new_styles.append(
                                {
                                    'selector': id_condition_edge,
                                    'style': {
                                        'hidden': 'true',
                                        'width': '0'
                                    }
                                }
                            )
                        else:
                            id_condition_node = 'node[id = "{}"]'.format(element.get('id'))
                            if element.get('id') == node_id:
                                color = '#42a1f5'
                            else:
                                color = 'gray'
                            new_styles.append({
                                'selector': id_condition_node,
                                'style': {
                                    'background-color': color
                                }
                            })

            for e in all_elements:
                element = e.get('data')
                if element.get('source') is not None:
                    edge_id = element.get('id')
                    id_condition_edge = 'edge[id = "{}"]'.format(edge_id)
                    if element.get("id") not in hidden_edge_ids and element.get('weight') > value:
                        width = self.stylesheetProvider.get_edge_width(layout['name'])
                    else:
                        width = 0
                        hidden_edge_ids.append(edge_id)

                        if element.get('source') not in hidden_edge_ids_per_node_id:
                            hidden_edge_ids_per_node_id[element.get('source')] = set()
                        hidden_edge_ids_per_node_id[element.get('source')].add(edge_id)

                        if element.get('target') not in hidden_edge_ids_per_node_id:
                            hidden_edge_ids_per_node_id[element.get('target')] = set()
                        hidden_edge_ids_per_node_id[element.get('target')].add(edge_id)
                    new_styles.append(
                        {
                            'selector': id_condition_edge,
                            'style': {
                                'width': width
                            }
                        }
                    )
                else:
                    nodes.add(element.get('id'))

            sp = StylesheetProvider()
            for node_id in nodes:
                id_condition_node = 'node[id = "{}"]'.format(node_id)
                if node_id in hidden_edge_ids_per_node_id and len(hidden_edge_ids_per_node_id[node_id]) == len(
                        nodes) - 1:
                    new_styles.append({
                        'selector': id_condition_node,
                        'style': {
                            'width': 0,
                            'height': 0,
                            'color': 'black',
                            'label': '',
                        }
                    })
                else:
                    new_styles.append({
                        'selector': id_condition_node,
                        'style': {
                            'width': sp.get_node_width(layout),
                            'height': sp.get_node_width(layout),
                            'color': 'black',
                            'label': 'data(label)',
                        }
                    })

            children = []
            if selected_node is not None:
                children = html.Iframe(id='pdf-viewer-frame', src='assets/' + selected_node['label'])

            return value, self.stylesheetProvider.get_stylesheet(layout['name']) + new_styles, children
