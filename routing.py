# routing.py
# Graph model, Dijkstra (using networkx) and wait-time calculations
import json
import networkx as nx
from typing import List, Tuple, Dict

def load_graph_from_file(path: str) -> Dict:
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def build_graph(data: Dict) -> nx.Graph:
    G = nx.Graph()
    # if nodes include coords in data (optional), we will keep them in node attributes
    for n in data.get('nodes', []):
        G.add_node(n)
    for u, v, w in data.get('edges', []):
        G.add_edge(u, v, weight=w)
    # if data contains positions, attach them to nodes as attributes
    if 'positions' in data:
        for node, pos in data['positions'].items():
            if node in G:
                G.nodes[node]['pos'] = tuple(pos)
    return G

def shortest_path_and_length(G: nx.Graph, source: str, target: str) -> Tuple[List[str], float]:
    path = nx.shortest_path(G, source=source, target=target, weight='weight')
    length = nx.shortest_path_length(G, source=source, target=target, weight='weight')
    return path, float(length)

def route_total_time(G: nx.Graph, route: List[str]) -> float:
    total = 0.0
    for a, b in zip(route, route[1:]):
        total += G[a][b]['weight']
    return total

def estimate_wait_reduction(old_route: List[str], optimized_route: List[str], interval_minutes: float, passenger_demand: Dict[str, int]) -> Dict:
    """
    Estimates total passenger wait time before and after optimization.

    Simple model:
      - Bus interval scales with route time (same number of buses circulate)
      - Average wait per passenger = interval / 2
      - Total wait = sum(demand_at_stop * avg_wait)

    Returns a dict with old_total_wait, new_total_wait and percent_reduction
    """
    # Note: this function requires a graph to compute route times; the app sets G_global
    old_time = route_total_time(G_global, old_route)
    new_time = route_total_time(G_global, optimized_route)

    old_interval = interval_minutes
    # frequency scales inversely to route time
    if old_time == 0:
        new_interval = old_interval
    else:
        new_interval = old_interval * (new_time / old_time)

    def total_wait(interval):
        avg_wait = interval / 2.0
        total = 0
        for stop, demand in passenger_demand.items():
            total += demand * avg_wait
        return total

    old_total = total_wait(old_interval)
    new_total = total_wait(new_interval)
    reduction = (old_total - new_total)
    pct = (reduction / old_total * 100.0) if old_total > 0 else 0.0

    total_passengers = sum(passenger_demand.values())

    return {
        'old_total_wait_minutes': round(old_total, 2),
        'new_total_wait_minutes': round(new_total, 2),
        'absolute_reduction_minutes': round(reduction, 2),
        'percent_reduction': round(pct, 2),
        'old_route_time': round(old_time, 2),
        'optimized_route_time': round(new_time, 2),
        'old_interval': round(old_interval, 2),
        'new_interval': round(new_interval, 2),
        'total_passengers': int(total_passengers),
        'old_avg_wait': round(old_interval/2.0, 2),
        'new_avg_wait': round(new_interval/2.0, 2)
    }

# A tiny global used by estimate_wait_reduction; loaded from app when graph created
G_global = None

def set_global_graph(G: nx.Graph):
    global G_global
    G_global = G

def get_node_positions(G: nx.Graph, center_lat=22.0, center_lng=77.0, scale=0.03, seed=42) -> Dict[str, Tuple[float, float]]:
    """
    Return a dict mapping node -> (lat, lng).
    Priority:
      1. if node has 'pos' attribute (from data), use that (assumed as [lat, lng])
      2. otherwise compute a layout via networkx.spring_layout and map to lat/lng around center coords.

    scale controls the spread (in degrees). Default center is arbitrary (India-ish).
    """
    positions = {}
    # If nodes already have 'pos' attr, use them
    has_any_pos = any('pos' in G.nodes[n] for n in G.nodes())
    if has_any_pos:
        for n in G.nodes():
            p = G.nodes[n].get('pos')
            if p:
                # assume p is (lat, lng) or (y, x) -> keep as (lat, lng)
                positions[n] = (float(p[0]), float(p[1]))
            else:
                positions[n] = (center_lat, center_lng)
        return positions

    # compute spring layout (2D)
    layout = nx.spring_layout(G, seed=seed)
    # layout maps nodes to coordinates in roughly [-1,1]. We'll normalize to lat/lng near center.
    xs = [v[0] for v in layout.values()]
    ys = [v[1] for v in layout.values()]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    # avoid division by zero
    range_x = max_x - min_x if max_x - min_x != 0 else 1.0
    range_y = max_y - min_y if max_y - min_y != 0 else 1.0

    for n, (x, y) in layout.items():
        # normalized in [ -0.5, 0.5 ] to keep nodes close
        nxorm = (x - (min_x + max_x) / 2.0) / range_x
        nyorm = (y - (min_y + max_y) / 2.0) / range_y
        lat = center_lat + nyorm * scale
        lng = center_lng + nxorm * scale
        positions[n] = (float(lat), float(lng))
    return positions
