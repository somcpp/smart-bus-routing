# 🚍 Smart Bus Routing System

An intelligent route‑optimization and passenger wait‑time reduction system built using **Graph Theory (Dijkstra’s Algorithm)**, **Flask**, **Leaflet Maps**, and **geo‑based visualizations** for the **Delhi NCR + Ghaziabad** region.

This project simulates a real smart‑city bus routing system by modeling city stops as nodes, roads as weighted edges, and using shortest‑path algorithms to optimize routes and reduce total passenger wait time.

---

## ⭐ Features

### 🔹 1. Smart Route Optimization (Dijkstra)

* Computes the **fastest path** between two stops.
* Uses real geographic coordinates for accuracy.
* Weights edges by estimated travel time based on haversine distance.

### 🔹 2. Interactive Leaflet Map

* Real‑world coordinates plotted on a map.
* Shows bus stops, edges, and the optimized route.
* Smooth visualization of the path.

### 🔹 3. Geo‑Scaled Static Visualization

* A clear, readable matplotlib visualization.
* Uses actual latitude/longitude instead of random layouts.

### 🔹 4. Passenger Wait‑Time Analytics

* Calculates **old vs new wait time**.
* Uses passenger demand across stops.
* Computes efficiency gain and time saved for all commuters.

### 🔹 5. Clean Dashboard UI

* Modern styling with route badges.
* Cards showing stats and time reduction.
* Explanation box for transparency.

---

## 🧠 How It Works (Concept)

### 🟦 Graph Representation

The city is represented as a **weighted graph**:

* **Nodes:** Bus stops (A, B, C, …)
* **Edges:** Roads connecting stops
* **Weights:** Travel time in minutes

### 🟦 Why Dijkstra's Algorithm?

Dijkstra’s Algorithm is used because:

* All weights are **positive** (travel times)
* It finds the **minimum‑cost path** from a source node to all other nodes
* Perfect for **shortest route planning** in transportation

### 🟩 Dijkstra in simple terms:

Imagine you’re at bus stop **A** and want to reach **L**.
You look at all possible paths but always choose the **cheapest next step**.
You keep expanding the cheapest options until you reach your destination with the lowest total cost.

It works like:

1. Start from source with distance 0
2. Mark all neighbors with tentative distances
3. Pick the node with smallest distance
4. Update distances of its neighbors
5. Repeat until all nodes are visited

### 🟪 Why Dijkstra fits Smart Bus Routing

* Road travel time cannot be negative → satisfies Dijkstra constraints
* Optimizes actual bus movement
* Helps reduce passenger waiting times
* Produces fast results (millisecond computations)

---

## 📊 Wait‑Time Calculation

Each bus has a **base interval** (e.g., 30 minutes). Passengers wait on average:

```
average_wait = interval / 2
```

When a route becomes faster → buses return sooner → interval becomes smaller:

```
new_interval = old_interval * (new_route_time / old_route_time)
```

### Total passenger wait time:

```
total_wait = Σ (passenger_demand × average_wait)
```

This gives realistic city‑scale wait‑time reduction.

---

## 🗺️ Dataset (Delhi NCR + Ghaziabad)

The project uses 12 real stops:

* Ghaziabad
* Indirapuram
* Vaishali
* Noida Sec‑62
* Noida Sec‑18
* Anand Vihar
* Dilshad Garden
* Loni
* East Ghaziabad
* Modinagar Road
* Kavi Nagar
* Shahdara

Each stop has:

* Latitude / longitude
* Passenger demand
* Connections to nearby stops

---

## 🧩 Project Structure

```
smart-bus-routing/
├── app.py
├── routing.py
├── visualize.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── data/
│   └── sample_graph.json
└── requirements.txt
```

---

## ▶️ How to Run the Project

### 1️⃣ Create a virtual environment

```
python -m venv venv
venv\Scripts\activate   # Windows
# OR
source venv/bin/activate # Mac/Linux
```

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 3️⃣ Run the Flask server

```
python app.py
```

### 4️⃣ Open in browser

Go to:

```
http://127.0.0.1:5000
```

---

## 🏙️ Real‑World Use Case

This system can be adapted by:

* City transport authorities (DTC, UPSRTC)
* University bus management
* Private shuttle service providers
* Route planning apps

It improves:

* Passenger satisfaction
* Fuel usage
* Bus scheduling
* Traffic load distribution

---

## 🔮 Future Improvements

* Real GPS data integration
* Live traffic‑based edge weights
* Machine learning prediction for peak hours
* Route animation on map
* Multi‑bus fleet optimization
* School/college shuttle personalization

---

## 📜 License

This project is open for educational and research use.

---

## ✨ Credits

Developed with ❤️ as a smart‑city analytics project integrating:

* Python
* NetworkX
* Flask
* Leaflet JS
* Matplotlib
* Delhi NCR geo‑mapping
