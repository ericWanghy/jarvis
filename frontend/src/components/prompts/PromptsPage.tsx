import React, { useState, useEffect } from 'react';
import {
  Plus,
  Trash2,
  Save,
  RefreshCw,
  Folder,
  FileText,
  Search,
  Sparkles,
  AlertCircle,
  X,
  ChevronRight,
  ChevronDown,
  Terminal
} from 'lucide-react';
import Editor from '@monaco-editor/react';
import { apiGet, apiPost, apiDelete } from '../../api/client';

interface PromptTree {
  [folder: string]: string[];
}

export default function PromptsPage() {
  const [tree, setTree] = useState<PromptTree>({});
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [fileContent, setFileContent] = useState('');
  const [originalContent, setOriginalContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedFolders, setExpandedFolders] = useState<Record<string, boolean>>({});

  // Create Modal State
  const [createModalOpen, setCreateModalOpen] = useState(false);
  const [newFileName, setNewFileName] = useState('');
  const [newFileFolder, setNewFileFolder] = useState('intents');
  const [customFolder, setCustomFolder] = useState('');

  // Delete Modal State
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [fileToDelete, setFileToDelete] = useState<string | null>(null);

  useEffect(() => {
    fetchTree();
  }, []);

  const fetchTree = async () => {
    try {
      const data = await apiGet<PromptTree>('/api/v1/prompts');
      setTree(data);
      // Expand all folders by default
      const allExpanded = Object.keys(data).reduce((acc, key) => ({ ...acc, [key]: true }), {});
      setExpandedFolders(allExpanded);
    } catch (error) {
      console.error(error);
    }
  };

  const loadFile = async (path: string) => {
    if (fileContent !== originalContent && selectedFile) {
      if (!confirm('You have unsaved changes. Discard them?')) return;
    }

    setIsLoading(true);
    setSelectedFile(path);
    try {
      const data = await apiGet<{ content: string }>(`/api/v1/prompts/content?path=${path}`);
      setFileContent(data.content);
      setOriginalContent(data.content);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    if (!selectedFile) return;
    setIsSaving(true);
    try {
      await apiPost('/api/v1/prompts/content', { path: selectedFile, content: fileContent });
      setOriginalContent(fileContent);
    } catch (error) {
      console.error(error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleCreate = async () => {
    const folder = newFileFolder === 'custom' ? customFolder : newFileFolder;
    if (!folder || !newFileName) return;

    const path = `${folder}/${newFileName.endsWith('.md') ? newFileName : newFileName + '.md'}`;

    try {
      await apiPost('/api/v1/prompts/create', { path, content: '# New Prompt\n' });

      setCreateModalOpen(false);
      setNewFileName('');
      fetchTree();
      loadFile(path);
    } catch (error: any) {
      console.error(error);
    }
  };

  const handleDelete = async () => {
    if (!fileToDelete) return;
    try {
      await apiDelete(`/api/v1/prompts/delete?path=${fileToDelete}`);

      if (selectedFile === fileToDelete) {
        setSelectedFile(null);
        setFileContent('');
      }
      fetchTree();
    } catch (error) {
      console.error(error);
    } finally {
      setDeleteModalOpen(false);
      setFileToDelete(null);
    }
  };

  const toggleFolder = (folder: string) => {
    setExpandedFolders(prev => ({ ...prev, [folder]: !prev[folder] }));
  };

  const hasChanges = fileContent !== originalContent;

  // Filter tree based on search
  const filteredTree = Object.entries(tree).reduce((acc, [folder, files]) => {
    const filteredFiles = files.filter(f =>
      f.toLowerCase().includes(searchQuery.toLowerCase()) ||
      folder.toLowerCase().includes(searchQuery.toLowerCase())
    );
    if (filteredFiles.length > 0) {
      acc[folder] = filteredFiles;
    }
    return acc;
  }, {} as PromptTree);

  return (
    <div className="h-full flex bg-gray-50 dark:bg-gray-950 overflow-hidden">
      {/* Sidebar */}
      <div className="w-72 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 flex flex-col">
        <div className="p-4 border-b border-gray-200 dark:border-gray-800">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider flex items-center gap-2">
              <Terminal className="w-4 h-4" />
              Prompt Library
            </h2>
            <button
              onClick={() => setCreateModalOpen(true)}
              className="p-1.5 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg text-cyan-600 dark:text-cyan-400 transition-colors"
              title="New Prompt"
            >
              <Plus className="w-4 h-4" />
            </button>
          </div>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search prompts..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-4 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-cyan-500/20 focus:border-cyan-500 transition-all"
            />
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {Object.entries(filteredTree).map(([folder, files]) => (
            <div key={folder}>
              <button
                onClick={() => toggleFolder(folder)}
                className="w-full flex items-center gap-2 px-2 py-1.5 text-xs font-bold text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 uppercase tracking-wider transition-colors"
              >
                {expandedFolders[folder] ? <ChevronDown className="w-3 h-3" /> : <ChevronRight className="w-3 h-3" />}
                <Folder className="w-3.5 h-3.5" />
                {folder}
              </button>

              {expandedFolders[folder] && (
                <div className="ml-2 pl-2 border-l border-gray-200 dark:border-gray-800 mt-1 space-y-0.5">
                  {files.map(file => {
                    const path = `${folder}/${file}`;
                    const isActive = selectedFile === path;
                    return (
                      <div key={path} className="group relative">
                        <button
                          onClick={() => loadFile(path)}
                          className={`
                            w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-all text-left
                            ${isActive
                              ? 'bg-cyan-50 dark:bg-cyan-900/20 text-cyan-700 dark:text-cyan-300 font-medium'
                              : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'}
                          `}
                        >
                          <FileText className="w-4 h-4 shrink-0" />
                          <span className="truncate">{file}</span>
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            setFileToDelete(path);
                            setDeleteModalOpen(true);
                          }}
                          className="absolute right-2 top-1/2 -translate-y-1/2 p-1 text-gray-400 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Main Editor Area */}
      <div className="flex-1 flex flex-col min-w-0 bg-white dark:bg-gray-900">
        {selectedFile ? (
          <>
            {/* Toolbar */}
            <div className="h-14 border-b border-gray-200 dark:border-gray-800 flex items-center justify-between px-6 bg-white dark:bg-gray-900">
              <div className="flex items-center gap-3">
                <FileText className="w-5 h-5 text-gray-400" />
                <span className="font-medium text-gray-700 dark:text-gray-200">{selectedFile}</span>
                {hasChanges && (
                  <span className="px-2 py-0.5 bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400 text-xs rounded-full font-medium">
                    Unsaved
                  </span>
                )}
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => alert('Coming Soon: Evolution Engine')}
                  className="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-violet-600 dark:text-violet-400 hover:bg-violet-50 dark:hover:bg-violet-900/20 rounded-lg transition-colors"
                >
                  <Sparkles className="w-4 h-4" />
                  Evolve
                </button>
                <button
                  onClick={handleSave}
                  disabled={!hasChanges || isSaving}
                  className={`
                    flex items-center gap-2 px-4 py-1.5 text-sm font-medium rounded-lg transition-all shadow-sm
                    ${hasChanges
                      ? 'bg-cyan-600 hover:bg-cyan-500 text-white shadow-cyan-500/20'
                      : 'bg-gray-100 dark:bg-gray-800 text-gray-400 cursor-not-allowed'}
                  `}
                >
                  {isSaving ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
                  Save
                </button>
              </div>
            </div>

            {/* Editor */}
            <div className="flex-1 relative">
              {isLoading && (
                <div className="absolute inset-0 z-10 bg-white/50 dark:bg-black/50 backdrop-blur-sm flex items-center justify-center">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-500"></div>
                </div>
              )}
              <Editor
                height="100%"
                defaultLanguage="markdown"
                value={fileContent}
                onChange={(value) => setFileContent(value || '')}
                theme="vs-dark" // You might want to toggle this based on app theme
                options={{
                  minimap: { enabled: false },
                  fontSize: 14,
                  wordWrap: 'on',
                  padding: { top: 20 },
                  scrollBeyondLastLine: false,
                  fontFamily: 'JetBrains Mono, monospace',
                }}
              />
            </div>
          </>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center text-gray-400 dark:text-gray-600 bg-gray-50 dark:bg-gray-950/50">
            <FileText className="w-16 h-16 mb-4 opacity-20" strokeWidth={1} />
            <p className="text-sm">Select a prompt to edit</p>
          </div>
        )}
      </div>

      {/* Create Modal */}
      {createModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/20 backdrop-blur-sm">
          <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-2xl w-full max-w-md border border-gray-200 dark:border-gray-800 p-6 animate-in fade-in zoom-in duration-200">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-lg font-bold text-gray-800 dark:text-gray-100">Create New Prompt</h3>
              <button onClick={() => setCreateModalOpen(false)} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Folder</label>
                <select
                  value={newFileFolder}
                  onChange={(e) => setNewFileFolder(e.target.value)}
                  className="w-full p-2.5 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl focus:ring-2 focus:ring-cyan-500/20 focus:border-cyan-500 outline-none transition-all"
                >
                  {Object.keys(tree).map(folder => (
                    <option key={folder} value={folder}>{folder}</option>
                  ))}
                  <option value="custom">+ New Folder...</option>
                </select>
              </div>

              {newFileFolder === 'custom' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Folder Name</label>
                  <input
                    type="text"
                    placeholder="e.g., workflows"
                    value={customFolder}
                    onChange={(e) => setCustomFolder(e.target.value)}
                    className="w-full p-2.5 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl focus:ring-2 focus:ring-cyan-500/20 focus:border-cyan-500 outline-none transition-all"
                  />
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">File Name</label>
                <input
                  type="text"
                  placeholder="e.g., intent_coding.md"
                  value={newFileName}
                  onChange={(e) => setNewFileName(e.target.value)}
                  className="w-full p-2.5 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl focus:ring-2 focus:ring-cyan-500/20 focus:border-cyan-500 outline-none transition-all"
                  autoFocus
                />
              </div>

              <div className="flex justify-end gap-3 mt-6">
                <button
                  onClick={() => setCreateModalOpen(false)}
                  className="px-4 py-2 text-sm font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleCreate}
                  className="px-4 py-2 text-sm font-medium text-white bg-cyan-600 hover:bg-cyan-700 rounded-lg shadow-lg shadow-cyan-500/20 transition-colors"
                >
                  Create
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {deleteModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/20 backdrop-blur-sm">
          <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-2xl w-full max-w-md border border-gray-200 dark:border-gray-800 p-6 animate-in fade-in zoom-in duration-200">
            <div className="flex gap-4">
              <div className="w-12 h-12 rounded-full bg-red-100 dark:bg-red-900/20 flex items-center justify-center flex-shrink-0 text-red-600 dark:text-red-400">
                <AlertCircle className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-gray-800 dark:text-gray-100 mb-2">Delete Prompt?</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">
                  Are you sure you want to delete <b>{fileToDelete}</b>? This action cannot be undone.
                </p>
              </div>
            </div>
            <div className="flex justify-end gap-3 mt-6">
              <button
                onClick={() => setDeleteModalOpen(false)}
                className="px-4 py-2 text-sm font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleDelete}
                className="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg shadow-lg shadow-red-500/20 transition-colors flex items-center gap-2"
              >
                <Trash2 className="w-4 h-4" />
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
