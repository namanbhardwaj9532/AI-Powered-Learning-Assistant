import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import "../static/Notes.css";

function Notes() {
    const [title, setTitle] = useState("");
    const [content, setContent] = useState("");
    const [notes, setNotes] = useState([]);
    const [file, setFile] = useState(null);

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
        const formdata = new FormData()
        formdata.append("title", title);
        formdata.append("content", content);
        if (file) {
            formdata.append("file", file);
        }
        const response = await fetch("http://localhost:8000/notes", {
            method: "POST",
            credentials: "include",
            body: formdata
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

                <label>Description</label>
                <textarea
                    placeholder="Add a short description..."
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                />
                <input
                    type="file"
                    onChange={(e) => setFile(e.target.files[0])}
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
                        <div className="note" key={note._id} onClick={()=>navigate(`/file/${note._id}`)}>
                            <h3>{note.title}</h3>
                            <p>{note.content}</p>
                            <a
                                href={`http://localhost:8000/uploads/${note.filesavedname}`}
                                target="_blank"
                                rel="noopener noreferrer"
                                onClick={(e) => e.stopPropagation()}
                            >
                                {note.filename}
                            </a>
                        </div>
                    ))
                )}

            </div>

        </div>
    );
}

export default Notes;