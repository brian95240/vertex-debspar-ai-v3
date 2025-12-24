import React from 'react';

export function MessageStream({ messages }: { messages: any[] }) {
  return (
    <div className="flex-1 overflow-y-auto space-y-4 pr-2 scrollbar-thin scrollbar-thumb-slate-600">
      {messages.map((m, i) => (
        <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
          <div className={`max-w-[80%] rounded-lg p-3 ${
            m.role === 'user' ? 'bg-blue-900 text-blue-100' : 'bg-slate-700 text-slate-200'
          }`}>
            <p className="text-sm">{m.content}</p>
          </div>
        </div>
      ))}
      {messages.length === 0 && (
        <div className="h-full flex items-center justify-center text-slate-500 italic">
          System Initialized. Awaiting opening statement.
        </div>
      )}
    </div>
  );
}