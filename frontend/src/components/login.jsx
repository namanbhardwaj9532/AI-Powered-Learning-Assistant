import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import "../static/login.css"

function Login() {
    const navigate = useNavigate();

    const [username, setusername] = useState("");
    const [password, setpassword] = useState("");
    const [result, setresult] = useState("");

    async function formsubmitted(e) {
        e.preventDefault();

        setresult("working....");

        const response = await fetch("http://localhost:8000/login", {
            method: "POST",
            credentials:"include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        setresult(data.message);

        if (data.message === "login successful") {
            navigate("/main");
        }
    }

    return (
        <div className="login-page">

            <div className="login-card">

                <h1>Welcome Back</h1>
                <p className="subtitle">Login to your account</p>

                <form onSubmit={formsubmitted}>

                    <label>Username</label>
                    <input
                        type="text"
                        placeholder="Enter username"
                        value={username}
                        onChange={(e) => setusername(e.target.value)}
                    />

                    <label>Password</label>
                    <input
                        type="password"
                        placeholder="Enter password"
                        value={password}
                        onChange={(e) => setpassword(e.target.value)}
                    />

                    <button type="submit">
                        Login
                    </button>

                </form>

                {result && (
                    <p className="result">
                        {result}
                    </p>
                )}

                <p className="register-text">
                    New user? <Link to="/registration">Create an account</Link>
                </p>

            </div>

        </div>
    );
}

export default Login;