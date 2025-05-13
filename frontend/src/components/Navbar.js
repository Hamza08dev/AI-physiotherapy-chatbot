import { useContext, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import { Link } from "react-router-dom";
import "../App.css"; // Ensure correct CSS import
import logo from "../assets/logo.png"; // Ensure the logo exists

const Navbar = () => {
  const authContext = useContext(AuthContext);
  const user = authContext?.user || null;
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        <img src={logo} alt="Logo" className="navbar-logo" />
        AI Physiotherapy
      </Link>

      {/* Hamburger Menu */}
      <div className="menu-icon" onClick={() => setMenuOpen(!menuOpen)}>
        ☰
      </div>

      {/* Navigation Links */}
      <div className={`nav-links ${menuOpen ? "show" : ""}`}>
        <Link to="/" onClick={() => setMenuOpen(false)}>Home</Link>
        {user ? (
          <>
            <Link to="/chat" onClick={() => setMenuOpen(false)}>Chat</Link>
            <button onClick={() => { authContext.logout(); setMenuOpen(false); }}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" onClick={() => setMenuOpen(false)}>Login</Link>
            <Link to="/signup" onClick={() => setMenuOpen(false)}>Signup</Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
