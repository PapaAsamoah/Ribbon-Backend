import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const API = "http://localhost:8000/ranked";

export default function Home() {
  const [subreddit, setSubreddit] = useState("wallstreetbets");
  const [data, setData] = useState([]);
  const [sortKey, setSortKey] = useState("score");

  async function load() {
    const res = await fetch(`${API}?subreddit=${subreddit}`);
    const json = await res.json();
    setData(json.results || []);
  }

  useEffect(() => {
    load();
  }, []);

  function sortBy(key) {
    setSortKey(key);
    setData([...data].sort((a, b) => (b[key] ?? 0) - (a[key] ?? 0)));
  }

  return (
    <main className="main-section">
      <div className="card-box">
        <form onSubmit={(e) => { e.preventDefault(); load(); }}>
          <input
            value={subreddit}
            onChange={(e) => setSubreddit(e.target.value)}
            placeholder="subreddit"
          />
          <button>Load</button>
        </form>

        <table className="data-table">
          <thead>
            <tr>
              <th>#</th>
              <th className="table-header" onClick={() => sortBy("symbol")}>
                Ticker
              </th>
              <th className="table-header" onClick={() => sortBy("score")}>
                Score
              </th>
            </tr>
          </thead>

          <tbody>
            {data.map((row, i) => (
              <tr key={row.symbol}>
                <td>{i + 1}</td>
                <td>
                  <Link to={`/ticker/${row.symbol}`}>{row.symbol}</Link>
                </td>
                <td>{row.score?.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
