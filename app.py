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

    # generate visualization
    png = draw_graph_highlight_path(G, path)
    img_inline = png_bytes_to_base64_inline(png)

    return render_template('index.html', nodes=list(G.nodes()), result={
        'path': path,
        'time': length,
        'stats': stats,
        'img': img_inline
    })

if __name__ == '__main__':
    app.run(debug=True)
