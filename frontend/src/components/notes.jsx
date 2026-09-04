import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../static/Notes.css";
import Navbar from "./navbar"
import UserFlashcards from "./all_flashcards";

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

        const formdata = new FormData();
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
        setFile(null);
    }

    return (
        <div>
            <Navbar />
            <div className="notes-page">

                <div className="notes-container">
                    <UserFlashcards />
                    <h1>My Notes</h1>
                    <p className="subtitle">
                        Upload and manage your study notes
                    </p>

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

                        <label>PDF File</label>

                        <input
                            type="file"
                            accept=".pdf"
                            onChange={(e) => setFile(e.target.files[0])}
                        />

                        {file && (
                            <p className="selected-file">
                                Selected: {file.name}
                            </p>
                        )}

                        <button type="submit">
                            Add Note
                        </button>

                    </form>


                    <div className="notes-list">

                        <div className="notes-list-header">
                            <h2>Your Notes</h2>
                            <span>{notes.length} notes</span>
                        </div>

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
                                            navigate(`/file/${note._id}`)
                                        }
                                    >

                                        <div className="note-icon">
                                            PDF
                                        </div>

                                        <h3>{note.title}</h3>

                                        <p>
                                            {note.content ||
                                                "No description available."}
                                        </p>

                                        <a
                                            href={`http://localhost:8000/uploads/${note.filesavedname}`}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            onClick={(e) =>
                                                e.stopPropagation()
                                            }
                                        >
                                            {note.filename}
                                        </a>

                                    </div>

                                ))}

                            </div>
                        )}

                    </div>

                </div>

            </div>
        </div> 
    );
}

export default Notes;