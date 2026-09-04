import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "../static/Flashcards.css";

function Flashcards() {
    const [flashcards, setFlashcards] = useState([]);
    const [flipped, setFlipped] = useState(false);
    const [currentIndex, setCurrentIndex] = useState(0);

    const { note_id } = useParams();

    useEffect(() => {
        showflashcards();
    }, [note_id]);

    async function showflashcards() {
        try {
            const response = await fetch(
                `http://localhost:8000/${note_id}/flashcards`,
                {
                    method: "GET",
                    credentials: "include"
                }
            );

            const data = await response.json();

            setFlashcards(data.flashcards);
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

            <h1>Flashcards</h1>

            <p className="flashcards-subtitle">
                Click the card to reveal the answer
            </p>

            <div className="flashcards-wrapper">

                {/* Left Arrow */}
                <button
                    className="flashcard-arrow"
                    onClick={previousCard}
                    disabled={currentIndex === 0}
                >
                    &#10094;
                </button>


                {/* Card */}
                <div
                    className={`flashcard-container ${
                        flipped ? "flipped" : ""
                    }`}
                    onClick={flipCard}
                >

                    <div className="flashcard">

                        {/* Front */}
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


                        {/* Back */}
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


                {/* Right Arrow */}
                <button
                    className="flashcard-arrow"
                    onClick={nextCard}
                    disabled={currentIndex === flashcards.length - 1}
                >
                    &#10095;
                </button>

            </div>


            {/* Counter */}
            <p className="flashcard-counter">
                {currentIndex + 1} / {flashcards.length}
            </p>

        </div>
    );
}

export default Flashcards;