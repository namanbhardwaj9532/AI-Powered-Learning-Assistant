import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../static/Notes.css";

function Notes() {
    const [title, setTitle] = useState("");
    const [content, setContent] = useState("");
    const [notes, setNotes] = useState([]);

    const navigate = useNavigate();

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
            setNotes(data);
        }

        getNotes();
    }, [navigate]);

    async function addNote(e) {
        e.preventDefault();

        const response = await fetch("http://localhost:8000/notes", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: title,
                content: content
            })
        });

        if (response.status === 401) {
            navigate("/login");
            return;
        }

        const notesResponse = await fetch("http://localhost:8000/notes", {
            credentials: "include"
        });

        const updatedNotes = await notesResponse.json();

        setNotes(updatedNotes);
        setTitle("");
        setContent("");
    }

    return (
        <div className="notes-page">

            <h1>My Notes</h1>

            <form className="note-form" onSubmit={addNote}>

                <label>Title</label>
                <input
                    type="text"
                    placeholder="Enter note title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                />

                <label>Content</label>
                <textarea
                    placeholder="Write your note..."
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                />


                <button type="submit">
                    Add Note
                </button>

            </form>

            <div className="notes-list">

                <h2>Your Notes</h2>

                {notes.length === 0 ? (
                    <p>No notes yet.</p>
                ) : (
                    notes.map((note) => (
                        <div className="note" key={note._id}>
                            <h3>{note.title}</h3>
                            <p>{note.content}</p>
                        </div>
                    ))
                )}

            </div>

        </div>
    );
}

export default Notes;