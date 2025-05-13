import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Chatbot from "../components/Chatbot";

function ChatPage() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
    } else {
      setUser(token);
    }
    setLoading(false);
  }, [navigate]);

  if (loading) {
    return <p>Loading...</p>;
  }

  return (
    <div className="chat-page">
      <h2>AI Physiotherapy Chatbot</h2>
      {user ? <Chatbot /> : <p>You must be logged in to access the chatbot.</p>}
    </div>
  );
}

export default ChatPage;