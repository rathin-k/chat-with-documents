import { useEffect, useRef, useState } from "react"
import api from "../api/axios"

function Sidebar({ onSelectConversation,onNewChat,refreshKey,selectedConversationId }) {
  const fileInputRef = useRef(null)

  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState("")
  const [documents, setDocuments] = useState([])
  const [conversations, setConversations] = useState([])

  const fetchDocuments = async () => {
    try {
      const response = await api.get("/documents/")

      setDocuments(response.data)

    } catch (error) {
      console.error(
        "Failed to fetch documents:",
        error
      )

      setError("Failed to load documents")
    }
  }

  const fetchConversations = async () => {
   try {
     const response = await api.get(
       "/chat/conversations"
     )

     setConversations(response.data)

    } catch (error) {
      console.error(
       "Failed to fetch conversations:",
      error
    )
   }
  }

  useEffect(() => {
   fetchDocuments()
   fetchConversations()
  }, [refreshKey])

  const handleUploadClick = () => {
    fileInputRef.current.click()
  }

  const handleFileChange = async (e) => {
    const file = e.target.files[0]

    if (!file) {
      return
    }

    setError("")
    setUploading(true)

    try {
      const formData = new FormData()

      formData.append("file", file)

      const response = await api.post(
        "/upload/",
        formData
      )

      console.log(
        "Upload successful:",
        response.data
      )

    } catch (error) {
      console.error(error)

      if (error.response) {
        setError(
          error.response.data.detail ||
          "Upload failed"
        )
      } else {
        setError("Cannot connect to server")
      }

    } finally {
      setUploading(false)

      // Allow selecting the same file again
      e.target.value = ""
    }
  }
  
  const handleDelete = async (documentId) => {
  try {
    setError("")

    await api.delete(
      `/documents/${documentId}`
    )

    fetchDocuments()

  } catch (error) {
    console.error(
      "Delete failed:",
      error
    )

    if (error.response) {
      setError(
        error.response.data.detail ||
        "Failed to delete document"
      )
    } else {
      setError("Cannot connect to server")
    }
  }
}

  return (
    <aside className="w-72 shrink-0 h-screen bg-white border-r border-gray-200 flex flex-col">

      {/* Header */}

      <div className="p-5 border-b border-gray-200">

  <h2 className="text-xl font-bold text-gray-800">
    Documents
  </h2>

  <input
    ref={fileInputRef}
    type="file"
    accept=".pdf"
    onChange={handleFileChange}
    className="hidden"
  />

  <button
    onClick={handleUploadClick}
    disabled={uploading}
    className="mt-4 w-full bg-blue-600 text-white py-2.5 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50"
  >
    {uploading ? "Uploading..." : "+ Upload PDF"}
  </button>

  {error && (
    <p className="text-sm text-red-600 mt-3">
      {error}
    </p>
  )}

</div>

      {/* Document list */}

      <div className="flex-1 overflow-y-auto p-4">

        <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
          Documents
        </h3>

        {/* Documents */}

         {documents.map((document) => (
           <div
             key={document.document_id}
             className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-100 transition-colors"
            >
             <span>📄</span>

             <span className="text-sm text-gray-700 truncate flex-1">
               {document.filename}
             </span>

             <button
               onClick={() => handleDelete(document.document_id)}
               className="text-red-500 hover:text-red-700 text-sm"
             >
               🗑
             </button>
           </div>
          ))}


  {/* Conversations */}

  <div className="mt-6">

    <div className="flex justify-between items-center mb-3"></div>

      <h3 className="text-xs font-semibold text-gray-500 uppercase mb-2 tracking-wide">
        Conversations
      </h3>
    
      <button
        onClick={onNewChat}
        className="w-full mt-3 border border-gray-300 text-gray-700 py-2 rounded-lg font-medium hover:bg-gray-100 transition-colors"
      >
       + New Chat
      </button>
     
    {conversations.map((conversation) => (
      <div
        key={conversation.conversation_id}
        onClick={() =>
          onSelectConversation(
            conversation.conversation_id
          )
        }
        className={`flex items-center gap-3 p-3 rounded-lg cursor-pointer transition-colors ${
          conversation.conversation_id === selectedConversationId
            ? "bg-gray-100"
            : "hover:bg-gray-100"
        }`}
      >
        <span>💬</span>

        <span className="text-sm text-gray-700 truncate">
          {conversation.title}
        </span>
      </div>
    ))}

  </div>

</div>

    </aside>
  )
}

export default Sidebar