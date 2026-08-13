import { Link } from "react-router-dom";

function Login() {

    async function formsubmitted(e) {
        e.preventDefault();


    }

    return (
        <div>
            <h1>Login</h1>

            <form onSubmit={formsubmitted}>
                <label>username:</label>
                <input placeholder="enter username"
                    value={username}
                    onChange={(e) => setusername(e.target.value)}
                ></input>
                <br></br>
                <br></br>
                <label>password:</label>
                <input type="password" placeholder="enter password"
                    value={password}
                    onChange={(e) => setpassword(e.target.value)}
                ></input>
                <br></br>
                <br></br>
                <button type="submit">submit</button>
            </form>
            <p>
                New user? <Link to="/registration">Register</Link>
            </p>
        </div>
    );
}

export default Login;