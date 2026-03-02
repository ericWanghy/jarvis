import React, { useState } from 'react';
import { Brain, Route, Clock, Database, Lightbulb, ChevronDown, ChevronRight } from 'lucide-react';

interface BrainStatusProps {
  metadata: any;
}

export function BrainStatus({ metadata }: BrainStatusProps) {
  if (!metadata) return null;

  const [isOpen, setIsOpen] = useState(false);
  const { route, processing_time, sources } = metadata;
  const timeStr = processing_time ? `${(processing_time * 1000).toFixed(0)}ms` : 'N/A';

  return (
    <div className="mb-1 w-full overflow-hidden">
      <div
        className="flex items-center gap-1.5 cursor-pointer opacity-60 hover:opacity-100 transition-opacity"
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className="text-violet-500">
          <Brain size={12} />
        </div>
        <span className="text-[10px] font-bold text-violet-500 tracking-wide">
          THOUGHT PROCESS
        </span>
        <span className="font-mono text-[10px] text-gray-400">{timeStr}</span>
        {isOpen ? <ChevronDown size={12} className="text-gray-400" /> : <ChevronRight size={12} className="text-gray-400" />}
      </div>

      {isOpen && (
        <div className="mt-2 p-2 bg-gray-50 dark:bg-gray-800/50 rounded border border-gray-100 dark:border-gray-800 text-xs">
          <div className="flex flex-col gap-2 mt-2">
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="flex items-center gap-2 p-1.5 bg-white dark:bg-gray-800 rounded border border-slate-100 dark:border-gray-700">
                <Route size={14} className="text-indigo-500" />
                <span className="text-slate-500 dark:text-gray-400">
                  Mode: <span className="text-slate-700 dark:text-gray-200 font-mono font-semibold">{route?.primary_mode?.toUpperCase()}</span>
                </span>
              </div>
              <div className="flex items-center gap-2 p-1.5 bg-white dark:bg-gray-800 rounded border border-slate-100 dark:border-gray-700">
                <Lightbulb size={14} className="text-amber-500" />
                <span className="text-slate-500 dark:text-gray-400">
                  Intent: <span className="text-slate-700 dark:text-gray-200 font-mono font-semibold">{route?.primary_intent?.toUpperCase()}</span>
                </span>
              </div>
            </div>

            {sources && sources.length > 0 && (
              <div className="flex items-start gap-2 p-1.5 bg-white dark:bg-gray-800 rounded border border-slate-100 dark:border-gray-700">
                <Database size={14} className="text-emerald-500 mt-0.5" />
                <span className="text-slate-500 dark:text-gray-400 text-xs">
                  Sources: <span className="text-slate-700 dark:text-gray-200">{sources.join(', ')}</span>
                </span>
              </div>
            )}

            {route?.reasoning && (
              <div className="mt-1 p-2 bg-slate-100/50 dark:bg-gray-800/50 rounded border border-slate-200/50 dark:border-gray-700 font-mono text-[11px] text-slate-600 dark:text-gray-400 leading-relaxed">
                {route.reasoning}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
