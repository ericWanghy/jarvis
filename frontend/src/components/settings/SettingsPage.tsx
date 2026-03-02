import React, { useState } from 'react';
import {
  Settings,
  Brain,
  Bell,
  Info,
  AlertTriangle,
  Monitor,
  Volume2,
  Cpu,
  Key,
  Database,
  Check,
  Type,
  HardDrive,
  Shield,
  Activity,
  Zap,
  Moon,
  Sun,
  Laptop
} from 'lucide-react';
import { useSettings } from '../../context/SettingsContext';
import ReactMarkdown from 'react-markdown';

// Types
type SettingsSection = 'general' | 'brain' | 'notifications' | 'storage' | 'about';

export default function SettingsPage() {
  const { fontSize, setFontSize, preferredModel, setPreferredModel } = useSettings();
  const [activeSection, setActiveSection] = useState<SettingsSection>('general');
  const [theme, setTheme] = useState<'light' | 'dark' | 'system'>('light');

  // Navigation Items
  const navItems = [
    { id: 'general', label: 'General', icon: Settings },
    { id: 'brain', label: 'Brain & LLM', icon: Brain },
    { id: 'notifications', label: 'Notifications', icon: Bell },
    { id: 'storage', label: 'Storage', icon: Database },
    { id: 'about', label: 'About', icon: Info },
  ];

  // Render Content Based on Section
  const renderContent = () => {
    switch (activeSection) {
      case 'general':
        return (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-300">
            <div className="bg-white dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700/50 rounded-2xl p-6 shadow-sm">
              <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-1">Appearance</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">Customize how Jarvis looks and feels.</p>

              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Theme Mode</label>
                  <div className="grid grid-cols-3 gap-3">
                    {[
                      { id: 'light', label: 'Light', icon: Sun },
                      { id: 'dark', label: 'Dark', icon: Moon },
                      { id: 'system', label: 'System', icon: Laptop },
                    ].map((item) => (
                      <button
                        key={item.id}
                        onClick={() => setTheme(item.id as any)}
                        className={`
                          flex flex-col items-center justify-center gap-2 p-4 rounded-xl border transition-all
                          ${theme === item.id
                            ? 'bg-cyan-50 dark:bg-cyan-900/20 border-cyan-500 text-cyan-600 dark:text-cyan-400'
                            : 'bg-gray-50 dark:bg-gray-800 border-transparent hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-600 dark:text-gray-400'
                          }
                        `}
                      >
                        <item.icon size={20} />
                        <span className="text-sm font-medium">{item.label}</span>
                      </button>
                    ))}
                  </div>
                </div>

                <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800/50 rounded-xl border border-gray-100 dark:border-gray-700">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-white dark:bg-gray-700 rounded-lg text-gray-500">
                      <Type size={18} />
                    </div>
                    <div>
                      <div className="text-sm font-medium text-gray-700 dark:text-gray-200">Font Size</div>
                      <div className="text-xs text-gray-500">Adjust text size for chat messages</div>
                    </div>
                  </div>
                  <div className="flex bg-white dark:bg-gray-700 rounded-lg p-1 border border-gray-200 dark:border-gray-600">
                    {['small', 'medium', 'large'].map((size) => (
                      <button
                        key={size}
                        onClick={() => setFontSize(size as any)}
                        className={`
                          px-3 py-1 rounded-md text-xs font-medium transition-all capitalize
                          ${fontSize === size
                            ? 'bg-cyan-100 dark:bg-cyan-900/50 text-cyan-700 dark:text-cyan-300 shadow-sm'
                            : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'
                          }
                        `}
                      >
                        {size}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700/50 rounded-2xl p-6 shadow-sm">
              <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-1">Behavior</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">Configure application startup and interactions.</p>

              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800/50 rounded-xl border border-gray-100 dark:border-gray-700">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-white dark:bg-gray-700 rounded-lg text-gray-500">
                      <Zap size={18} />
                    </div>
                    <div>
                      <div className="text-sm font-medium text-gray-700 dark:text-gray-200">Launch at Startup</div>
                      <div className="text-xs text-gray-500">Open Jarvis automatically when you log in</div>
                    </div>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" className="sr-only peer" defaultChecked />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-cyan-300 dark:peer-focus:ring-cyan-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-cyan-600"></div>
                  </label>
                </div>

                <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800/50 rounded-xl border border-gray-100 dark:border-gray-700">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-white dark:bg-gray-700 rounded-lg text-gray-500">
                      <Volume2 size={18} />
                    </div>
                    <div>
                      <div className="text-sm font-medium text-gray-700 dark:text-gray-200">Sound Effects</div>
                      <div className="text-xs text-gray-500">Play subtle sounds for actions</div>
                    </div>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" className="sr-only peer" defaultChecked />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-cyan-300 dark:peer-focus:ring-cyan-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-cyan-600"></div>
                  </label>
                </div>
              </div>
            </div>
          </div>
        );

      case 'brain':
        return (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-300">
            <div className="bg-white dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700/50 rounded-2xl p-6 shadow-sm">
              <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-1">Model Configuration</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">Configure the underlying LLM parameters.</p>

              <div className="bg-cyan-50 dark:bg-cyan-900/20 border border-cyan-100 dark:border-cyan-800 rounded-xl p-4 mb-6 flex gap-3">
                <Cpu className="text-cyan-600 dark:text-cyan-400 shrink-0 mt-0.5" size={20} />
                <div>
                  <h4 className="text-sm font-semibold text-cyan-900 dark:text-cyan-300">Brain Orchestrator v2.1</h4>
                  <p className="text-xs text-cyan-700 dark:text-cyan-400 mt-1">
                    Currently using local gateway routing. All requests are processed within the secure enterprise perimeter.
                  </p>
                </div>
              </div>

              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Preferred Model</label>
                  <div className="relative">
                    <Brain className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
                    <select
                      value={preferredModel}
                      onChange={(e) => setPreferredModel(e.target.value as any)}
                      className="w-full pl-10 pr-4 py-2.5 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl text-sm focus:ring-2 focus:ring-cyan-500/20 focus:border-cyan-500 outline-none transition-all appearance-none"
                    >
                      <option value="gpt5-1">Internal GPT-5 (Default)</option>
                      <option value="gemini3">Internal Gemini 3 (Multimodal)</option>
                      <option value="qwen">Qwen Public (Fallback)</option>
                    </select>
                  </div>
                  <p className="text-xs text-gray-500 mt-2">Primary model used for complex reasoning tasks.</p>
                </div>

                <div className="pt-6 border-t border-gray-100 dark:border-gray-800">
                  <h4 className="text-sm font-semibold text-gray-800 dark:text-gray-200 mb-4">Gateway Connection</h4>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-xs font-medium text-gray-500 uppercase tracking-wider mb-1.5">Endpoint URL</label>
                      <div className="relative">
                        <Activity className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={16} />
                        <input
                          type="text"
                          defaultValue="http://api-hub.inner.chj.cloud/llm-gateway/v1"
                          className="w-full pl-10 pr-4 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg text-xs font-mono text-gray-600 dark:text-gray-300 focus:ring-2 focus:ring-cyan-500/20 focus:border-cyan-500 outline-none"
                        />
                      </div>
                    </div>
                    <div>
                      <label className="block text-xs font-medium text-gray-500 uppercase tracking-wider mb-1.5">API Key</label>
                      <div className="relative">
                        <Key className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={16} />
                        <input
                          type="password"
                          defaultValue="sk-xxxxxxxxxxxxxxxxxxxxxxxx"
                          className="w-full pl-10 pr-4 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg text-xs font-mono text-gray-600 dark:text-gray-300 focus:ring-2 focus:ring-cyan-500/20 focus:border-cyan-500 outline-none"
                        />
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-red-50 dark:bg-red-900/10 border border-red-100 dark:border-red-900/30 rounded-xl p-4 flex gap-3">
                  <AlertTriangle className="text-red-600 dark:text-red-400 shrink-0 mt-0.5" size={18} />
                  <div>
                    <h4 className="text-sm font-semibold text-red-900 dark:text-red-300">Danger Zone</h4>
                    <p className="text-xs text-red-700 dark:text-red-400 mt-1">
                      Changing these settings may cause Jarvis to lose connection to the brain. Ensure you have valid credentials.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );

      case 'notifications':
        return (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-300">
            <div className="bg-white dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700/50 rounded-2xl p-6 shadow-sm">
              <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-1">Notification Preferences</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">Control when and how Jarvis interrupts you.</p>

              <div className="space-y-3">
                {[
                  { title: 'System Notifications', desc: 'Allow Jarvis to send macOS system notifications', checked: true },
                  { title: 'Reminders', desc: 'Notify when set reminders are due', checked: true },
                  { title: 'Calendar Events', desc: 'Alert 5 minutes before meetings', checked: true },
                  { title: 'Background Tasks', desc: 'Notify when long-running tasks complete', checked: false },
                ].map((item, i) => (
                  <div key={i} className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800/50 rounded-xl border border-gray-100 dark:border-gray-700 hover:border-gray-200 dark:hover:border-gray-600 transition-colors">
                    <div>
                      <div className="text-sm font-medium text-gray-700 dark:text-gray-200">{item.title}</div>
                      <div className="text-xs text-gray-500">{item.desc}</div>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input type="checkbox" className="sr-only peer" defaultChecked={item.checked} />
                      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-cyan-300 dark:peer-focus:ring-cyan-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-cyan-600"></div>
                    </label>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );

      case 'about':
        return (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-300">
            <div className="bg-white dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700/50 rounded-2xl p-8 shadow-sm text-center">
              <div className="w-24 h-24 bg-gradient-to-tr from-cyan-500 to-purple-600 rounded-3xl mx-auto flex items-center justify-center shadow-lg shadow-cyan-500/30 mb-6">
                <Cpu className="text-white" size={48} />
              </div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Jarvis AI</h2>
              <p className="text-gray-500 dark:text-gray-400 mb-6">Your Personal Brain Extension</p>
              <span className="px-3 py-1 bg-cyan-50 dark:bg-cyan-900/30 text-cyan-600 dark:text-cyan-300 text-xs font-semibold rounded-full border border-cyan-100 dark:border-cyan-800">
                v5.5.0 Dev
              </span>

              <div className="max-w-sm mx-auto mt-10 space-y-4 text-left">
                <div className="flex justify-between py-3 border-b border-gray-100 dark:border-gray-800">
                  <span className="text-sm text-gray-500">Build Version</span>
                  <span className="text-sm font-mono font-medium text-gray-700 dark:text-gray-300">20260125.rc2</span>
                </div>
                <div className="flex justify-between py-3 border-b border-gray-100 dark:border-gray-800">
                  <span className="text-sm text-gray-500">Core Engine</span>
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Python 3.10 + Flask</span>
                </div>
                <div className="flex justify-between py-3 border-b border-gray-100 dark:border-gray-800">
                  <span className="text-sm text-gray-500">UI Framework</span>
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">React 19 + Tailwind</span>
                </div>
                <div className="flex justify-between py-3 border-b border-gray-100 dark:border-gray-800">
                  <span className="text-sm text-gray-500">Local DB</span>
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">SQLite + Chroma</span>
                </div>
              </div>

              <button className="mt-8 w-full max-w-xs px-4 py-2.5 bg-gray-900 dark:bg-white text-white dark:text-gray-900 rounded-xl font-medium hover:opacity-90 transition-opacity">
                Check for Updates
              </button>
              <p className="text-xs text-gray-400 mt-6">© 2026 Jarvis Team. All rights reserved.</p>
            </div>
          </div>
        );

      default:
        return <div className="p-6 text-gray-500">Section under construction</div>;
    }
  };

  return (
    <div className="h-full flex bg-gray-50 dark:bg-gray-950 overflow-hidden">
      {/* Settings Sidebar */}
      <div className="w-64 bg-white/50 dark:bg-gray-900/50 backdrop-blur-xl border-r border-gray-200 dark:border-gray-800 flex flex-col">
        <div className="p-6">
          <h2 className="text-xl font-bold text-gray-800 dark:text-gray-100">Settings</h2>
          <p className="text-xs text-gray-500 mt-1">Global configuration</p>
        </div>
        <nav className="flex-1 px-3 space-y-1 overflow-y-auto">
          {navItems.map((item) => {
            const isActive = activeSection === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveSection(item.id as SettingsSection)}
                className={`
                  w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all
                  ${isActive
                    ? 'bg-white dark:bg-gray-800 text-cyan-600 dark:text-cyan-400 shadow-sm ring-1 ring-gray-200 dark:ring-gray-700'
                    : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800/50'
                  }
                `}
              >
                <item.icon size={18} strokeWidth={isActive ? 2.5 : 2} />
                {item.label}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto p-8">
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white capitalize">
              {navItems.find(n => n.id === activeSection)?.label}
            </h2>
          </div>
          {renderContent()}
        </div>
      </div>
    </div>
  );
}
