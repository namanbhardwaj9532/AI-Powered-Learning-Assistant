import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "../static/Flashcards.css"

function Flashcards() {

    const [keywords, setkeywords] = useState([]);

    const { note_id } = useParams();

    useEffect(() => {
        showflashcards();
    }, [note_id]);

    async function showflashcards() {

        const response = await fetch(
            `http://localhost:8000/${note_id}/flashcards`,
            {
                method: "GET",
                credentials: "include"
            }
        );

        const data = await response.json();

        setkeywords(data.keywords);
    }

    return (
        <div className="flashcards">
            {keywords.map((keyword, index) => (
                <span key={index}>
                    {keyword}
                </span>
            ))}
        </div>
    );
}

export default Flashcards;