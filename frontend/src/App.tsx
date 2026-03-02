import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ChatInterface from './components/chat/ChatInterface';
import MemoriesPage from './components/memories/MemoriesPage';
import RemindersPage from './components/reminders/RemindersPage';
import PromptsPage from './components/prompts/PromptsPage';
import SettingsPage from './components/settings/SettingsPage';
import { AppTab } from './types';
import { SettingsProvider } from './context/SettingsContext';
import { ChatProvider } from './context/ChatContext';

const AppContent: React.FC = () => {
  const [activeTab, setActiveTab] = useState<AppTab>(AppTab.Chat);
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('theme');
      if (saved === 'light' || saved === 'dark') return saved;
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    return 'light'; // Default to light for v5.5
  });

  useEffect(() => {
    const root = window.document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    localStorage.setItem('theme', theme);
  }, [theme]);

  const renderContent = () => {
    switch (activeTab) {
      case AppTab.Chat:
        return <ChatInterface />;
      case AppTab.Memories:
        return <MemoriesPage />;
      case AppTab.Reminders:
        return <RemindersPage />;
      case AppTab.Prompts:
        return <PromptsPage />;
      case AppTab.Settings:
        return <SettingsPage />;
      default:
        return <ChatInterface />;
    }
  };

  return (
    <div className="flex w-full h-screen overflow-hidden bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100 font-sans selection:bg-cyan-500/30 selection:text-cyan-800 dark:selection:text-cyan-100 transition-colors duration-300">
      <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />
      <main className="flex-1 h-full relative overflow-hidden flex flex-col">
        {renderContent()}
      </main>
    </div>
  );
};

const App: React.FC = () => {
  return (
    <SettingsProvider>
      <ChatProvider>
        <AppContent />
      </ChatProvider>
    </SettingsProvider>
  );
};

export default App;
