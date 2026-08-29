import { useState } from "react";
import { useParams } from "react-router-dom";

function Test() {
    const [questions, setQuestions] = useState("");
    const { note_id } = useParams();

    async function quiz(e) {
        e.preventDefault();

        try {
            const response = await fetch(
                `http://localhost:8000/${note_id}/test`,
                {
                    method: "GET",
                    credentials: "include"
                }
            );

            const data = await response.json();

            setQuestions(data.output);
        } catch (error) {
            console.error("Quiz error:", error);
        }
    }

    return (
        <div>
            <h1>QUIZ</h1>

            <button onClick={quiz}>
                Start
            </button>

            <p>{questions}</p>
        </div>
    );
}

export default Test;