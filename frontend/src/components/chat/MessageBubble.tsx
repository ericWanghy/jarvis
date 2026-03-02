import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { Bot, User, Copy, Check, ThumbsUp, Edit2, Sparkles } from 'lucide-react';
import 'katex/dist/katex.min.css';
import { BrainStatus } from './BrainStatus';
import { useSettings } from '../../context/SettingsContext';

// --- Code Block Component ---
const CodeBlock = ({ node, inline, className, children, ...props }: any) => {
  const match = /language-(\w+)/.exec(className || '');
  const language = match ? match[1] : '';
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(String(children).replace(/\n$/, ''));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!inline && match) {
    return (
      <div className="relative group my-6 rounded-xl overflow-hidden border border-slate-200 dark:border-slate-700 shadow-sm bg-[#1e293b]">
        <div className="flex items-center justify-between px-4 py-2.5 bg-[#0f172a] border-b border-slate-700">
          <span className="text-xs text-slate-300 font-mono font-medium tracking-wide uppercase">{language}</span>
          <button
            onClick={handleCopy}
            className="p-1.5 hover:bg-slate-700 rounded-md text-slate-400 hover:text-white transition-colors"
            title="Copy code"
          >
            {copied ? <Check className="w-4 h-4 text-teal-400" /> : <Copy className="w-4 h-4" />}
          </button>
        </div>
        <SyntaxHighlighter
          {...props}
          style={vscDarkPlus}
          language={language}
          PreTag="div"
          customStyle={{ margin: 0, padding: '1.25rem', fontSize: '0.85rem', lineHeight: '1.5', background: 'transparent', fontFamily: 'Menlo, Monaco, Consolas, "Courier New", monospace' }}
        >
          {String(children).replace(/\n$/, '')}
        </SyntaxHighlighter>
      </div>
    );
  }

  return (
    <code {...props} className={`${className} bg-slate-100 dark:bg-slate-800 px-1.5 py-0.5 rounded-md text-pink-600 dark:text-pink-400 font-mono text-sm border border-slate-200/60 dark:border-slate-700`}>
      {children}
    </code>
  );
};

// --- Main Message Bubble ---
interface MessageBubbleProps {
  role: 'user' | 'assistant' | 'system';
  content: string;
  images?: string[];
  metadata?: any;
  timestamp?: string;
  id?: string;
  onEdit?: (content: string) => void;
}

