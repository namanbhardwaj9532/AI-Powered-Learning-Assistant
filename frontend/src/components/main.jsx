import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";

function Main() {
    const [loading, setLoading] = useState(true);
    const [name,setname]=useState("");
    const [authenticated, setAuthenticated] = useState(false);
    const navigate=useNavigate();

    useEffect(() => {
        async function checkAuth() {
            const response = await fetch("http://localhost:8000/main", {
                credentials: "include"
            });

            if (response.status === 401) {
                navigate("/login");
                return;
            }

            const data=await response.json();
            setname(data.uid);

            setAuthenticated(true);
            setLoading(false);

        }

        checkAuth();
    }, []);

    if (loading) {
        return <div>Checking authentication...</div>;
    }

    if (!authenticated) {
        return null;
    }

    async function logout(){
        const response=await fetch("http://localhost:8000/logout",{
            method:"POST",
            credentials:"include",
        })
        navigate("/login");
    }

    return (
        <div>
            <button onClick={logout}>logout</button>
            <label>{name}</label>
        </div>
    );
}

export default Main;