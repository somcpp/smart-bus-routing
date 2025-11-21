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
    for n in data.get('nodes', []):
        G.add_node(n)
    for u, v, w in data.get('edges', []):
        G.add_edge(u, v, weight=w)
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

    return {
        'old_total_wait_minutes': old_total,
        'new_total_wait_minutes': new_total,
        'absolute_reduction_minutes': reduction,
        'percent_reduction': pct,
        'old_route_time': old_time,
        'optimized_route_time': new_time,
        'old_interval': old_interval,
        'new_interval': new_interval
    }

# A tiny global used by estimate_wait_reduction; loaded from app when graph created
G_global = None

def set_global_graph(G: nx.Graph):
    global G_global
    G_global = G
