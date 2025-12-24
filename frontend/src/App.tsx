import React from 'react';
import DebateInterface from './components/DebateInterface';

function App() {
  return (
    <div className="min-h-screen bg-slate-900 text-white flex flex-col items-center p-4">
      <header className="w-full max-w-4xl py-6 border-b border-slate-700 mb-8">
        <h1 className="text-3xl font-bold tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">
          DEBATE VERTEX // HYBRID
        </h1>
      </header>
      <main className="w-full max-w-4xl flex-1">
        <DebateInterface />
      </main>
    </div>
  );
}
export default App;