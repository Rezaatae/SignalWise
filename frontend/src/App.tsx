import { useEffect, useState } from "react";
import { healthCheck } from "./services/api";

function App() {
  const [status, setStatus] = useState("");

  useEffect(() => {
    healthCheck().then((data) => {
      setStatus(data.status);
    });
  }, []);

  return (
    <div>
      <h1>Full Stack App</h1>
      <p>Backend status: {status}</p>
    </div>
  );
}

export default App;