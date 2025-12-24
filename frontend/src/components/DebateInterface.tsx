import React, { useState, useEffect, useRef } from 'react';
import { RebuttalTimer, RebuttalTimerHandle } from './RebuttalTimer';
import { MessageStream } from './MessageStream';

export default function DebateInterface() {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState('');
  const [pressure, setPressure] = useState(0);
  const [tier, setTier] = useState('IDLE');
  
  const timerRef = useRef<RebuttalTimerHandle>(null);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/debate');
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'response') {
        setMessages(prev => [...prev, { role: 'assistant', content: data.text }]);
        timerRef.current?.start(); // Start timer for user reply
      } else if (data.type === 'status') {
        setPressure(data.pressure);
        setTier(data.tier);
      }
    };
    setSocket(ws);
    return () => ws.close();
  }, []);

  const sendRebuttal = () => {
    if (!socket || !input.trim()) return;
    
    const remaining = timerRef.current?.getRemaining() || 0;
    timerRef.current?.reset(); // Stop timer while bot thinks
    
    setMessages(prev => [...prev, { role: 'user', content: input }]);
    socket.send(JSON.stringify({ text: input, timer: remaining }));
    setInput('');
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 h-[600px]">
      <div className="md:col-span-2 flex flex-col bg-slate-800 rounded-xl p-4 shadow-2xl">
        <MessageStream messages={messages} />
        <div className="mt-4 flex gap-2">
          <input 
            className="flex-1 bg-slate-900 border border-slate-700 rounded p-2 text-white"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendRebuttal()}
            placeholder="Enter your argument..."
          />
          <button 
            onClick={sendRebuttal}
            className="bg-blue-600 hover:bg-blue-500 px-6 rounded font-bold"
          >
            SPAR
          </button>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        <div className="bg-slate-800 p-4 rounded-xl">
          <h3 className="text-slate-400 text-sm uppercase font-bold mb-2">Vertex Stats</h3>
          <div className="flex justify-between items-center mb-2">
            <span>Pressure:</span>
            <span className={`font-mono ${pressure > 7 ? 'text-red-500' : 'text-blue-500'}`}>
              {pressure.toFixed(1)}/10
            </span>
          </div>
          <div className="flex justify-between items-center">
            <span>Active Cortex:</span>
            <span className="font-mono text-xs bg-slate-700 px-2 py-1 rounded">
              {tier}
            </span>
          </div>
        </div>
        
        <div className="bg-slate-800 p-4 rounded-xl flex flex-col items-center justify-center flex-1">
          <h3 className="text-slate-400 text-sm uppercase font-bold mb-4">Rebuttal Clock</h3>
          <RebuttalTimer ref={timerRef} durationSeconds={60} />
        </div>
      </div>
    </div>
  );
}