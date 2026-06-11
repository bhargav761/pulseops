import { useEffect, useState } from "react";

function App() {

  const [metrics, setMetrics] = useState({
    cpu_usage: "0%",
    memory_usage: "0%",
    requests: 0
  });

  useEffect(() => {

    fetch("http://127.0.0.1:8000/metrics")
      .then((response) => response.json())
      .then((data) => setMetrics(data));

  }, []);

  return (
    <div className="min-h-screen bg-slate-900 text-white p-6">

      <h1 className="text-4xl font-bold mb-8">
        PulseOps Dashboard
      </h1>

      <div className="grid grid-cols-3 gap-6">

        <div className="bg-slate-800 p-6 rounded-xl shadow-lg">
          <h2 className="text-xl font-semibold">CPU Usage</h2>
          <p className="text-3xl mt-4 text-green-400">
            {metrics.cpu_usage}
          </p>
        </div>

        <div className="bg-slate-800 p-6 rounded-xl shadow-lg">
          <h2 className="text-xl font-semibold">Memory Usage</h2>
          <p className="text-3xl mt-4 text-yellow-400">
            {metrics.memory_usage}
          </p>
        </div>

        <div className="bg-slate-800 p-6 rounded-xl shadow-lg">
          <h2 className="text-xl font-semibold">Requests</h2>
          <p className="text-3xl mt-4 text-blue-400">
            {metrics.requests}
          </p>
        </div>

      </div>

    </div>
  );
}

export default App;