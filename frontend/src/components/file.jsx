import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import "../static/file.css"

function File() {
    const [title, setTitle] = useState("");
    const [filename, setFilename] = useState("");
    const [notetext, setnotetext] = useState("")
    const [tol, settol] = useState(0)

    const { note_id } = useParams();

    useEffect(() => {
        async function getNote() {
            const response = await fetch(
                `http://localhost:8000/file/${note_id}`,
                {
                    credentials: "include"
                }
            );

            const data = await response.json();

            setTitle(data.title);
            setFilename(data.filename);
            setnotetext(data.text);
            settol(data.tolpages);
        }

        getNote();
    }, [note_id]);

    return (
        <div className="file-container">
            <div className="file-header">
                <h1>{title}</h1>
                <span className="file-name">{filename}</span>
                <br></br>
                <span className="file-name">total pages:{tol}</span>
            </div>

            <div className="file-content">
                <p className="note-text">{notetext}</p>
            </div>
        </div>
    );
}

export default File;