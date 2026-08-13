import { Link } from "react-router-dom";
import { useState } from "react";
import "../static/Registration.css";

function Registration() {
    const [username, setusername] = useState("");
    const [password, setpassword] = useState("");
    const [result, setresult] = useState("");

    async function formsubmitted(e) {
        e.preventDefault();

        setresult("Creating account...");

        const response = await fetch("http://localhost:8000/register", {
            method: "POST",
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
    }

    return (
        <div className="registration-page">

            <div className="registration-card">

                <h1>Create Account</h1>
                <p className="subtitle">
                    Register for your account
                </p>

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
                        Register
                    </button>

                </form>

                {result && (
                    <p className="result">
                        {result}
                    </p>
                )}

                <p className="login-text">
                    Already have an account?{" "}
                    <Link to="/login">Login</Link>
                </p>

            </div>

        </div>
    );
}

export default Registration;