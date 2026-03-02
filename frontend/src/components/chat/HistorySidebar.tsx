import { ActionIcon, Tooltip, ScrollArea, Box, Text } from '@mantine/core';
import { IconArrowUp, IconArrowDown } from '@tabler/icons-react';

interface HistorySidebarProps {
  messages: Array<{
    role: 'user' | 'assistant' | 'system';
    id?: string;
    content: string;
    created_at?: string;
  }>;
  onScrollTo: (id: string) => void;
}

export function HistorySidebar({ messages, onScrollTo }: HistorySidebarProps) {
  // Filter out system messages for navigation to keep it clean
  const navMessages = messages.filter(msg => msg.role !== 'system');

  const handleScrollToTop = () => {
    if (navMessages.length > 0 && navMessages[0].id) {
        onScrollTo(navMessages[0].id);
    }
  };

  const handleScrollToBottom = () => {
    if (navMessages.length > 0) {
        const lastMsg = navMessages[navMessages.length - 1];
        if (lastMsg.id) onScrollTo(lastMsg.id);
    }
  };

  return (
    <div className="w-12 h-full flex flex-col items-center py-4 bg-white/50 border-l border-slate-100/50 backdrop-blur-sm">
      <Tooltip label="Scroll to Top" position="left">
        <ActionIcon
          variant="subtle"
          color="gray"
          onClick={handleScrollToTop}
          className="mb-2 hover:bg-slate-100"
        >
          <IconArrowUp size={16} />
        </ActionIcon>
      </Tooltip>

      <ScrollArea className="flex-1 w-full" scrollbarSize={2}>
        <div className="flex flex-col items-center gap-1 py-2">
          {navMessages.map((msg, i) => (
            <Tooltip
              key={i}
              label={`${msg.role === 'user' ? 'You' : 'Jarvis'}: ${msg.content.slice(0, 30)}${msg.content.length > 30 ? '...' : ''}`}
              position="left"
              withArrow
              transitionProps={{ duration: 200, transition: 'fade' }}
            >
              <button
                onClick={() => msg.id && onScrollTo(msg.id)}
                className={`
                  group relative w-3 h-3 rounded-full transition-all duration-300
                  ${msg.role === 'user'
                    ? 'bg-emerald-200 hover:bg-emerald-400'
                    : 'bg-indigo-200 hover:bg-indigo-400'
                  }
                `}
              >
                {/* Active/Hover Indicator */}
                <div className="absolute inset-0 rounded-full opacity-0 group-hover:opacity-100 group-hover:scale-150 transition-all bg-current opacity-20" />
              </button>
            </Tooltip>
          ))}
        </div>
      </ScrollArea>

      <Tooltip label="Scroll to Bottom" position="left">
        <ActionIcon
          variant="subtle"
          color="gray"
          onClick={handleScrollToBottom}
          className="mt-2 hover:bg-slate-100"
        >
          <IconArrowDown size={16} />
        </ActionIcon>
      </Tooltip>
    </div>
  );
}
