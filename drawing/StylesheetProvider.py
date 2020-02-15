class StylesheetProvider:
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
                'text-outline-color': 'white',
                'background-color': 'gray'
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
        }
    ]

    def get_stylesheet(self):
        return self.__stylesheet