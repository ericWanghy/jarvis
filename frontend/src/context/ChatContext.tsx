import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { useSettings } from './SettingsContext';
import { apiGet, apiPost, apiDelete, BASE_URL } from '../api/client';

// Types (mirrored from backend or defined here)
interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
  images?: string[];
  metadata?: any;
  created_at?: string;
  id?: string;
}

interface Session {
  id: string;
  title: string;
  created_at: string;
  updated_at?: string;
}

interface ChatContextType {
  sessions: Session[];
  activeSessionId: string | null;
  messages: Message[];
  isLoading: boolean;
  createSession: () => Promise<void>;
  loadSession: (sessionId: string) => Promise<void>;
  deleteSession: (sessionId: string) => Promise<void>;
  sendMessage: (content: string, images?: string[]) => Promise<void>;
  stopGeneration: () => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const abortControllerRef = React.useRef<AbortController | null>(null);
  const { preferredModel } = useSettings();

  // Fetch sessions on mount
  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      const data = await apiGet<Session[]>('/api/v1/sessions');
      setSessions(data);
      // Automatically load the most recent session if none is active
      if (!activeSessionId && data.length > 0) {
          // Optional: Auto-load first session
          // loadSession(data[0].id);
      }
    } catch (error) {
      console.error('Failed to fetch sessions:', error);
    }
  };

  const createSession = async () => {
    try {
      const newSession = await apiPost<Session>('/api/v1/sessions');
      setSessions(prev => [newSession, ...prev]);
      setActiveSessionId(newSession.id);
      setMessages([
          { role: 'assistant', content: '你好！我是 Jarvis v5.6。今天有什么可以帮你？', created_at: new Date().toISOString(), id: 'init-1' }
      ]);
    } catch (error) {
      console.error('Failed to create session:', error);
    }
  };

  const loadSession = async (sessionId: string) => {
    if (sessionId === activeSessionId) return;

    setIsLoading(true);
    setActiveSessionId(sessionId);
    try {
      const data = await apiGet<Message[]>(`/api/v1/sessions/${sessionId}`);
      setMessages(data);
    } catch (error) {
      console.error('Failed to load session messages:', error);
      setMessages([]);
    } finally {
      setIsLoading(false);
    }
  };

  const deleteSession = async (sessionId: string) => {
      try {
          await apiDelete(`/api/v1/sessions/${sessionId}`);
          setSessions(prev => prev.filter(s => s.id !== sessionId));
          if (activeSessionId === sessionId) {
              setActiveSessionId(null);
              setMessages([]); // Or reset to welcome screen
          }
      } catch (error) {
          console.error('Failed to delete session', error);
      }
  };

  const sendMessage = async (content: string, images: string[] = []) => {
    if ((!content.trim() && images.length === 0) || isLoading) return;

    // Ensure we have an active session
    let currentSessionId = activeSessionId;
    if (!currentSessionId) {
        // Create session first if none exists
        try {
            const newSession = await apiPost<Session>('/api/v1/sessions');
            setSessions(prev => [newSession, ...prev]);
            currentSessionId = newSession.id;
            setActiveSessionId(currentSessionId);
        } catch (e) {
            console.error(e);
            return;
        }
    }

    const userMsgId = `msg-${Date.now()}-user`;
    const assistantMsgId = `msg-${Date.now()}-assistant`;

    // Optimistic update
    const newMessages: Message[] = [
        ...messages,
        { role: 'user', content, images, created_at: new Date().toISOString(), id: userMsgId }
    ];
    setMessages(newMessages);

    // Placeholder for AI
    setMessages(prev => [...prev, { role: 'assistant', content: '', created_at: new Date().toISOString(), id: assistantMsgId }]);
    setIsLoading(true);

    abortControllerRef.current = new AbortController();

    try {
      const response = await fetch(`${BASE_URL}/api/v1/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: newMessages.map(m => ({ role: m.role, content: m.content, images: m.images })),
          stream: true,
          session_id: currentSessionId,
          preferred_model: preferredModel,
        }),
        signal: abortControllerRef.current.signal
      });

      if (!response.ok) throw new Error(response.statusText);

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let fullText = "";
      let metadata: any = null;

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value, { stream: true });
          fullText += chunk;

          // Parse metadata if present
          if (fullText.includes("__META_JSON__")) {
             const parts = fullText.split("__META_JSON__");
             fullText = parts[0];
             try {
                 metadata = JSON.parse(parts[1]);
             } catch (e) {
                 console.error("Failed to parse metadata", e);
             }
          }

          // Update UI
          setMessages(prev => {
              const last = prev[prev.length - 1];
              const others = prev.slice(0, -1);
              return [...others, { ...last, content: fullText, metadata }];
          });
        }
      }

      // Update session list to reflect "Last Updated" change
      fetchSessions();

    } catch (error: any) {
      if (error.name !== 'AbortError') {
        setMessages(prev => [...prev, { role: 'assistant', content: `Error: ${error.message}`, created_at: new Date().toISOString() }]);
      }
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  };

  const stopGeneration = () => {
      if (abortControllerRef.current) {
          abortControllerRef.current.abort();
          setIsLoading(false);
      }
  };

  return (
    <ChatContext.Provider value={{
        sessions,
        activeSessionId,
        messages,
        isLoading,
        createSession,
        loadSession,
        deleteSession,
        sendMessage,
        stopGeneration
    }}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};
