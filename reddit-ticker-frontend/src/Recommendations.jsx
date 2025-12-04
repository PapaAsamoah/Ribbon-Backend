import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export default function Recommendations() {
  const [data, setData] = useState([]);

  useEffect(() => {
    async function load() {
      const res = await fetch("http://localhost:8000/ranked");
      const json = await res.json();
      const sorted = (json.results || [])
        .sort((a, b) => b.score - a.score)
        .slice(0, 10);
      setData(sorted);
    }
    load();
  }, []);

  return (
    <main className="main-section">
      <div className="card-box">
        <h2>Top Recommendations</h2>
        <ol>
          {data.map((t) => (
            <li key={t.symbol}>
              <Link to={`/ticker/${t.symbol}`}>{t.symbol}</Link> –{" "}
              {t.score.toFixed(2)}
            </li>
          ))}
        </ol>
      </div>
    </main>
  );
}
