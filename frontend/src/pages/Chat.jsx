import Sidebar from "../components/Sidebar"
import ChatWindow from "../components/ChatWindow"

function Chat() {
  return (
    <div className="h-screen flex">
      <Sidebar />
      <ChatWindow />
    </div>
  )
}

export default Chat