import { useState } from "react"
import "../static/chatbot.css"

function Chatbot() {
    const [prompt, setprompt] = useState("")
    const [output, setoutput] = useState("")

    async function getresponse(e) {
        e.preventDefault();
        setoutput("working...")
        const response = await fetch("http://localhost:8000/chatbot", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "prompt": prompt
            })
        })
        const data = await response.json()
        setoutput(data.output)
    }

    return (
        <div>
            <form className="chat-form" onSubmit={getresponse}>

                <div className="chat-header">
                    <h2>AI Assistant</h2>
                    <p>Ask me anything</p>
                </div>

                <div className="chat-output">
                    <textarea
                        placeholder="AI response will appear here..."
                        value={output}
                        readOnly
                    />
                </div>

                <div className="chat-input">
                    <input
                        type="text"
                        placeholder="Write your prompt..."
                        value={prompt}
                        onChange={(e) => setprompt(e.target.value)}
                    />

                    <button type="submit">
                        Send
                    </button>
                </div>

            </form>
        </div>
    )
}
export default Chatbot