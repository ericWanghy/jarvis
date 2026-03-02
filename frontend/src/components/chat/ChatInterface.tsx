import React, { useState, useRef, useEffect } from 'react';
import {
  Send,
  Plus,
  ChevronRight,
  PanelRightClose,
  MoreHorizontal,
  Bot,
  Database,
  Search,
  Loader2,
  X,
  Trash2,
  Mic
} from 'lucide-react';
import { useChat } from '../../context/ChatContext';
import { MessageBubble } from './MessageBubble';

const ChatInterface: React.FC = () => {
  const {
    activeSessionId,
    messages,
    isLoading,
    sendMessage,
    stopGeneration,
    sessions,
    createSession,
    loadSession,
    deleteSession
  } = useChat();

  const [input, setInput] = useState('');
  const [isSidebarOpen, setSidebarOpen] = useState(false);
  const [attachedImages, setAttachedImages] = useState<string[]>([]);
  const isComposing = useRef(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = async () => {
    if ((!input.trim() && attachedImages.length === 0) || isLoading) return;

    const content = input;
    const images = [...attachedImages];

    setInput('');
    setAttachedImages([]);

    try {
      await sendMessage(content, images);
    } catch (error) {
      console.error('Failed to send message:', error);
      // Restore input on error
      setInput(content);
      setAttachedImages(images);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      if (isComposing.current || e.nativeEvent.isComposing || e.keyCode === 229) {
        e.preventDefault();
        return;
      }
      e.preventDefault();
      handleSend();
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files) return;

    Array.from(files).forEach(file => {
      if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
          if (e.target?.result) {
            setAttachedImages(prev => [...prev, e.target!.result as string]);
          }
        };
        reader.readAsDataURL(file);
      }
    });
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const removeImage = (index: number) => {
    setAttachedImages(prev => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="flex h-full w-full bg-gray-50 dark:bg-black transition-colors duration-300 overflow-hidden relative">
      {/* Session Sidebar - Collapsed by Default */}
      <div className={`${isSidebarOpen ? 'w-72 opacity-100 translate-x-0' : 'w-0 opacity-0 -translate-x-10'} bg-gray-50 dark:bg-black border-r border-gray-200 dark:border-gray-800 transition-all duration-300 ease-[cubic-bezier(0.25,0.1,0.25,1)] flex flex-col shrink-0 overflow-hidden z-20`}>
        <div className="p-4 border-b border-gray-200 dark:border-gray-800">
          <button
            onClick={createSession}
            className="w-full bg-cyan-600 hover:bg-cyan-500 active:scale-[0.98] text-white p-3 rounded-xl flex items-center justify-center gap-2 font-medium transition-all shadow-lg shadow-cyan-900/20 group"
          >
            <Plus className="w-4 h-4 group-hover:rotate-90 transition-transform duration-300" />
            <span className="text-sm">New Chat</span>
          </button>
        </div>
        <div className="flex-1 overflow-y-auto px-3 py-2 space-y-1 scrollbar-thin scrollbar-thumb-gray-200 dark:scrollbar-thumb-gray-800">
          {sessions.map(session => (
            <div
              key={session.id}
              onClick={() => loadSession(session.id)}
              className={`group p-3 rounded-xl text-sm cursor-pointer shadow-sm relative overflow-hidden transition-all border
                ${activeSessionId === session.id
                  ? 'bg-white dark:bg-gray-900 border-cyan-500/50 dark:border-cyan-500/50'
                  : 'bg-transparent border-transparent hover:bg-gray-100 dark:hover:bg-gray-900 hover:border-gray-200 dark:hover:border-gray-800'
                }`}
            >
              {activeSessionId === session.id && (
                <div className="absolute left-0 top-0 bottom-0 w-1 bg-cyan-500"></div>
              )}
              <div className="flex justify-between items-center">
                <span className={`font-medium truncate pr-2 ${activeSessionId === session.id ? 'text-gray-900 dark:text-gray-100' : 'text-gray-600 dark:text-gray-400'}`}>
                  {session.title || 'New Conversation'}
                </span>
                <button
                  onClick={(e) => { e.stopPropagation(); deleteSession(session.id); }}
                  className="opacity-0 group-hover:opacity-100 p-1 hover:text-red-500 text-gray-400 transition-opacity"
                >
                  <Trash2 className="w-3 h-3" />
                </button>
              </div>
              <div className="text-[10px] text-gray-400 mt-1">
                {new Date(session.updated_at || session.created_at).toLocaleDateString()}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col relative min-w-0 bg-white dark:bg-[#050505]">
        {/* Header - Glassmorphism */}
        <header className="h-14 flex items-center justify-between px-6 z-10 sticky top-0 bg-white/80 dark:bg-black/80 backdrop-blur-xl border-b border-gray-200 dark:border-gray-800 transition-colors duration-300">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setSidebarOpen(!isSidebarOpen)}
              className="p-2 hover:bg-gray-100 dark:hover:bg-gray-900 rounded-lg text-gray-500 dark:text-gray-400 transition-colors"
              title={isSidebarOpen ? "Collapse Sidebar" : "Expand Sidebar"}
            >
              {isSidebarOpen ? <PanelRightClose className="w-5 h-5" /> : <ChevronRight className="w-5 h-5" />}
            </button>
            <div className="flex flex-col">
              <h2 className="font-semibold text-gray-900 dark:text-gray-100 tracking-tight flex items-center gap-2 text-sm">
                Jarvis AI
                {/* RAG Indicator (Mock) */}
                <span className="flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] bg-gray-100 dark:bg-gray-900 text-gray-500 dark:text-gray-400 font-medium border border-gray-200 dark:border-gray-800">
                  <Database className="w-3 h-3" />
                  <span>Local Context</span>
                </span>
              </h2>
            </div>
          </div>
          <div className="flex items-center gap-1">
            <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-900 rounded-lg text-gray-500 dark:text-gray-400 transition-colors" title="Search History">
              <Search className="w-4 h-4" />
            </button>
            <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-900 rounded-lg text-gray-500 dark:text-gray-400 transition-colors">
              <MoreHorizontal className="w-4 h-4" />
            </button>
          </div>
        </header>

        {/* Message List */}
        <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-2 scroll-smooth scrollbar-thin scrollbar-thumb-gray-200 dark:scrollbar-thumb-gray-800">
          {messages.map((msg) => (
            <MessageBubble
              key={msg.id}
              role={msg.role}
              content={msg.content}
              images={msg.images}
              metadata={msg.metadata}
              timestamp={msg.created_at}
              id={msg.id}
            />
          ))}

          {isLoading && messages.length > 0 && messages[messages.length - 1].role !== 'assistant' && (
             <div className="flex w-full gap-3 mb-6 px-4 animate-in fade-in duration-300">
                {/* Avatar */}
                <div className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 shadow-sm border border-gray-200 dark:border-gray-800 mt-0.5 bg-gradient-to-br from-indigo-600 via-blue-600 to-cyan-500">
                   <Bot className="w-4 h-4 text-white" />
                </div>

                <div className="flex flex-col items-start">
                   {/* Header */}
                   <div className="flex items-center gap-2 mb-1">
                     <span className="text-xs font-bold text-gray-700 dark:text-gray-200">JARVIS</span>
                     <span className="text-[10px] text-gray-400 dark:text-gray-500 font-mono">Thinking...</span>
                   </div>

                   {/* Loading Bubble */}
                   <div className="px-4 py-3 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl rounded-tl-sm shadow-sm flex items-center gap-2">
                      <span className="w-1.5 h-1.5 bg-cyan-500 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                      <span className="w-1.5 h-1.5 bg-cyan-500 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                      <span className="w-1.5 h-1.5 bg-cyan-500 rounded-full animate-bounce"></span>
                   </div>
                </div>
             </div>
          )}
          <div ref={messagesEndRef} className="h-4" />
        </div>

        {/* Input Bar - Floating & Elegant */}
        <div className="p-4 bg-white/80 dark:bg-black/80 backdrop-blur-md border-t border-gray-200 dark:border-gray-800 z-20">
          <div className="max-w-4xl mx-auto relative group">
            <div className={`absolute -inset-0.5 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-2xl opacity-0 group-focus-within:opacity-20 transition duration-500 blur`}></div>
            <div className="relative flex flex-col bg-gray-50 dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-2 shadow-sm transition-all group-focus-within:bg-white dark:group-focus-within:bg-black group-focus-within:shadow-md">

              {/* Image Previews */}
              {attachedImages.length > 0 && (
                <div className="flex gap-2 mb-2 overflow-x-auto px-2 pt-2">
                  {attachedImages.map((img, idx) => (
                    <div key={idx} className="relative group/img">
                      <img src={img} alt="Preview" className="h-16 w-16 object-cover rounded-lg border border-gray-200 dark:border-gray-700" />
                      <button
                        onClick={() => removeImage(idx)}
                        className="absolute -top-1 -right-1 bg-red-500 text-white rounded-full p-0.5 opacity-0 group-hover/img:opacity-100 transition-opacity shadow-sm"
                      >
                        <X className="w-3 h-3" />
                      </button>
                    </div>
                  ))}
                </div>
              )}

              <div className="flex items-end gap-2">
                {/* Attachments & Tools */}
                <div className="flex items-center gap-1 pb-2 pl-1">
                   <input
                      type="file"
                      ref={fileInputRef}
                      onChange={handleFileSelect}
                      className="hidden"
                      accept="image/*"
                      multiple
                    />
                   <button
                    onClick={() => fileInputRef.current?.click()}
                    className="p-2 text-gray-400 hover:text-cyan-600 dark:hover:text-cyan-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full transition-colors"
                    title="Add Attachment"
                   >
                     <Plus className="w-5 h-5" />
                   </button>
                   <button className="hidden md:block p-2 text-gray-400 hover:text-cyan-600 dark:hover:text-cyan-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full transition-colors" title="Local Context (RAG)">
                     <Database className="w-5 h-5" />
                   </button>
                </div>

                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  onCompositionStart={() => { isComposing.current = true; }}
                  onCompositionEnd={() => { isComposing.current = false; }}
                  placeholder="Message Jarvis..."
                  className="flex-1 bg-transparent text-gray-900 dark:text-gray-100 p-3 max-h-[150px] resize-none focus:outline-none scrollbar-hide placeholder-gray-400 dark:placeholder-gray-500 leading-relaxed text-sm"
                  rows={1}
                  style={{ minHeight: '44px' }}
                />

                {/* Right Side Actions */}
                <div className="flex items-center gap-1 pb-1.5 pr-1">
                   {/* Live Mode Toggle (Visual Only) */}
                   {!input.trim() && attachedImages.length === 0 && (
                      <button className="p-2 text-gray-400 hover:text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-900/20 rounded-full transition-all duration-300 group/mic" title="Live Voice Mode (Coming Soon)">
                         <Mic className="w-5 h-5 group-hover/mic:scale-110" />
                      </button>
                   )}

                   {/* Send Button */}
                   {isLoading ? (
                      <button
                        onClick={stopGeneration}
                        className="p-2.5 bg-red-500 hover:bg-red-600 text-white rounded-xl transition-all shadow-sm"
                      >
                        <Loader2 className="w-5 h-5 animate-spin" />
                      </button>
                   ) : (
                      <button
                        onClick={handleSend}
                        disabled={!input.trim() && attachedImages.length === 0}
                        className={`p-2.5 rounded-xl transition-all duration-300
                          ${(input.trim() || attachedImages.length > 0)
                            ? 'bg-cyan-600 text-white shadow-lg shadow-cyan-600/20 hover:bg-cyan-500 active:scale-95'
                            : 'bg-gray-200 dark:bg-gray-800 text-gray-400 cursor-not-allowed hidden'}`}
                      >
                        <Send className="w-5 h-5 ml-0.5" />
                      </button>
                   )}
                </div>
              </div>
            </div>

            <div className="text-center mt-2 opacity-0 group-focus-within:opacity-100 transition-opacity duration-500">
               <p className="text-[10px] text-gray-400 dark:text-gray-600 font-medium tracking-wide flex items-center justify-center gap-2">
                 <span>Neural Engine X</span>
                 <span className="w-0.5 h-2 bg-gray-300 dark:bg-gray-800"></span>
                 <span>Local Context Active</span>
               </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