export function MessageBubble({ role, content, images, metadata, timestamp, id, onEdit }: MessageBubbleProps) {
  const isUser = role === 'user';
  const isSystem = role === 'system';
  const { getFontSizeClass, fontSize } = useSettings();
  const fontSizeClass = getFontSizeClass(fontSize);

  // Helper to format timestamp
  const formatTime = (dateStr?: string) => {
    try {
      const date = dateStr ? new Date(dateStr) : new Date();
      return new Intl.DateTimeFormat('zh-CN', {
        month: 'numeric',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      }).format(date);
    } catch {
      return '';
    }
  };

  if (isSystem) {
    return (
      <div className="flex justify-center my-8" id={id}>
        <span className="bg-slate-50 dark:bg-slate-800/50 text-slate-500 dark:text-slate-400 px-4 py-1.5 rounded-full text-xs font-medium border border-slate-200 dark:border-slate-700/50 shadow-sm">
          {content}
        </span>
      </div>
    );
  }

  return (
    <div className={`flex flex-col w-full mb-6 px-4 md:px-6 group`} id={id}>

      {/* Header Row: Avatar + Name + Time */}
      <div className={`flex items-end gap-2 mb-1 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        {/* Avatar */}
        <div className={`
            w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center text-white shadow-sm
            ${isUser
                ? 'bg-gradient-to-br from-blue-500 to-blue-600'
                : 'bg-gradient-to-br from-indigo-500 to-purple-600'
            }
        `}>
            {isUser ? <User size={16} strokeWidth={2} /> : <Sparkles size={16} strokeWidth={2} />}
        </div>

        {/* Name & Time */}
        <div className={`flex items-baseline gap-2 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
            <span className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                {isUser ? 'Me' : 'Jarvis'}
            </span>
            <span className="text-[10px] text-slate-400 dark:text-slate-500">
                {formatTime(timestamp)}
            </span>
        </div>
      </div>

      {/* Message Content Row */}
      <div className={`
        flex flex-col max-w-[90%] md:max-w-[85%]
        ${isUser ? 'items-end self-end mr-10' : 'items-start self-start ml-10'}
        min-w-0
      `}>

        {/* Brain Status (Assistant Only) */}
        {!isUser && metadata && (
            <div className="w-full mb-2">
                <BrainStatus metadata={metadata} />
            </div>
        )}

        {/* Bubble */}
        <div className={`relative group/bubble max-w-full px-4 py-3 shadow-sm text-sm leading-relaxed transition-all duration-200
            ${isUser
                ? 'bg-blue-100/80 dark:bg-blue-900/30 text-slate-800 dark:text-slate-100 rounded-2xl rounded-tr-sm'
                : 'bg-[#f2f3f5] dark:bg-[#1e293b] text-slate-800 dark:text-slate-100 rounded-2xl rounded-tl-sm'
            } ${fontSizeClass}`}
        >
            {/* Attached Images */}
            {images && images.length > 0 && (
                <div className={`grid gap-2 mb-3 ${images.length > 1 ? 'grid-cols-2' : 'grid-cols-1'}`}>
                    {images.map((img, idx) => (
                        <img
                            key={idx}
                            src={img}
                            alt="Attachment"
                            className="w-full h-auto object-cover rounded-lg border border-slate-200/50 dark:border-slate-700 shadow-sm max-h-[300px]"
                        />
                    ))}
                </div>
            )}

            {/* Markdown Content */}
            <div className={`markdown-body relative overflow-hidden leading-relaxed ${fontSizeClass}
                ${isUser ? 'text-slate-800 dark:text-slate-100' : 'text-slate-800 dark:text-slate-100'}
            `}>
                {isUser ? (
                    <div className="whitespace-pre-wrap" style={{ lineHeight: 1.5 }}>{content}</div>
                ) : (
                    <ReactMarkdown
                        remarkPlugins={[remarkGfm, remarkMath]}
                        rehypePlugins={[rehypeKatex]}
                        components={{
                            p: ({node, ...props}) => <p className={`mb-2 last:mb-0 ${fontSizeClass}`} {...props} />,
                            h1: ({node, ...props}) => <h1 className={`text-lg font-bold mb-2 mt-3 ${fontSizeClass}`} {...props} />,
                            h2: ({node, ...props}) => <h2 className={`text-base font-bold mb-2 mt-2 ${fontSizeClass}`} {...props} />,
                            h3: ({node, ...props}) => <h3 className={`text-sm font-bold mb-1 mt-2 ${fontSizeClass}`} {...props} />,
                            ul: ({node, ...props}) => <ul className="list-disc pl-4 mb-2 space-y-0.5" {...props} />,
                            ol: ({node, ...props}) => <ol className="list-decimal pl-4 mb-2 space-y-0.5" {...props} />,
                            li: ({node, ...props}) => <li className="pl-1" {...props} />,
                            blockquote: ({node, ...props}) => <blockquote className={`border-l-2 border-slate-300 dark:border-slate-600 pl-3 italic my-2 text-slate-500 dark:text-slate-400 ${fontSizeClass}`} {...props} />,
                            a: ({node, ...props}) => <a className="text-blue-600 dark:text-blue-400 hover:underline" {...props} />,
                            code: CodeBlock,
                            table: ({node, ...props}) => (
                                <div className="overflow-x-auto my-2 rounded border border-slate-200 dark:border-slate-700">
                                    <table {...props} className="w-full text-left text-xs border-collapse" />
                                </div>
                            ),
                            th: ({node, ...props}) => <th className="p-1.5 bg-slate-100 dark:bg-slate-800 font-semibold border-b border-slate-200 dark:border-slate-700" {...props} />,
                            td: ({node, ...props}) => <td className="p-1.5 border-b border-slate-100 dark:border-slate-800 last:border-0" {...props} />,
                            hr: ({node, ...props}) => <hr className="my-4 border-t border-slate-200 dark:border-slate-700" {...props} />,
                        }}
                    >
                        {content}
                    </ReactMarkdown>
                )}
            </div>

            {/* Action Buttons */}
            <div className={`
                absolute -bottom-6 flex space-x-1 opacity-0 group-hover/bubble:opacity-100 transition-opacity duration-200
                ${isUser ? 'right-0' : 'left-0'}
            `}>
                <button
                    onClick={() => navigator.clipboard.writeText(content)}
                    className="p-1.5 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors"
                    title="复制内容"
                >
                    <Copy size={16} />
                </button>
                {isUser && onEdit && (
                    <button
                        onClick={() => onEdit(content)}
                        className="p-1.5 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors"
                        title="编辑"
                    >
                        <Edit2 size={16} />
                    </button>
                )}
                {!isUser && (
                    <button
                        className="p-1.5 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors"
                        title="点赞"
                    >
                        <ThumbsUp size={16} />
                    </button>
                )}
            </div>
        </div>
      </div>
    </div>
  );
}
