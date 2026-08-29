import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import "../static/file.css";

function File() {
    const [title, setTitle] = useState("");
    const [filename, setFilename] = useState("");
    const [notetext, setNoteText] = useState([]);
    const [tol, setTol] = useState(0);


    const [prompt, setPrompt] = useState("");
    const [output, setOutput] = useState("");

    const { note_id } = useParams();

    const navigate=useNavigate();
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
            setNoteText(data.text);
            setTol(data.tolpages);
        }

        getNote();
    }, [note_id]);

    async function  test(){
        navigate(`/test/${note_id}`)
    }
    async function getResponse(e) {
        e.preventDefault();

        if (!prompt.trim()) {
            return;
        }

        setOutput("Working...");

        const response = await fetch(
            `http://localhost:8000/${note_id}/chatbot`,
            {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    prompt: prompt
                })
            }
        );

        if (!response.ok) {
            setOutput("Something went wrong.");
            return;
        }

        const data = await response.json();

        setOutput(data.output);
    }

    return (
        <div className="file-page">

            <div className="file-container">

                <div className="file-header">
                    <h1>{title}</h1>

                    <span className="file-name">
                        {filename}
                    </span>

                    <br />

                    <span className="file-name">
                        Total pages: {tol}
                    </span>
                </div>
                <div>
                    <button class="test-btn" onClick={test}>test</button>
                </div>
                <div className="file-content">
                    <p className="note-text">
                        {notetext}
                    </p>
                </div>

            </div>



            <div className="chat-panel">

                <div className="chat-header">
                    <h2>AI Assistant</h2>

                    <p>
                        Ask questions about your document
                    </p>
                </div>



                <div className="chat-output">

                    {output ? (
                        <p>{output}</p>
                    ) : (
                        <p className="chat-placeholder">
                            Ask something about your document...
                        </p>
                    )}

                </div>



                <form
                    className="chat-input"
                    onSubmit={getResponse}
                >

                    <input
                        type="text"
                        placeholder="Ask something..."
                        value={prompt}
                        onChange={(e) =>
                            setPrompt(e.target.value)
                        }
                    />

                    <button type="submit">
                        Send
                    </button>

                </form>

            </div>

        </div>
    );
}

export default File;