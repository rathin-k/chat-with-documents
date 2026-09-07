import { useState } from "react"
import api from "../api/axios"

function ChatWindow() {
  const [question, setQuestion] = useState("")
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const [conversationId, setConversationId] = useState(null)

  const handleSend = async (e) => {
    e.preventDefault()

    if (!question.trim() || loading) {
      return
    }

    const currentQuestion = question

    setQuestion("")
    setError("")
    setLoading(true)

    // Show user's message immediately
    setMessages((previousMessages) => [
      ...previousMessages,
      {
        role: "user",
        content: currentQuestion
      }
    ])

    try {

      const response = await api.post(
        "/chat/",
        {
          question: currentQuestion,
          conversation_id: conversationId
        }
      )

      const data = response.data

      // Save conversation ID returned by backend
      if (!conversationId) {
        setConversationId(data.conversation_id)
      }

      // Add assistant response
      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources
        }
      ])

    } catch (error) {

      console.error(
        "Chat request failed:",
        error
      )

      if (error.response) {
        setError(
          error.response.data.detail ||
          "Failed to get answer"
        )
      } else {
        setError("Cannot connect to server")
      }

    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="flex-1 h-screen flex flex-col bg-gray-50">

      {/* Header */}

      <div className="h-16 bg-white border-b border-gray-200 flex items-center px-6">
        <h1 className="text-lg font-semibold text-gray-800">
          Chat with Documents
        </h1>
      </div>


      {/* Messages */}

      <div className="flex-1 overflow-y-auto p-6">

        <div className="max-w-3xl mx-auto space-y-4">

          {messages.length === 0 && (
            <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-200">
              <p className="text-gray-700">
                Upload a document and ask questions about it.
              </p>
            </div>
          )}


          {messages.map((message, index) => (

            <div
              key={index}
              className={
                message.role === "user"
                  ? "flex justify-end"
                  : "flex justify-start"
              }
            >

              <div
                className={
                  message.role === "user"
                    ? "max-w-xl bg-blue-600 text-white rounded-xl px-4 py-3"
                    : "max-w-xl bg-white text-gray-800 rounded-xl px-4 py-3 border border-gray-200"
                }
              >

                <p className="whitespace-pre-wrap">
                  {message.content}
                </p>


                {/* Sources */}

                {message.sources &&
                  message.sources.length > 0 && (
                   <div className="mt-4 pt-3 border-t border-gray-200">
                    <p className="text-xs font-semibold text-gray-500 mb-2">
                      Sources
                   </p>

                   {[
                    ...new Map(
                     message.sources.map((source) => [
                       source.metadata.document_id,
                       source
                     ])
                    ).values()
                  ].map((source, sourceIndex) => (
                    <div
                      key={sourceIndex}
                      className="text-xs text-gray-500 mb-2"
                    >
                     📄 {source.metadata.filename}
                    </div>
                  ))}
              </div>
             )}

              </div>

            </div>

          ))}


          {/* Loading */}

          {loading && (

            <div className="flex justify-start">

              <div className="bg-white border border-gray-200 rounded-xl px-4 py-3">
                <p className="text-gray-500">
                  Thinking...
                </p>
              </div>

            </div>

          )}

          {error && (
            <p className="text-sm text-red-600">
              {error}
            </p>
          )}

        </div>

      </div>


      {/* Input */}

      <div className="bg-white border-t border-gray-200 p-4">

        <form
          onSubmit={handleSend}
          className="max-w-3xl mx-auto flex gap-3"
        >

          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question..."
            disabled={loading}
            className="flex-1 border border-gray-300 rounded-lg px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
          />

          <button
            type="submit"
            disabled={loading || !question.trim()}
            className="bg-blue-600 text-white px-6 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? "..." : "Send"}
          </button>

        </form>

      </div>

    </main>
  )
}

export default ChatWindow