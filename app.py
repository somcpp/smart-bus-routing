# app.py
from flask import Flask, render_template, request
import json
import routing
from visualize import draw_graph_highlight_path, png_bytes_to_base64_inline

app = Flask(__name__)

# load data and build graph
DATA_PATH = 'data/sample_graph.json'
DATA = routing.load_graph_from_file(DATA_PATH)
G = routing.build_graph(DATA)
routing.set_global_graph(G)

@app.route('/')
def index():
    nodes = list(G.nodes())
    return render_template('index.html', nodes=nodes)

@app.route('/route', methods=['POST'])
def route():
    src = request.form['source']
    dst = request.form['target']

    # find optimized shortest path
    try:
        path, length = routing.shortest_path_and_length(G, src, dst)
    except Exception as e:
        return f"Error finding path: {e}", 400

    # compute wait time change vs old_route (from data)
    old_route = DATA.get('old_route')
    interval = DATA.get('bus_interval_minutes', 30)
    demand = DATA.get('demand', {})

    stats = routing.estimate_wait_reduction(old_route, path, interval, demand)

    # generate visualization (png fallback for old UI)
    png = draw_graph_highlight_path(G, path)
    img_inline = png_bytes_to_base64_inline(png)

    # compute node positions for interactive map
    # Prefer explicit positions if provided in the data file (sample_graph.json includes lat/lng per node)
    data_positions = DATA.get('positions') if DATA else None
    positions = {}
    if data_positions:
        # Use provided positions (ensure floats)
        for n in G.nodes():
            p = data_positions.get(n)
            if p:
                positions[n] = [float(p[0]), float(p[1])]
        # if some nodes missing positions, compute fallback for them
        missing = [n for n in G.nodes() if n not in positions]
        if missing:
            computed = routing.get_node_positions(G, center_lat=28.6692, center_lng=77.4538, scale=0.03, seed=42)
            for n in missing:
                positions[n] = [float(computed[n][0]), float(computed[n][1])]
    else:
        # compute positions around Ghaziabad if none provided
        computed = routing.get_node_positions(G, center_lat=28.6692, center_lng=77.4538, scale=0.03, seed=42)
        positions = {n: [float(v[0]), float(v[1])] for n, v in computed.items()}

    # prepare map JSON for frontend
    # positions: {node: [lat, lng]}, edges list for drawing optional
    map_json = {
        'positions': {n: [positions[n][0], positions[n][1]] for n in positions},
        'path': path,
        'edges': [[u, v] for u, v in G.edges()]
    }

    # pretty path for display (A → B → C)
    pretty_path = " \u2192 ".join(path)

    return render_template('index.html', nodes=list(G.nodes()), result={
        'path': path,
        'path_pretty': pretty_path,
        'time': round(length, 2),
        'stats': stats,
        'img': img_inline,
        'map_json': map_json
    })

if __name__ == '__main__':
    app.run(debug=True)
