import React, { useState, useEffect, useImperativeHandle, forwardRef } from 'react';

export interface RebuttalTimerHandle {
  start: () => void;
  reset: () => void;
  getRemaining: () => number;
}

interface RebuttalTimerProps {
  durationSeconds: number;
}

export const RebuttalTimer = forwardRef<RebuttalTimerHandle, RebuttalTimerProps>(
  ({ durationSeconds }, ref) => {
    const [remaining, setRemaining] = useState(durationSeconds);
    const [isRunning, setIsRunning] = useState(false);

    useEffect(() => {
      if (!isRunning || remaining <= 0) {
        if (remaining <= 0) setIsRunning(false);
        return;
      }

      const interval = setInterval(() => {
        setRemaining(prev => {
          if (prev <= 1) {
            setIsRunning(false);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);

      return () => clearInterval(interval);
    }, [isRunning, remaining]);

    useImperativeHandle(ref, () => ({
      start: () => {
        setRemaining(durationSeconds);
        setIsRunning(true);
      },
      reset: () => {
        setIsRunning(false);
        setRemaining(durationSeconds);
      },
      getRemaining: () => remaining,
    }));

    const percentage = (remaining / durationSeconds) * 100;
    const isWarning = remaining < 10;
    const isCritical = remaining < 5;

    return (
      <div className="flex flex-col items-center gap-4">
        <div className="relative w-32 h-32 flex items-center justify-center">
          <svg className="w-full h-full transform -rotate-90">
            <circle
              cx="64"
              cy="64"
              r="60"
              fill="none"
              stroke="#334155"
              strokeWidth="4"
            />
            <circle
              cx="64"
              cy="64"
              r="60"
              fill="none"
              stroke={isCritical ? '#ef4444' : isWarning ? '#f59e0b' : '#3b82f6'}
              strokeWidth="4"
              strokeDasharray={`${(percentage / 100) * 376.99} 376.99`}
              className="transition-all duration-300"
            />
          </svg>
          <div className="absolute text-center">
            <div className={`text-4xl font-bold font-mono ${
              isCritical ? 'text-red-500' : isWarning ? 'text-amber-500' : 'text-blue-400'
            }`}>
              {remaining}
            </div>
            <div className="text-xs text-slate-400">seconds</div>
          </div>
        </div>
        <div className={`text-sm font-mono ${
          isCritical ? 'text-red-400' : isWarning ? 'text-amber-400' : 'text-slate-400'
        }`}>
          {isRunning ? 'THINKING...' : 'READY'}
        </div>
      </div>
    );
  }
);

RebuttalTimer.displayName = 'RebuttalTimer';
