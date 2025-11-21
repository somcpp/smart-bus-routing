# visualize.py
# Functions to draw the graph and highlight the chosen route. Returns PNG bytes.
import io
import base64
import matplotlib.pyplot as plt
import networkx as nx

def draw_graph_highlight_path(G: nx.Graph, path: list, figsize=(6,4)) -> bytes:
    plt.figure(figsize=figsize)
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx_nodes(G, pos, node_size=500)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, width=1)

    # highlight path edges
    if path and len(path) > 1:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=3)

    # edge labels (weights)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.axis('off')
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return buf.read()

def png_bytes_to_base64_inline(png_bytes: bytes) -> str:
    return 'data:image/png;base64,' + base64.b64encode(png_bytes).decode('ascii')
