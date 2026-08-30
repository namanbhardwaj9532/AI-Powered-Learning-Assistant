import { useState } from "react";
import { useParams } from "react-router-dom";

function Test() {
    const [questions, setQuestions] = useState([]);
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

            setQuestions(data.questions);
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

            <div>
                {questions.map((item, index) => (
                    <div key={index}>
                        <h3>
                            {index + 1}. {item.question}
                        </h3>

                        {item.options.map((option, optionIndex) => (
                            <div key={optionIndex}>
                                <label>
                                    <input
                                        type="radio"
                                        name={`question-${index}`}
                                    />
                                    {option}
                                </label>
                            </div>
                        ))}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Test;