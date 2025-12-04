import { useParams, Link } from "react-router-dom";
import { useEffect, useState } from "react";

export default function Ticker() {
  const { symbol } = useParams();
  const [ticker, setTicker] = useState(null);

  useEffect(() => {
    async function load() {
      const res = await fetch("http://localhost:8000/ranked");
      const json = await res.json();
      const found = (json.results || []).find(
        (x) => x.symbol.toUpperCase() === symbol.toUpperCase()
      );
      setTicker(found || null);
    }
    load();
  }, [symbol]);

  if (!ticker) return <p>Loading...</p>;

  return (
    <main className="main-section">
      <div className="card-box">
        <h2>{ticker.symbol}</h2>
        <p>Score: {ticker.score.toFixed(2)}</p>

        <h3>Relevant Posts</h3>
        {ticker.posts?.length ? (
          <ul>
            {ticker.posts.slice(0, 10).map((p, i) => (
              <li key={i}>{p.title}</li>
            ))}
          </ul>
        ) : (
          <p>No posts available.</p>
        )}

        <p>
          <Link to="/">Back</Link>
        </p>
      </div>
    </main>
  );
}
