import "../static/Navbar.css";

import { Link, useNavigate } from "react-router-dom";

function Navbar() {
    const navigate = useNavigate();

    async function logout() {
        await fetch("http://localhost:8000/logout", {
            method: "POST",
            credentials: "include",
        });

        navigate("/login");
    }

    return (
        <nav className="navbar">

            <Link to="/" className="navbar-logo">
                NinjaAI
            </Link>

            <div className="navbar-links">
                <Link to="/main">Home</Link>

                <Link to="/dashboard">
                    Dashboard
                </Link>

                <Link to="/notes">
                    My Notes
                </Link>

                <Link to="/chatbot">
                    Chatbot
                </Link>

                <Link to="/test">
                    Test
                </Link>
            </div>

            <button
                className="navbar-logout"
                onClick={logout}
            >
                Logout
            </button>

        </nav>
    );
}

export default Navbar;