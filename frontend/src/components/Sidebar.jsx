import { useEffect, useRef, useState } from "react"
import api from "../api/axios"

function Sidebar() {
  const fileInputRef = useRef(null)

  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState("")
  const [documents, setDocuments] = useState([])

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

  useEffect(() => {
    fetchDocuments()
  }, [])

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

  return (
    <aside className="w-72 h-screen bg-white border-r border-gray-200 flex flex-col">

      {/* Header */}

      <div className="p-6 border-b border-gray-200">

        <h2 className="text-xl font-bold text-gray-800">
          Documents
        </h2>

        {/* Hidden file input */}

        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          className="hidden"
        />

        {/* Upload button */}

        <button
          onClick={handleUploadClick}
          disabled={uploading}
          className="mt-4 w-full bg-blue-600 text-white py-2.5 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50"
        >
          {uploading ? "Uploading..." : "+ Upload PDF"}
        </button>

        {/* Error */}

        {error && (
          <p className="text-sm text-red-600 mt-3">
            {error}
          </p>
        )}

      </div>

      {/* Document list */}

      <div className="flex-1 overflow-y-auto p-4">

        {documents.map((document) => (
          <div
           key={document.document_id}
           className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-100 cursor-pointer"
          >
            <span>📄</span>

            <span className="text-sm text-gray-700 truncate">
              {document.filename}
           </span>
      </div>
   ))}

      </div>

    </aside>
  )
}

export default Sidebar