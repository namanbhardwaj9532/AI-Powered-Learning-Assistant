import { Link } from "react-router-dom";
import "../static/Index.css";

function Index() {
    return (
        <div className="index-page">
            <div className="hero-card">
                <h1>AI Learning Assistant</h1>

                <p>
                    Learn smarter with AI-powered assistance, personalized
                    quizzes, notes, and coding support.
                </p>

                <Link className="enter-btn" to="/login">
                    Enter
                </Link>
            </div>
        </div>
    );
}

export default Index;