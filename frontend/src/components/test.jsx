import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "../static/Test.css";

function Test() {
    const [questions, setQuestions] = useState([]);
    const { note_id } = useParams();
    const [answers, setanswers] = useState({});
    const [submitted, setsubmitted] = useState(false);
    const [result, setresult] = useState(null);

    useEffect(() => {
        quiz();
    }, [note_id]);

    async function quiz() {
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

    async function submitquiz() {
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
        <div className="test-page">

            <div className="test-container">

                <header className="test-header">
                    <h1>Quiz</h1>
                    <p>Test your understanding of the notes.</p>
                </header>

                {!submitted && (
                    <div className="questions">

                        {questions.map((item) => (
                            <div className="question-card" key={item.id}>

                                <h3>
                                    <span>{item.id}</span>
                                    {item.question}
                                </h3>

                                <div className="options">

                                    {item.options.map((option, optionIndex) => (
                                        <label
                                            className="option"
                                            key={optionIndex}
                                        >
                                            <input
                                                type="radio"
                                                name={`question-${item.id}`}
                                                onChange={() =>
                                                    handleanswers(
                                                        item.id,
                                                        option
                                                    )
                                                }
                                            />

                                            <span>{option}</span>
                                        </label>
                                    ))}

                                </div>

                            </div>
                        ))}

                        {questions.length > 0 && (
                            <button
                                className="submit-btn"
                                onClick={submitquiz}
                            >
                                Submit Quiz
                            </button>
                        )}

                    </div>
                )}

                {submitted && result && (
                    <div className="result-card">

                        <div className="result-score">
                            {result.score}
                            <span>/{result.total}</span>
                        </div>

                        <h2>Quiz Completed</h2>

                        <p>
                            You answered {result.score} out of{" "}
                            {result.total} questions correctly.
                        </p>

                        <button
                            className="submit-btn"
                            onClick={() => {
                                setsubmitted(false);
                                setresult(null);
                            }}
                        >
                            Review Answers
                        </button>

                    </div>
                )}

            </div>

        </div>
    );
}

export default Test;