import { Link } from "react-router-dom";
import { useState } from "react";

function Registration() {

    const [username,setusername]=useState("")
    const [password,setpassword]=useState("")
    const [result,setresult]=useState("not registered")

    async function formsubmitted(e) {

        e.preventDefault();
        
        const response = await fetch("http://localhost:8000/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username:username,
                password: password
            })
        });

        const data=await response.json();
        setresult(data.message);
    }
    return (
        <div>
            <Link to="/login">login</Link>
            <form onSubmit={formsubmitted}>
                <label>username:</label>
                <input placeholder="enter username"
                value={username}
                onChange={(e)=>setusername(e.target.value)}
                ></input>
                <br></br>
                <br></br>
                <label>password:</label>
                <input type="password" placeholder="enter password"
                value={password}
                onChange={(e)=>setpassword(e.target.value)}
                ></input>
                <br></br>
                <br></br>
                <button type="submit">submit</button>
            </form>
            <label>{result}</label>
        </div>
    );
}

export default Registration;