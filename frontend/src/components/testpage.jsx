import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "./navbar";

function Testpage() {

    const [notes, setnotes] = useState([])

    const navigate = useNavigate()
    useEffect(() => {
        async function getNotes() {
            const response = await fetch("http://localhost:8000/notes", {
                credentials: "include"
            });

            if (response.status === 401) {
                navigate("/login");
                return;
            }

            const data = await response.json();
            setnotes(data);
        }

        getNotes();
    }, [navigate]);

    return (
        <div>
            <Navbar />
            {notes.length === 0 ? (
                <div className="empty-notes">
                    <p>No notes yet.</p>
                    <span>Upload your first note above.</span>
                </div>
            ) : (
                <div className="notes-grid">

                    {notes.map((note) => (

                        <div
                            className="note"
                            key={note._id}
                            onClick={() =>
                                navigate(`/contest/${note._id}`)
                            }
                        >

                            <div className="note-icon">
                                PDF
                            </div>

                            <h3>{note.title}</h3>



                        </div>

                    ))}

                </div>
            )}
        </div>
    );
}

export default Testpage;