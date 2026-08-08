import AIChatCard from "./AIChatCard";

export default function App() {
  return (
    <div className="min-h-screen flex justify-center items-center"
      style={{
        background: `
          radial-gradient(ellipse at 25% 25%, rgba(79,70,229,0.18) 0%, transparent 55%),
          radial-gradient(ellipse at 75% 75%, rgba(139,92,246,0.12) 0%, transparent 55%),
          #030712`
      }}>
      <AIChatCard />
    </div>
  );
}
