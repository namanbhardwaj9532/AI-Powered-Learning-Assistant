import { useState } from "react"
import "../static/chatbot.css"
import Navbar from "./navbar"

function Chatbot() {
    const [prompt, setPrompt] = useState("")
    const [messages, setMessages] = useState([])

    async function getresponse(e) {
        e.preventDefault()

        if (!prompt.trim()) return

        const userMessage = prompt
        setPrompt("")

        // Add user message
        setMessages((prev) => [
            ...prev,
            {
                sender: "user",
                text: userMessage
            }
        ])

        // Loading message
        setMessages((prev) => [
            ...prev,
            {
                sender: "ai",
                text: "Thinking..."
            }
        ])

        try {
            const response = await fetch("http://localhost:8000/chatbot", {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    prompt: userMessage
                })
            })

            const data = await response.json()

            // Replace "Thinking..." with actual response
            setMessages((prev) => [
                ...prev.slice(0, -1),
                {
                    sender: "ai",
                    text: data.output
                }
            ])
        } catch (error) {
            setMessages((prev) => [
                ...prev.slice(0, -1),
                {
                    sender: "ai",
                    text: "Something went wrong. Please try again."
                }
            ])
        }
    }

    return (
        <div>
            <Navbar />
            <div className="chatbot-container">
                <div className="chatbot">

                    {/* Header */}
                    <div className="chatbot-header">
                        <div className="ai-icon">
                            AI
                        </div>

                        <div>
                            <h2>AI Assistant</h2>
                            <span>Online</span>
                        </div>
                    </div>

                    {/* Messages */}
                    <div className="chat-messages">

                        {messages.length === 0 && (
                            <div className="welcome-message">
                                <div className="welcome-icon">AI</div>
                                <h3>How can I help you?</h3>
                                <p>
                                    Ask me anything and I'll try to help.
                                </p>
                            </div>
                        )}

                        {messages.map((message, index) => (
                            <div
                                key={index}
                                className={`message-row ${message.sender}`}
                            >
                                {message.sender === "ai" && (
                                    <div className="message-icon">
                                        AI
                                    </div>
                                )}

                                <div className="message">
                                    {message.text}
                                </div>
                            </div>
                        ))}

                    </div>

                    {/* Input */}
                    <form
                        className="chat-input-container"
                        onSubmit={getresponse}
                    >
                        <input
                            type="text"
                            placeholder="Message AI Assistant..."
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                        />

                        <button type="submit">
                            ↑
                        </button>
                    </form>

                </div>

            </div>
        </div>
    )
}

export default Chatbot