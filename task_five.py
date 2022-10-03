import dash_cytoscape as cyto
import networkx as nx
from networkx.readwrite import json_graph
from dash import Dash, dcc, html, Input, Output


app = Dash(__name__)


def get_networkx_graph(n: int = 100, m: int = 200) -> list[dict, ...]:
    graph = nx.gnm_random_graph(n, m)
    graph_elements = json_graph.adjacency_data(graph)

    elements = []
    for node in graph_elements['nodes']:
        elements.append({'data': {'id': str(node['id']), 'label': str(node['id'])}})

    for adjacency in tuple(nx.generate_adjlist(graph)):
        nodes_link = tuple(str(el) for el in adjacency.split())
        base_node = nodes_link[0]
        if len(nodes_link) > 1:
            for node in nodes_link[1:]:
                elements.append({'data': {'source': base_node, 'target': node}})

    return elements


default_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#fa5633',
            'label': 'data(label)'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'line-color': '#bd533c'
        }
    },
    {
        'selector': 'label',
        'style': {
            'content': 'data(label)',
            'color': '#e6e6e8',
        }
    }
]

div_style = {
    'width': '100%',
    'height': '100%',
    'backgroundColor': '#26292e',
    'margin-top': '-8px',
    'margin-left': '-8px',
    'margin-right': '-8px',
    'margin-bottom': '-8px',

}

dropdown_style = {
    "font-family": "sans-serif",
    "font-size": "large",
    'background-color': '#fa5633',
    'color': '#bd533c',
    'border': 'none',
}

app.layout = html.Div([
    dcc.Dropdown(
        [
            'random', 'circle', 'concentric', 'grid', 'breadthfirst',
            'cose',
        ], 'cose', id='graph-dropdown', style=dropdown_style,
    ),

    cyto.Cytoscape(
        id='cytoscape',
        elements=get_networkx_graph(),
        layout={'name': 'random', 'animate': True, 'id': 'cytoscape-layout'},
        stylesheet=default_stylesheet,
        style={
            'width': '100%',
            'height': '1000px',
        },
    )
],
    style=div_style,
    id='cytoscape-layout',
)


@app.callback(
    Output('cytoscape', 'layout'),
    Input('graph-dropdown', 'value')
)
def update_output(value):
    return {'name': value, 'animate': True, 'id': 'cytoscape-layout'}


if __name__ == '__main__':
    app.run_server(debug=True)
