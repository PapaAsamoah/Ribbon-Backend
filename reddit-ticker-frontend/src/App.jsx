import { Routes, Route, Link } from "react-router-dom";
import Home from "./home.jsx";
import Recommendations from "./Recommendations.jsx";
import Ticker from "./ticker.jsx";

export default function App() {
  return (
    <>
      <header className="header">
        <div className="logo-row">
          <img src="/ribbon_logo.png" className="logo-image" />
          <span className="brand-text">Ribbon</span>
        </div>
        <h1 className="main-title">Reddit Ticker Sentiments</h1>
        <p className="subtitle-text">
          Future of Retail Investor Favored Stock Discovery
        </p>

        <nav style={{ marginTop: "1rem" }}>
          <Link to="/" style={{ marginRight: "1rem" }}>Home</Link>
          <Link to="/recommendations">Recommendations</Link>
        </nav>
      </header>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/recommendations" element={<Recommendations />} />
        <Route path="/ticker/:symbol" element={<Ticker />} />
      </Routes>

      <div className="quote-area">
        <img src="/dima.png" className="quote-image" />
        <p className="quote-text">
          "This has got me out of my gambling debts,<br />
          due to the amazing stock finds!"
        </p>
      </div>

      <footer className="footer-box">
        <span>Cohort VI Product</span>
      </footer>
    </>
  );
}
