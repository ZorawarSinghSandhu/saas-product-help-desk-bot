import { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { Send } from "lucide-react";

function cn(...classes) {
  return classes.filter(Boolean).join(" ");
}

export default function AIChatCard({ className }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messageRef = useRef(null);

  const SUGGESTIONS = [
    "How does seat billing work?",
    "What is active user billing?",
    "Tell me about Delegation Credential",
    "What is high water mark billing?",
  ];

  useEffect(() => {
    if (messageRef.current) {
      messageRef.current.scrollTop = messageRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async (text) => {
    const question = text || input;
    if (!question.trim() || isTyping) return;

    setMessages((prev) => [
      ...prev,
      { sender: "user", text: question, citations: [] },
    ]);
    setInput("");
    setIsTyping(true);
    const url = `${import.meta.env.VITE_API_URL}/ask`;

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: question }),
      });
      if (!response.ok) {
        console.log(await response.text());
        throw new Error(`Response Status: ${response.status}`);
      }

      const result = await response.json();

      const unique_urls = [...new Set(result.sources)];
      const file_names = [...new Set(result.file_headings)];

      const citations = (unique_urls || []).map((url, index) => ({
        url: url,
        heading: file_names?.[index] ?? "Source",
      }));

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: result.answer,
          citations,
        },
      ]);
      setIsTyping(false);
    } catch (error) {
      setIsTyping(false);
      console.log(error.message);

      setMessages((prev) => [
        ...prev,
        { sender: "ai", text: "Sorry, something went wrong." },
      ]);
    }
  };

  return (
    <div
      className={cn(
        "relative w-[90vw] max-w-4xl h-[90vh] rounded-2xl overflow-hidden p-[2px]",
        className,
      )}
    >
      {/* Animated Outer Border */}
      <motion.div
        className="pointer-events-none absolute inset-0 rounded-2xl border-2 border-indigo-500/40"
        animate={{ rotate: [0, 360] }}
        transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
      />

      {/* Inner Card */}
      <div className="relative z-10 flex flex-col w-full h-full rounded-xl border border-white/10 overflow-hidden bg-black/90 backdrop-blur-xl">
        {/* Inner Animated Background */}
        <div className="pointer-events-none absolute inset-0 z-0 bg-linear-to-br from-indigo-950 via-slate-950 to-purple-950" />

        {/* Floating Particles */}
        {Array.from({ length: 20 }).map((_, i) => (
          <motion.div
            key={i}
            className="pointer-events-none absolute w-1 h-1 rounded-full bg-indigo-400/20"
            animate={{
              y: ["0%", "-140%"],
              x: [Math.random() * 200 - 100, Math.random() * 200 - 100],
              opacity: [0, 1, 0],
            }}
            transition={{
              duration: 5 + Math.random() * 3,
              repeat: Infinity,
              delay: i * 0.5,
              ease: "easeInOut",
            }}
            style={{ left: `${Math.random() * 100}%`, bottom: "-10%" }}
          />
        ))}

        {/* Header */}
        <div className="px-4 py-3 border-b border-white/10 relative z-10">
          <h2 className="text-lg font-semibold text-white">
            🤖 Cal.com Support AI
          </h2>
        </div>

        {/* Messages */}
        {messages.length === 0 && (
          <div className="relative z-20 flex flex-col items-center justify-center h-full gap-5 text-center">
            <p className="text-white text-xl font-semibold">
              How can I help you?
            </p>
            <div className="flex flex-col gap-2 w-full max-w-xs">
              {SUGGESTIONS.map((s, i) => (
                <button
                  key={i}
                  onClick={() => handleSend(s)}
                  className="relative z-30 text-left text-sm text-white/70 bg-white/10 hover:bg-white/20 border border-white/10 hover:border-white/20 rounded-xl px-4 py-3 transition-all duration-150"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        <div
          ref={messageRef}
          className="flex-1 px-4 py-3 overflow-y-auto space-y-3 text-sm flex flex-col relative z-10"
        >
          {messages.map((msg, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4 }}
              className={cn(
                "px-3 py-2 rounded-xl max-w-[80%] shadow-md backdrop-blur-md",
                msg.sender === "ai"
                  ? "bg-slate-800/90 text-slate-100 self-start border border-indigo-500/15"
                  : "bg-indigo-600 text-white self-end",
              )}
            >
              {msg.text}

              {msg.citations?.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-2">
                  {msg.citations.map((citation, index) => (
                    <a
                      key={index}
                      href={citation.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-3 py-1 rounded-md bg-indigo-500/20 hover:bg-indigo-500/30 text-indigo-300 text-xs"
                    >
                      {citation.heading}
                    </a>
                  ))}
                </div>
              )}
            </motion.div>
          ))}

          {/* AI Typing Indicator */}
          {isTyping && (
            <motion.div
              className="flex items-center gap-1 px-3 py-2 rounded-xl max-w-[30%] bg-white/10 self-start"
              initial={{ opacity: 0 }}
              animate={{ opacity: [0, 1, 0.6, 1] }}
              transition={{ repeat: Infinity, duration: 1.2 }}
            >
              <span className="w-2 h-2 rounded-full bg-white animate-pulse"></span>
              <span className="w-2 h-2 rounded-full bg-white animate-pulse delay-200"></span>
              <span className="w-2 h-2 rounded-full bg-white animate-pulse delay-400"></span>
            </motion.div>
          )}
        </div>

        {/* Input */}
        <div className="flex items-center gap-2 p-3 border-t border-white/10 relative z-10">
          <input
            className="flex-1 px-3 py-2 text-sm bg-white/10 rounded-lg border border-white/10 text-white focus:outline-none focus:ring-1 focus:ring-white/50"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button
            disabled={isTyping}
            onClick={handleSend}
            className="p-2 rounded-lg bg-white/10 hover:bg-white/20 transition-colors"
          >
            <Send className="w-4 h-4 text-white" />
          </button>
        </div>
      </div>
    </div>
  );
}
