from numbers import Number

from dash.dependencies import Output, Input

from drawing.StylesheetProvider import StylesheetProvider


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

        @app.callback(Output('dropdown-documents', 'value'), [Input('button-select-all', 'n_clicks')])
        def f(id):
            return '-1'

        @app.callback([Output('slider-value', 'children'),
                       Output('container', 'stylesheet')],
                      [Input('slider-similarity', 'value'),
                       Input('container', 'elements'),
                       Input('container', 'layout'),
                       Input('container', 'tapNodeData')])
        def update_slider(value, all_elements, layout, selected_node):
            new_styles = []
            hidden_edges = []

            if selected_node is not None:
                node_id = str(selected_node['id'])
                if node_id is not None and all_elements:
                    for e in all_elements:
                        element = e.get('data')
                        id_condition_edge = 'edge[id = "{}"]'.format(element.get('id'))
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
                            new_styles.append(
                                {
                                    'selector': id_condition_edge,
                                    'style': {
                                        'hidden': 'true',
                                        'width': '0'
                                    }
                                }
                            )
                        elif element.get('id') == node_id:
                            id_condition_node = 'node[id = "{}"]'.format(element.get('id'))
                            new_styles.append({
                                'selector': id_condition_node,
                                'style': {
                                    'background-color': '#42a1f5'
                                }
                            })
                        else:
                            id_condition_node = 'node[id = "{}"]'.format(element.get('id'))
                            new_styles.append({
                                'selector': id_condition_node,
                                'style': {
                                    'background-color': 'gray'
                                }
                            })

                return value, self.stylesheetProvider.get_stylesheet(layout['name']) + new_styles
            else:
                for e in all_elements:
                    element = e.get('data')
                    id_condition_edge = 'edge[id = "{}"]'.format(element.get('id'))
                    if element.get('source') is not None:
                        if element.get('weight') > value:
                            new_styles.append(
                                {
                                    'selector': id_condition_edge,
                                    'style': {
                                        'width': self.stylesheetProvider.get_edge_width(layout['name']),
                                    }
                                }
                            )
                        else:
                            hidden_edges.append(element)
                            new_styles.append(
                                {
                                    'selector': id_condition_edge,
                                    'style': {
                                        'width': 0
                                    }
                                }
                            )

                    # for e in all_elements:
                    #     element = e.get('data')
                    #     id_condition_node = 'node[id = "{}"]'.format(element.get('id'))
                    #     if element.get('source') is None:


                    # elif element.get('id') == node_id:
                    #     id_condition_node = 'node[id = "{}"]'.format(element.get('id'))
                    #     new_styles.append({
                    #         'selector': id_condition_node,
                    #         'style': {
                    #             'background-color': '#42a1f5'
                    #         }
                    #     })
                    # else:
                    #     id_condition_node = 'node[id = "{}"]'.format(element.get('id'))
                    #     new_styles.append({
                    #         'selector': id_condition_node,
                    #         'style': {
                    #             'background-color': 'gray'
                    #         }
                    #     })

            return value, self.stylesheetProvider.get_stylesheet(layout['name']) + new_styles
