import React from 'react';
import { MessageSquare, Brain, Calendar, Terminal, Settings, Hexagon } from 'lucide-react';
import { AppTab } from '../types';

interface SidebarProps {
  activeTab: AppTab;
  onTabChange: (tab: AppTab) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activeTab, onTabChange }) => {
  const navItems = [
    { id: AppTab.Chat, icon: MessageSquare, label: '对话' },
    { id: AppTab.Memories, icon: Brain, label: '记忆库' },
    { id: AppTab.Reminders, icon: Calendar, label: '日程' },
    { id: AppTab.Prompts, icon: Terminal, label: '提示词' },
    { id: AppTab.Settings, icon: Settings, label: '设置' },
  ];

  return (
    <div className="w-20 lg:w-64 h-full bg-gray-50 dark:bg-black border-r border-gray-200 dark:border-gray-800 flex flex-col justify-between shrink-0 transition-all duration-300 z-30 relative">
      <div>
        {/* App Logo/Header */}
        <div className="h-16 flex items-center justify-center lg:justify-start lg:px-6 border-b border-gray-200 dark:border-gray-800">
          <div className="relative group">
            <div className="absolute -inset-1 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-full blur opacity-25 group-hover:opacity-50 transition duration-200"></div>
            <Hexagon className="relative w-8 h-8 text-cyan-600 dark:text-cyan-500 transform transition-transform group-hover:rotate-180 duration-700" strokeWidth={2} />
          </div>
          <div className="hidden lg:flex flex-col ml-3">
            <span className="font-bold text-lg tracking-wider text-gray-900 dark:text-white font-sans">JARVIS</span>
            <span className="text-[10px] text-gray-500 dark:text-gray-400 font-mono tracking-widest">SYSTEM v5.5</span>
          </div>
        </div>

        {/* Navigation */}
        <nav className="mt-6 flex flex-col gap-2 px-3">
          {navItems.map((item) => {
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onTabChange(item.id)}
                className={`flex items-center justify-center lg:justify-start p-3 rounded-xl transition-all duration-200 group relative overflow-hidden
                  ${isActive
                    ? 'bg-white dark:bg-gray-900 text-cyan-600 dark:text-cyan-400 shadow-sm ring-1 ring-gray-200 dark:ring-gray-800'
                    : 'text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-900 hover:text-gray-900 dark:hover:text-gray-200'
                  }`}
              >
                <item.icon className={`w-5 h-5 transition-colors duration-200 ${isActive ? 'text-cyan-600 dark:text-cyan-400' : 'group-hover:text-gray-700 dark:group-hover:text-gray-300'}`} strokeWidth={isActive ? 2.5 : 2} />
                <span className={`hidden lg:block ml-3 text-sm font-medium tracking-wide ${isActive ? 'font-semibold' : ''}`}>
                  {item.label}
                </span>
                {isActive && (
                  <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 bg-cyan-500 rounded-r-full" />
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* User / Status */}
      <div className="p-4 border-t border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-black">
        <div className="flex items-center justify-center lg:justify-start gap-3 group cursor-pointer">
          <div className="relative">
            <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-cyan-600 to-blue-600 flex items-center justify-center text-xs font-bold text-white shadow-lg ring-2 ring-white dark:ring-gray-900 group-hover:ring-cyan-500/50 transition-all duration-300">
              WH
            </div>
            <span className="absolute bottom-0 right-0 w-2.5 h-2.5 rounded-full bg-green-500 ring-2 ring-white dark:ring-black"></span>
          </div>
          <div className="hidden lg:block overflow-hidden">
            <p className="text-sm font-semibold text-gray-800 dark:text-gray-200 truncate group-hover:text-cyan-500 transition-colors">Wang Huiyong</p>
            <p className="text-[10px] text-gray-500 dark:text-gray-500 font-medium tracking-wide uppercase">System Admin</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
