class StylesheetProvider:

    def get_stylesheet(self, layout):
        return [
            {
                'selector': 'node',
                'style': {
                    'width': self.get_node_width(layout),
                    'height': self.get_node_width(layout),
                    'color': 'black',
                    'label': 'data(label)',
                    'font-size': self.get_font_size(layout),
                    'text-outline-width': self.get_text_outline_size(layout),
                    'text-outline-color': 'white',
                    'background-color': 'gray'
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'font-size': self.get_font_size(layout),
                    'label': 'data(weight)',
                    'line-color': 'data(rgb)',
                    'line-style': 'solid',
                    'width': self.get_edge_width(layout),
                    'text-outline-width': self.get_text_outline_size(layout),
                    'text-outline-color': 'white',
                    'text-opacity': '1.0'
                }
            }
        ]

    def __is_concentric(self, layout):
        return layout == 'concentric'

    def __is_cose(self, layout):
        return layout == 'cose'

    def __is_circle(self, layout):
        return layout == 'circle'

    def get_node_width(self, layout):
        if self.__is_concentric(layout):
            return '7px'
        if self.__is_cose(layout):
            return '10px'
        if self.__is_circle(layout):
            return "45px"
        return '30px'

    def get_font_size(self, layout):
        if self.__is_concentric(layout):
            return '2px'
        if self.__is_cose(layout):
            return '4px'
        if self.__is_circle(layout):
            return "16px"
        return '12px'

    def get_edge_width(self, layout):
        if self.__is_concentric(layout):
            return '0.5px'
        if self.__is_cose(layout):
            return '1.2px'
        if self.__is_circle(layout):
            return "7px"
        return '5px'

    def get_text_outline_size(self, layout):
        if self.__is_concentric(layout):
            return '5px'
        if self.__is_cose(layout):
            return '1px'
        if self.__is_circle(layout):
            return "3px"
        return '2px'
