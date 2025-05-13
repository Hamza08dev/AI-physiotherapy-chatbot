import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="home-container">
      <h1>Welcome to PhysioAI</h1>
      <p>Your AI-powered physiotherapy assistant for personalized workout plans and rehabilitation exercises.</p>
      <div className="home-buttons">
        <Link to="/signup" className="btn">Get Started</Link>
        <Link to="/chat" className="btn">Chat Now</Link>
      </div>
    </div>
  );
}

export default Home;
