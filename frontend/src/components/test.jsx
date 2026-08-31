import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

function Test() {
    const [questions, setQuestions] = useState([]);
    const { note_id } = useParams();
    const [answers, setanswers] = useState({})
    const [submitted, setsubmitted] = useState(false)
    const [result, setresult] = useState(null)

    useEffect(() => {
        quiz()
    }, [note_id]);

    async function quiz(e) {
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

    function handleanswers(questionid, answer) {
        setanswers(prev => ({
            ...prev,
            [questionid]: answer
        }));
    }

    async function submitquiz(e) {
        try {
            const response = await fetch(
                `http://localhost:8000/${note_id}/test/submit`,
                {
                    method: "POST",
                    credentials: "include",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        answers: answers
                    })
                }
            );

            const data = await response.json();

            setresult(data);
            setsubmitted(true);

        } catch (error) {
            console.error("Submit error:", error);
        }
    }

    return (
        <div>
            <h1>QUIZ</h1>

            <div>
                {questions.map((item) => (
                    <div key={item.id}>
                        <h3>
                            {item.id}. {item.question}
                        </h3>

                        {item.options.map((option, optionIndex) => (
                            <div key={optionIndex}>
                                <label>
                                    <input
                                        type="radio"
                                        name={`question-${item.id}`}
                                        onChange={() => handleanswers(item.id, option)}
                                    />
                                    {option}
                                </label>
                            </div>
                        ))}
                    </div>
                ))}
                <br></br>
                <button onClick={submitquiz}>submit</button>
            </div>
            {submitted && result && (
                <div>
                    <h2>
                        Score: {result.score}/{result.total}
                    </h2>
                </div>
            )}
        </div>
    );
}

export default Test;