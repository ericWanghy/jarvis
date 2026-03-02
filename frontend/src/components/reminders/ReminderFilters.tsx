import React from 'react';
import { List, LayoutList, LayoutGrid, Calendar as CalendarIcon, Plus, ChevronLeft, ChevronRight } from 'lucide-react';
import dayjs from 'dayjs';

interface ViewModeSwitcherProps {
  viewMode: 'list' | 'day' | 'week' | 'month';
  setViewMode: (mode: 'list' | 'day' | 'week' | 'month') => void;
  onNew: () => void;
}

export const ViewModeSwitcher: React.FC<ViewModeSwitcherProps> = ({ viewMode, setViewMode, onNew }) => {
  return (
    <div className="flex items-center gap-2">
      <div className="flex bg-gray-100 dark:bg-gray-800 p-1 rounded-lg border border-gray-200 dark:border-gray-700">
        {[
          { id: 'list', icon: List, label: '列表' },
          { id: 'day', icon: LayoutList, label: '日' },
          { id: 'week', icon: LayoutGrid, label: '周' },
          { id: 'month', icon: CalendarIcon, label: '月' }
        ].map((mode) => (
          <button
            key={mode.id}
            onClick={() => setViewMode(mode.id as any)}
            className={`
              flex items-center gap-1 px-3 py-1.5 rounded-md text-xs font-medium transition-all
              ${viewMode === mode.id
                ? 'bg-white dark:bg-gray-700 text-cyan-600 dark:text-cyan-400 shadow-sm'
                : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'}
            `}
          >
            <mode.icon size={14} />
            {mode.label}
          </button>
        ))}
      </div>
      <button
        onClick={onNew}
        className="flex items-center gap-2 px-4 py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg text-sm font-medium transition-colors shadow-lg shadow-cyan-500/20"
      >
        <Plus size={16} />
        新建
      </button>
    </div>
  );
};

interface DateNavigationProps {
  viewMode: 'list' | 'day' | 'week' | 'month';
  currentDate: Date;
  setCurrentDate: React.Dispatch<React.SetStateAction<Date>>;
}

export const DateNavigation: React.FC<DateNavigationProps> = ({ viewMode, currentDate, setCurrentDate }) => {
  if (viewMode === 'list') return null;

  return (
    <div className="flex justify-center items-center gap-4 bg-gray-50/50 dark:bg-gray-800/30 p-2 rounded-lg border border-gray-100 dark:border-gray-800">
      <button
        onClick={() => {
          if (viewMode === 'day') setCurrentDate(d => dayjs(d).subtract(1, 'day').toDate());
          if (viewMode === 'week') setCurrentDate(d => dayjs(d).subtract(1, 'week').toDate());
          if (viewMode === 'month') setCurrentDate(d => dayjs(d).subtract(1, 'month').toDate());
        }}
        className="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-full text-gray-500"
      >
        <ChevronLeft size={20} />
      </button>
      <span className="text-sm font-bold text-gray-700 dark:text-gray-200 w-48 text-center font-mono">
        {viewMode === 'day' && dayjs(currentDate).format('YYYY年 M月 D日')}
        {viewMode === 'week' && `${dayjs(currentDate).startOf('week').format('M月D日')} - ${dayjs(currentDate).endOf('week').format('M月D日')}`}
        {viewMode === 'month' && dayjs(currentDate).format('YYYY年 M月')}
      </span>
      <button
        onClick={() => {
          if (viewMode === 'day') setCurrentDate(d => dayjs(d).add(1, 'day').toDate());
          if (viewMode === 'week') setCurrentDate(d => dayjs(d).add(1, 'week').toDate());
          if (viewMode === 'month') setCurrentDate(d => dayjs(d).add(1, 'month').toDate());
        }}
        className="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-full text-gray-500"
      >
        <ChevronRight size={20} />
      </button>
      <button
        onClick={() => setCurrentDate(new Date())}
        className="text-xs font-medium text-cyan-600 hover:text-cyan-700 dark:text-cyan-400"
      >
        今天
      </button>
    </div>
  );
};
