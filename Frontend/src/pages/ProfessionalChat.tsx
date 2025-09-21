import React, { useState, useRef, useEffect } from "react";

const ProfessionalChat: React.FC = () => {
  const [messages, setMessages] = useState<{ user: string; text: string }[]>([]);
  const [input, setInput] = useState("");
  const [logs, setLogs] = useState<string[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new message is added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;
    const newMessage = { user: "You", text: input };
    setMessages((prev) => [...prev, newMessage]);
    setLogs((prev) => [...prev, `Sent: ${input}`]); // log message
    setInput("");
    
    // Simulate AI response
    setTimeout(() => {
      const aiResponse = { user: "AgentForce AI", text: `Received: ${input}` };
      setMessages((prev) => [...prev, aiResponse]);
      setLogs((prev) => [...prev, `AI: ${aiResponse.text}`]);
    }, 700);
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#0A0A0D] text-white px-4 py-6">
      <h1 className="text-4xl font-extrabold text-gradient mb-6 text-center">
        Professional Chat
      </h1>

      {/* Chat Window */}
      <div className="flex-1 bg-[#1C1B29] rounded-2xl shadow-xl p-4 flex flex-col mb-4 overflow-hidden">
        <div className="flex-1 overflow-y-auto mb-4">
          {messages.map((msg, index) => (
            <div key={index} className="mb-3">
              <span className="font-bold text-[#7C3AED]">{msg.user}: </span>
              <span>{msg.text}</span>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="flex space-x-2">
          <input
            type="text"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            className="flex-1 px-4 py-3 rounded-xl bg-[#0A0A0D] border border-[#7C3AED] text-white focus:outline-none focus:ring-2 focus:ring-[#7C3AED]"
          />
          <button
            onClick={handleSend}
            className="px-6 py-3 bg-gradient-to-r from-[#7C3AED] to-[#5B21B6] font-bold rounded-xl hover:scale-105 transition-transform"
          >
            Send
          </button>
        </div>
      </div>

      {/* Logs Window */}
      <div className="h-48 bg-[#1C1B29] rounded-2xl shadow-xl p-4 overflow-y-auto font-mono text-sm text-[#A3A3A3]">
        <h2 className="text-lg font-bold text-gradient mb-2">Logs</h2>
        {logs.map((log, idx) => (
          <div key={idx}>{log}</div>
        ))}
      </div>
    </div>
  );
};

export default ProfessionalChat;
