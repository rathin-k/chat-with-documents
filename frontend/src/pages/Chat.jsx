import { useState } from "react"

import Sidebar from "../components/Sidebar"
import ChatWindow from "../components/ChatWindow"

function Chat() {

  const [selectedConversationId, setSelectedConversationId] = useState(null)

  const [conversationRefreshKey, setConversationRefreshKey] = useState(0)

  const handleNewChat = () => {
    setSelectedConversationId(null)
  }
  
  const handleConversationCreated = (conversationId) => {

    setSelectedConversationId(conversationId)

    setConversationRefreshKey(
      (previous) => previous + 1
    )
  }

  return (
    <div className="h-screen flex">

      <Sidebar
        onSelectConversation={setSelectedConversationId}
        onNewChat={handleNewChat}
        refreshKey={conversationRefreshKey}
        selectedConversationId={selectedConversationId}
      />

      <ChatWindow
        conversationId={selectedConversationId}
        onConversationCreated={handleConversationCreated}
      />

    </div>
  )
}

export default Chat