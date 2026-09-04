import { useState, useEffect } from "react";
import "../static/Flashcards.css";

function UserFlashcards() {
    const [flashcards, setFlashcards] = useState([]);
    const [flipped, setFlipped] = useState(false);
    const [currentIndex, setCurrentIndex] = useState(0);

    useEffect(() => {
        showflashcards();
    }, []);

    async function showflashcards() {
        try {
            const response = await fetch(
                "http://localhost:8000/flashcards",
                {
                    method: "GET",
                    credentials: "include"
                }
            );

            const data = await response.json();

            setFlashcards(data.flashcards);
            setCurrentIndex(0);
            setFlipped(false);

        } catch (error) {
            console.error("Flashcards error:", error);
        }
    }


    function flipCard() {
        setFlipped(prev => !prev);
    }

    function nextCard() {
        if (currentIndex < flashcards.length - 1) {
            setCurrentIndex(prev => prev + 1);
            setFlipped(false);
        }
    }

    function previousCard() {
        if (currentIndex > 0) {
            setCurrentIndex(prev => prev - 1);
            setFlipped(false);
        }
    }

    if (flashcards.length === 0) {
        return (
            <div className="flashcards-page">
                <h1>Flashcards</h1>
                <p className="flashcards-subtitle">
                    No flashcards available.
                </p>
            </div>
        );
    }

    const flashcard = flashcards[currentIndex];

    return (
        <div className="flashcards-page">

            <div className="flashcards-wrapper">

                <button
                    className="flashcard-arrow"
                    onClick={previousCard}
                    disabled={currentIndex === 0}
                >
                    &#10094;
                </button>


                <div
                    className={`flashcard-container ${
                        flipped ? "flipped" : ""
                    }`}
                    onClick={flipCard}
                >

                    <div className="flashcard">

                        <div className="flashcard-side flashcard-front">

                            <span className="card-label">
                                QUESTION
                            </span>

                            <h2>
                                {flashcard.question}
                            </h2>

                            <p className="flip-hint">
                                Click to reveal answer
                            </p>

                        </div>


                        <div className="flashcard-side flashcard-back">

                            <span className="card-label">
                                ANSWER
                            </span>

                            <p>
                                {flashcard.answer}
                            </p>

                            <p className="flip-hint">
                                Click to see question
                            </p>

                        </div>

                    </div>

                </div>



                <button
                    className="flashcard-arrow"
                    onClick={nextCard}
                    disabled={currentIndex === flashcards.length - 1}
                >
                    &#10095;
                </button>

            </div>


            <p className="flashcard-counter">
                {currentIndex + 1} / {flashcards.length}
            </p>

        </div>
    );
}

export default UserFlashcards;