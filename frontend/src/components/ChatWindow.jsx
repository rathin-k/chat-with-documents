function ChatWindow() {
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

        <div className="max-w-3xl mx-auto">

          <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-200">
            <p className="text-gray-700">
              Upload a document and ask questions about it.
            </p>
          </div>

        </div>

      </div>

      {/* Input */}
      <div className="bg-white border-t border-gray-200 p-4">

        <div className="max-w-3xl mx-auto flex gap-3">

          <input
            type="text"
            placeholder="Ask a question..."
            className="flex-1 border border-gray-300 rounded-lg px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
          />

          <button className="bg-blue-600 text-white px-6 rounded-lg font-medium hover:bg-blue-700">
            Send
          </button>

        </div>

      </div>

    </main>
  )
}

export default ChatWindow