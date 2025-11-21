# visualize.py
# Functions to draw the graph and highlight the chosen route. Returns PNG bytes.
import io
import base64
import matplotlib
# Use non-interactive backend to avoid opening a GUI (prevents tkinter/main-thread errors when running Flask)
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

def draw_graph_highlight_path(G: nx.Graph, path: list, figsize=(8,6)) -> bytes:
    plt.figure(figsize=figsize)

    # Extract coordinates from G (from positions in sample_graph.json)
    coords = {}
    for n in G.nodes():
        lat = G.nodes[n]['pos'][0]
        lng = G.nodes[n]['pos'][1]
        coords[n] = (lng, lat)  # matplotlib uses (x=lng, y=lat)

    # Plot edges
    for u, v in G.edges():
        x1, y1 = coords[u]
        x2, y2 = coords[v]
        plt.plot([x1, x2], [y1, y2], color="#777", linewidth=1.2)

        # Draw edge weight in midpoint
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        weight = G[u][v]['weight']
        plt.text(mid_x, mid_y, str(weight), fontsize=8, color="black")

    # Highlight path edges
    if path and len(path) > 1:
        for a, b in zip(path, path[1:]):
            x1, y1 = coords[a]
            x2, y2 = coords[b]
            plt.plot([x1, x2], [y1, y2], color="#007BFF", linewidth=3)

    # Plot nodes
    for n, (x, y) in coords.items():
        plt.scatter(x, y, s=300, color="#1D74F5")
        plt.text(x, y, n, fontsize=12, color="white", ha='center', va='center')

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Bus Network Graph (Geo-Scaled)")
    plt.grid(True, linestyle='--', alpha=0.3)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return buf.read()


def png_bytes_to_base64_inline(png_bytes: bytes) -> str:
    return 'data:image/png;base64,' + base64.b64encode(png_bytes).decode('ascii')
