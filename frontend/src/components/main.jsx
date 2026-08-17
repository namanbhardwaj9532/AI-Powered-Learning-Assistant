import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../static/Main.css";

function Main() {
    const [loading, setLoading] = useState(true);
    const [name, setname] = useState("");
    const [username, setusername] = useState("");
    const [email, setemail] = useState("");
    const [id, setid] = useState("");
    const [authenticated, setAuthenticated] = useState(false);

    const navigate = useNavigate();

    useEffect(() => {
        async function checkAuth() {
            const response = await fetch("http://localhost:8000/main", {
                credentials: "include"
            });

            if (response.status === 401) {
                navigate("/login");
                return;
            }

            const data = await response.json();

            setname(data.name);
            setid(data.uid);
            setusername(data.username);
            setemail(data.email);

            setAuthenticated(true);
            setLoading(false);
        }

        checkAuth();
    }, [navigate]);

    if (loading) {
        return <div className="loading">Checking authentication...</div>;
    }

    if (!authenticated) {
        return null;
    }

    async function logout() {
        await fetch("http://localhost:8000/logout", {
            method: "POST",
            credentials: "include",
        });

        navigate("/login");
    }

    return (
        <div>
            <div className="dashboard">

                <header className="dashboard-header">
                    <h1>Dashboard</h1>

                    <button className="logout-btn" onClick={logout}>
                        Logout
                    </button>
                </header>

                <div className="profile-card">

                    <div className="profile-title">
                        <div className="avatar">
                            {name.charAt(0).toUpperCase()}
                        </div>

                        <div>
                            <h2>{name}</h2>
                            <p>@{username}</p>
                        </div>
                    </div>

                    <div className="user-details">

                        <div className="detail">
                            <span>Name</span>
                            <strong>{name}</strong>
                        </div>

                        <div className="detail">
                            <span>Username</span>
                            <strong>{username}</strong>
                        </div>

                        <div className="detail">
                            <span>Email</span>
                            <strong>{email}</strong>
                        </div>

                        <div className="detail">
                            <span>User ID</span>
                            <strong>{id}</strong>
                        </div>

                    </div>

                </div>
                <Link to="/notes" className="notes-card">
                    <div className="notes-icon">📝</div>

                    <div>
                        <h2>My Notes</h2>
                    </div>

                    <span className="notes-arrow">→</span>
                </Link>
            </div>
        </div>
    );
}

export default Main;