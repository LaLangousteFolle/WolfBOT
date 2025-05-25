"use client";

export default function Home() {
  const handleLogin = () => {
    window.location.href = "http://localhost:8000/login";
  };

  return (
    <main className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-4xl font-bold mb-6">WolfBot</h1>
      <button
        onClick={handleLogin}
        className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700 transition"
      >
        Se connecter avec Discord
      </button>
    </main>
  );
}
