import React, { useState, useEffect, useMemo } from 'react';
import {
  Plus,
  Search,
  Filter,
  Radar,
  Wrench,
  RefreshCw,
  Brain,
  Heart,
  List,
  Lightbulb,
  Database,
  Trash2,
  AlertTriangle,
  Edit2,
  X,
  HardDrive
} from 'lucide-react';
import { apiGet, apiPost, apiPut, apiDelete } from '../../api/client';

// Types
interface Memory {
  id: number;
  content: string;
  category: 'core' | 'preference' | 'fact' | 'general';
  created_at: string;
  updated_at: string;
}

export default function MemoriesPage() {
  const [memories, setMemories] = useState<Memory[]>([]);
  const [search, setSearch] = useState('');
  const [modalOpen, setModalOpen] = useState(false);
  const [newContent, setNewContent] = useState('');
  const [newCategory, setNewCategory] = useState('general');
  const [editingMemory, setEditingMemory] = useState<Memory | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isScanning, setIsScanning] = useState(false);
  const [isConsolidating, setIsConsolidating] = useState(false);

  // Delete Modal State
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [memoryToDelete, setMemoryToDelete] = useState<number | null>(null);

  const fetchMemories = async () => {
    setIsLoading(true);
    try {
      const data = await apiGet<Memory[]>('/api/v1/memories');
      setMemories(data);
    } catch (e) {
      console.error(e);
      setMemories([]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchMemories();
  }, []);

  // Stats Calculation
  const stats = useMemo(() => {
    const total = memories.length;
    const core = memories.filter(m => m.category === 'core').length;
    const preference = memories.filter(m => m.category === 'preference').length;
    const fact = memories.filter(m => m.category === 'fact').length;
    const general = memories.filter(m => m.category === 'general').length;
    return { total, core, preference, fact, general };
  }, [memories]);

  const handleSave = async () => {
    try {
      if (editingMemory) {
        // Update
        const updated = await apiPut<Memory>(`/api/v1/memories/${editingMemory.id}`, {
          content: newContent,
          category: newCategory
        });
        setMemories(memories.map(m => m.id === updated.id ? updated : m));
      } else {
        // Create
        await apiPost('/api/v1/memories', {
          content: newContent,
          category: newCategory
        });
        fetchMemories();
      }
      closeModal();
    } catch (e) {
      console.error(e);
    }
  };

  const closeModal = () => {
    setModalOpen(false);
    setEditingMemory(null);
    setNewContent('');
    setNewCategory('general');
  };

  const openEditModal = (memory: Memory) => {
    setEditingMemory(memory);
    setNewContent(memory.content);
    setNewCategory(memory.category);
    setModalOpen(true);
  };

  const handleScan = async () => {
    setIsScanning(true);
    try {
      const data = await apiPost<{ count: number }>('/api/v1/memories/scan');
      if (data.count > 0) {
        fetchMemories();
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsScanning(false);
    }
  };

  const handleConsolidate = async () => {
    setIsConsolidating(true);
    try {
      await apiPost('/api/v1/memories/consolidate');
      fetchMemories();
    } catch (e) {
      console.error(e);
    } finally {
      setIsConsolidating(false);
    }
  };

  // Open Delete Confirmation Modal
  const handleDeleteClick = (id: number) => {
    setMemoryToDelete(id);
    setDeleteModalOpen(true);
  };

  // Execute Delete
  const confirmDelete = async () => {
    if (!memoryToDelete) return;

    console.log(`[Memory] Deleting ID: ${memoryToDelete}`);

    try {
      await apiDelete(`/api/v1/memories/${memoryToDelete}`);

      setMemories(prev => prev.filter(m => m.id !== memoryToDelete));
      setDeleteModalOpen(false);
      setMemoryToDelete(null);
    } catch (e) {
      console.error('[Memory] Exception during delete:', e);
      alert(`删除失败: ${e instanceof Error ? e.message : String(e)}`);
    }
  };

  const filteredMemories = memories.filter(m =>
    m.content.toLowerCase().includes(search.toLowerCase()) ||
    m.category.toLowerCase().includes(search.toLowerCase())
  );

  // Stats Card Component
  const StatsCard = ({ title, value, icon: Icon, color, total }: any) => (
    <div className="bg-white dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200 dark:border-gray-700/50 rounded-xl p-4 flex items-center gap-4 shadow-sm hover:shadow-md transition-all duration-200">
      <div className={`p-3 rounded-lg ${color} bg-opacity-10 text-opacity-100`}>
        <Icon className={`w-6 h-6 ${color.replace('bg-', 'text-')}`} />
      </div>
      <div>
        <div className="text-2xl font-bold text-gray-800 dark:text-gray-100">{value}</div>
        <div className="text-xs text-gray-500 dark:text-gray-400 uppercase font-semibold tracking-wider">{title}</div>
      </div>
    </div>
  );

  return (
    <div className="h-full flex flex-col bg-gray-50 dark:bg-gray-950 overflow-hidden">
      {/* Header & Stats */}
      <div className="px-6 py-6 border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl sticky top-0 z-10">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-800 dark:text-gray-100 flex items-center gap-3">
              <Brain className="w-8 h-8 text-cyan-600 dark:text-cyan-500" />
              Memory Library
            </h1>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Manage Jarvis's long-term memory and preferences</p>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={handleScan}
              disabled={isScanning}
              className="flex items-center gap-2 px-4 py-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-50"
            >
              <Radar className={`w-4 h-4 ${isScanning ? 'animate-spin' : ''}`} />
              Scan
            </button>
            <button
              onClick={handleConsolidate}
              disabled={isConsolidating}
              className="flex items-center gap-2 px-4 py-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-50"
            >
              <Wrench className={`w-4 h-4 ${isConsolidating ? 'animate-spin' : ''}`} />
              Consolidate
            </button>
            <button
              onClick={() => {
                setEditingMemory(null);
                setNewContent('');
                setNewCategory('general');
                setModalOpen(true);
              }}
              className="flex items-center gap-2 px-4 py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg text-sm font-medium transition-colors shadow-lg shadow-cyan-500/20"
            >
              <Plus className="w-4 h-4" />
              Add Memory
            </button>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
          <StatsCard title="Total" value={stats.total} icon={Database} color="bg-indigo-500 text-indigo-600" total={0} />
          <StatsCard title="Core" value={stats.core} icon={Brain} color="bg-violet-500 text-violet-600" total={stats.total} />
          <StatsCard title="Preference" value={stats.preference} icon={Heart} color="bg-pink-500 text-pink-600" total={stats.total} />
          <StatsCard title="Fact" value={stats.fact} icon={List} color="bg-cyan-500 text-cyan-600" total={stats.total} />
          <StatsCard title="General" value={stats.general} icon={Lightbulb} color="bg-gray-500 text-gray-600" total={stats.total} />
        </div>

        {/* Search & Filter */}
        <div className="flex flex-col md:flex-row gap-4 items-center">
          <div className="relative w-full md:w-96">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search internal memories..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-cyan-500/20 focus:border-cyan-500 transition-all"
            />
          </div>
          <div className="flex items-center gap-2 w-full md:w-auto">
            <button className="flex items-center gap-2 px-3 py-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg text-sm text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
              <Filter className="w-4 h-4" />
              Filter Type
            </button>
            <button onClick={fetchMemories} className="p-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors ml-auto md:ml-0">
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-y-auto p-6">
        {/* External Context Section (RAG) */}
        <div className="mb-8">
          <h2 className="text-sm font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-4 flex items-center gap-2">
            <HardDrive className="w-4 h-4" />
            External Context (RAG)
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div className="bg-white dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700/50 rounded-xl p-4 flex items-center justify-between group hover:border-cyan-500/50 transition-colors cursor-pointer">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-blue-50 dark:bg-blue-900/20 flex items-center justify-center text-blue-600 dark:text-blue-400">
                  <Database className="w-5 h-5" />
                </div>
                <div>
                  <div className="font-semibold text-gray-800 dark:text-gray-200">Local Repo</div>
                  <div className="text-xs text-gray-500">/Users/wanghuiyong/code</div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-green-500"></span>
                <span className="text-xs text-gray-400">Synced</span>
              </div>
            </div>

            <button className="border border-dashed border-gray-300 dark:border-gray-700 rounded-xl p-4 flex flex-col items-center justify-center gap-2 text-gray-500 hover:text-cyan-600 hover:border-cyan-500 hover:bg-cyan-50/50 dark:hover:bg-cyan-900/10 transition-all group h-full min-h-[80px]">
              <Plus className="w-6 h-6 group-hover:scale-110 transition-transform" />
              <span className="text-sm font-medium">Add Source</span>
            </button>
          </div>
        </div>

        {/* Memory Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {isLoading ? (
            <div className="col-span-full flex flex-col items-center justify-center h-64 gap-4 text-gray-400">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-500"></div>
              <p className="text-sm">Loading memories...</p>
            </div>
          ) : filteredMemories.length === 0 ? (
            <div className="col-span-full flex flex-col items-center justify-center h-64 gap-4 text-gray-400">
              <Search className="w-12 h-12 opacity-20" />
              <p className="text-sm">No memories found</p>
            </div>
          ) : (
            filteredMemories.map(m => (
              <div key={m.id} className="bg-white dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700/50 rounded-xl p-5 flex flex-col hover:shadow-lg hover:border-cyan-500/30 transition-all duration-200 group h-full">
                <div className="flex justify-between items-start mb-3">
                  <span className={`
                    px-2 py-1 rounded-md text-[10px] font-bold uppercase tracking-wider
                    ${m.category === 'core' ? 'bg-violet-100 text-violet-700 dark:bg-violet-900/30 dark:text-violet-300' :
                      m.category === 'preference' ? 'bg-pink-100 text-pink-700 dark:bg-pink-900/30 dark:text-pink-300' :
                      m.category === 'fact' ? 'bg-cyan-100 text-cyan-700 dark:bg-cyan-900/30 dark:text-cyan-300' :
                      'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300'}
                  `}>
                    {m.category}
                  </span>
                  <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      onClick={() => openEditModal(m)}
                      className="p-1.5 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg text-gray-400 hover:text-cyan-600 transition-colors"
                    >
                      <Edit2 className="w-3.5 h-3.5" />
                    </button>
                    <button
                      onClick={() => handleDeleteClick(m.id)}
                      className="p-1.5 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg text-gray-400 hover:text-red-500 transition-colors"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-300 font-mono leading-relaxed line-clamp-4 mb-4 flex-1">
                  {m.content}
                </p>
                <div className="mt-auto pt-3 border-t border-gray-100 dark:border-gray-800 flex items-center justify-between text-xs text-gray-400 font-mono">
                  <span>ID: {m.id}</span>
                  <span>{new Date(m.created_at).toLocaleDateString()}</span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Add/Edit Modal Overlay */}
      {modalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/20 backdrop-blur-sm">
          <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-2xl w-full max-w-lg border border-gray-200 dark:border-gray-800 p-6 animate-in fade-in zoom-in duration-200">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-lg font-bold text-gray-800 dark:text-gray-100">
                {editingMemory ? 'Edit Memory' : 'Add New Memory'}
              </h3>
              <button onClick={closeModal} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Content</label>
                <textarea
                  value={newContent}
                  onChange={(e) => setNewContent(e.target.value)}
                  placeholder="e.g. I prefer dark mode for coding interfaces..."
                  className="w-full p-3 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl focus:ring-2 focus:ring-cyan-500/20 focus:border-cyan-500 outline-none transition-all min-h-[120px]"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Category</label>
                <select
                  value={newCategory}
                  onChange={(e) => setNewCategory(e.target.value)}
                  className="w-full p-3 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl focus:ring-2 focus:ring-cyan-500/20 focus:border-cyan-500 outline-none transition-all"
                >
                  <option value="general">General</option>
                  <option value="core">Core</option>
                  <option value="preference">Preference</option>
                  <option value="fact">Fact</option>
                </select>
              </div>

              <div className="flex justify-end gap-3 mt-6">
                <button
                  onClick={closeModal}
                  className="px-4 py-2 text-sm font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleSave}
                  className="px-4 py-2 text-sm font-medium text-white bg-cyan-600 hover:bg-cyan-700 rounded-lg shadow-lg shadow-cyan-500/20 transition-colors"
                >
                  Save Memory
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
                <AlertTriangle className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-gray-800 dark:text-gray-100 mb-2">Delete Memory?</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">
                  Are you sure you want to delete this memory? This action cannot be undone and Jarvis will lose access to this information.
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
                onClick={confirmDelete}
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
