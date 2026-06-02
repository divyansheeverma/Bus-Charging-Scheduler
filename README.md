# Bus-Charging-Scheduler<h1 align="center">🏗️ System Architecture</h1>

---

<h2>📌 High-Level Architecture</h2>

<pre>
Scenario JSON
      ↓
Scheduler
      ↓
Plan Generation
      ↓
Simulation Engine
      ↓
Shared Station Manager
      ↓
Scoring Engine
      ↓
Final Bus Timelines + Station Schedules
      ↓
Streamlit UI
</pre>

---

<h2>🎯 Architecture Goals</h2>

<ul>
  <li>Simulate realistic EV charging behavior</li>
  <li>Handle charger contention</li>
  <li>Support multiple buses simultaneously</li>
  <li>Keep components modular and extensible</li>
  <li>Separate scheduling, simulation, and UI logic</li>
</ul>

---

<h2>🧩 Core Components</h2>

<table>
  <tr>
    <th>Component</th>
    <th>Responsibility</th>
  </tr>

  <tr>
    <td>scheduler.py</td>
    <td>Charging plan selection</td>
  </tr>

  <tr>
    <td>simulator.py</td>
    <td>Travel and charging simulation</td>
  </tr>

  <tr>
    <td>station_manager.py</td>
    <td>Shared charger state tracking</td>
  </tr>

  <tr>
    <td>scorer.py</td>
    <td>Plan scoring logic</td>
  </tr>

  <tr>
    <td>app.py</td>
    <td>Visualization/UI layer</td>
  </tr>
</table>

---

<h2>🔄 Scheduling Flow</h2>

<ol>
  <li>Load scenario JSON</li>
  <li>Generate valid charging plans</li>
  <li>Clone station state</li>
  <li>Simulate candidate plans</li>
  <li>Compute scores</li>
  <li>Select best plan</li>
  <li>Commit charger reservations</li>
</ol>

---

<h2>🚏 Shared Resource Scheduling</h2>

<p>
Charging stations are treated as shared resources.
</p>

<p>
A global <code>StationManager</code> maintains:
</p>

<ul>
  <li>Charger occupancy</li>
  <li>Station schedules</li>
  <li>Next available charging time</li>
</ul>

<p>
This creates realistic charger contention between buses.
</p>

---

<h2>🕒 Time Model</h2>

<p>
The simulation internally uses:
</p>

<pre>
integer minutes
</pre>

<p>
Example:
</p>

<pre>
19:00 → 1140
</pre>

<p>
Advantages:
</p>

<ul>
  <li>Simpler arithmetic</li>
  <li>No timezone complexity</li>
  <li>No datetime rollover bugs</li>
  <li>Reliable overnight simulation</li>
</ul>

---

<h2>⚡ Simulation Flow</h2>

<pre>
Travel
→ Arrive at station
→ Check charger availability
→ Wait if occupied
→ Charge
→ Continue journey
</pre>

---

<h2>📈 Scoring Model</h2>

<p>
Plans are evaluated using:
</p>

<pre>
score =
    wait_penalty
    +
    stop_penalty
</pre>

<p>
Where:
</p>

<ul>
  <li><b>wait_penalty</b> = charger waiting time</li>
  <li><b>stop_penalty</b> = number of charging stops</li>
</ul>

<p>
Lower scores are preferred.
</p>

---

<h2>🧪 Simulation Strategy</h2>

<p>
The system uses:
</p>

<pre>
Greedy Sequential Optimization
</pre>

<p>
Buses are processed in departure order.
Earlier buses reserve chargers first, influencing later buses.
</p>

---

<h2>📺 Streamlit UI</h2>

<p>
The frontend is intentionally lightweight.
</p>

<p>
Streamlit is used for:
</p>

<ul>
  <li>Scenario selection</li>
  <li>Displaying bus schedules</li>
  <li>Showing station charging timelines</li>
</ul>

<p>
All scheduling logic remains inside the backend engine.
</p>

---

<h2>📦 Scalability</h2>

<p>
The architecture can be extended to support:
</p>

<ul>
  <li>Additional routes</li>
  <li>Larger fleets</li>
  <li>Dynamic charger counts</li>
  <li>Battery SOC tracking</li>
  <li>Advanced optimization algorithms</li>
  <li>Real-time telemetry</li>
</ul>

---

<h2>⚖️ Tradeoffs</h2>

<p>
The current implementation prioritizes:
</p>

<ul>
  <li>Simplicity</li>
  <li>Explainability</li>
  <li>Modularity</li>
  <li>Maintainability</li>
</ul>

<p>
Instead of attempting expensive global optimization.
</p>

---

<h2>✅ Conclusion</h2>

<p>
The system successfully models:
</p>

<ul>
  <li>EV charging constraints</li>
  <li>Shared charger contention</li>
  <li>Scheduling conflicts</li>
  <li>Queue buildup</li>
  <li>Wait propagation</li>
  <li>Multi-bus coordination</li>
</ul>

<p>
while maintaining a clean and extensible architecture.
</p>
