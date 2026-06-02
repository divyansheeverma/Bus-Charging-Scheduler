<h1 align="center">🚌 Bus Charging Scheduler</h1>

<p align="center">
Simulation-based EV bus charging scheduler for intercity electric buses.
</p>

---

<h2>📌 Overview</h2>

<p>
This project simulates electric bus charging schedules between Bengaluru and Kochi.
The system handles:
</p>

<ul>
  <li>Battery range constraints</li>
  <li>Charging station contention</li>
  <li>Charging wait times</li>
  <li>Multiple buses sharing chargers</li>
  <li>Forward and reverse traffic</li>
  <li>Dynamic charging timelines</li>
</ul>

---

<h2>🚀 Features</h2>

<ul>
  <li>Multi-bus EV scheduling simulation</li>
  <li>Shared charger resource management</li>
  <li>Queue and wait-time simulation</li>
  <li>Forward and reverse route support</li>
  <li>Per-bus charging timelines</li>
  <li>Per-station charging schedules</li>
  <li>Multiple configurable scenarios</li>
  <li>Interactive Streamlit UI</li>
</ul>

---

<h2>🛠️ Tech Stack</h2>

<ul>
  <li>Python</li>
  <li>Streamlit</li>
  <li>Pandas</li>
</ul>

---

<h2>📂 Project Structure</h2>

<pre>
bus-charging-scheduler/
│
├── app.py
├── test.py
├── requirements.txt
│
├── scenarios/
│   ├── scenario_1.json
│   ├── scenario_2.json
│   ├── scenario_3.json
│   ├── scenario_4.json
│   └── scenario_5.json
│
└── engine/
    ├── __init__.py
    ├── scheduler.py
    ├── simulator.py
    ├── scorer.py
    ├── station_manager.py
    └── utils.py
</pre>

---

<h2>⚙️ Core Components</h2>

<table>
  <tr>
    <th>Component</th>
    <th>Responsibility</th>
  </tr>

  <tr>
    <td>scheduler.py</td>
    <td>Charging plan generation and selection</td>
  </tr>

  <tr>
    <td>simulator.py</td>
    <td>Travel and charging simulation</td>
  </tr>

  <tr>
    <td>station_manager.py</td>
    <td>Shared charger state management</td>
  </tr>

  <tr>
    <td>scorer.py</td>
    <td>Schedule scoring and evaluation</td>
  </tr>

  <tr>
    <td>app.py</td>
    <td>Streamlit frontend UI</td>
  </tr>
</table>

---

<h2>🧠 Scheduling Strategy</h2>

<p>
The scheduler uses a sequential greedy optimization strategy.
</p>

<ol>
  <li>Generate valid charging plans</li>
  <li>Simulate each candidate plan</li>
  <li>Evaluate wait times and delays</li>
  <li>Select lowest-cost plan</li>
  <li>Commit charger reservations</li>
</ol>

<p>
This creates realistic charger contention across the network.
</p>

---

<h2>⏱️ Time Representation</h2>

<p>
The simulation internally represents time as:
</p>

<pre>
minutes since midnight
</pre>

<p>
This avoids:
</p>

<ul>
  <li>datetime rollover bugs</li>
  <li>timezone complexity</li>
  <li>overnight simulation issues</li>
</ul>

---

<h2>🧪 Scenarios</h2>

<table>
  <tr>
    <th>Scenario</th>
    <th>Description</th>
  </tr>

  <tr>
    <td>Scenario 1</td>
    <td>Even spacing between departures</td>
  </tr>

  <tr>
    <td>Scenario 2</td>
    <td>Dense departures causing higher contention</td>
  </tr>

  <tr>
    <td>Scenario 3</td>
    <td>Direction imbalance between routes</td>
  </tr>

  <tr>
    <td>Scenario 4</td>
    <td>Operator-priority scheduling</td>
  </tr>

  <tr>
    <td>Scenario 5</td>
    <td>Peak congestion stress test</td>
  </tr>
</table>

---

<h2>▶️ Running the Project</h2>

<h3>Install dependencies</h3>

<pre>
pip install -r requirements.txt
</pre>

<h3>Run backend simulation</h3>

<pre>
python test.py
</pre>

<h3>Run Streamlit app</h3>

<pre>
streamlit run app.py
</pre>

---

<h2>📊 Outputs</h2>

<p>The application displays:</p>

<ul>
  <li>Per-bus charging plans</li>
  <li>Charging timelines</li>
  <li>Wait times</li>
  <li>Final arrival times</li>
  <li>Per-station charging schedules</li>
</ul>

---

<h2>🔮 Future Improvements</h2>

<ul>
  <li>Smarter global optimization</li>
  <li>Dynamic charger capacities</li>
  <li>Battery SOC simulation</li>
  <li>Real-time traffic integration</li>
  <li>OR-tools / Genetic algorithms</li>
  <li>Multi-route support</li>
</ul>

---

<h2>👨‍💻 Author </h2>

<p>
<b> Divyanshee Verma</b>
</p>
