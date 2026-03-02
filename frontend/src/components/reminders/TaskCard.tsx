import React from 'react';
import { Clock, Repeat2, Edit2, Trash2, Check } from 'lucide-react';
import dayjs from 'dayjs';
import { Reminder } from './types';

interface TaskCardProps {
  reminder: Reminder;
  compact?: boolean;
  onEdit: (reminder: Reminder) => void;
  onDelete: (id: number) => void;
  onComplete: (id: number, currentStatus: boolean) => void;
}

export const TaskCard: React.FC<TaskCardProps> = ({ reminder, compact = false, onEdit, onDelete, onComplete }) => {
  const isOverdue = reminder.due_date && new Date(reminder.due_date) < new Date() && !reminder.is_completed;
  const isCompleted = reminder.is_completed;
  const isToday = reminder.due_date && dayjs(reminder.due_date).isSame(dayjs(), 'day');

  // Determine border color based on status
  let borderColor = 'border-l-cyan-400'; // Default future
  if (isCompleted) borderColor = 'border-l-gray-300';
  else if (isOverdue) borderColor = 'border-l-red-500';
  else if (isToday) borderColor = 'border-l-orange-400';

  return (
    <div
      className={`
        group relative overflow-hidden transition-all duration-200 rounded-xl border border-gray-200 dark:border-gray-700/50
        ${isCompleted ? 'bg-gray-50 dark:bg-gray-900/50 opacity-70' : 'bg-white dark:bg-gray-800/80 hover:shadow-md hover:-translate-y-0.5'}
        border-l-4 ${borderColor}
        ${compact ? 'p-2' : 'p-4'}
      `}
    >
      <div className={`flex flex-col ${compact ? 'gap-1' : 'gap-2'}`}>
        {/* Header: Time & Badges */}
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-2">
            {reminder.due_date ? (
              <span className={`
                px-2 py-0.5 rounded text-[10px] font-medium flex items-center gap-1
                ${isOverdue ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300' :
                  isCompleted ? 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400' :
                    isToday ? 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-300' :
                      'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300'}
              `}>
                <Clock size={10} />
                {compact
                  ? dayjs(reminder.due_date).format('HH:mm')
                  : dayjs(reminder.due_date).format('MM-DD HH:mm')}
              </span>
            ) : (
              <span className="px-2 py-0.5 rounded text-[10px] font-medium bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400">
                待办
              </span>
            )}
            {reminder.recurrence_rule && (
              <Repeat2 size={12} className="text-cyan-500" />
            )}
          </div>

          {/* Actions (Visible on Hover) */}
          <div className={`flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity ${compact ? 'hidden' : ''}`}>
            <button
              onClick={(e) => { e.stopPropagation(); onEdit(reminder); }}
              className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded text-blue-500"
            >
              <Edit2 size={14} />
            </button>
            <button
              onClick={(e) => { e.stopPropagation(); onDelete(reminder.id); }}
              className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded text-red-500"
            >
              <Trash2 size={14} />
            </button>
          </div>
        </div>

        {/* Content */}
        <div
          className={`
            font-medium text-gray-800 dark:text-gray-200 leading-snug line-clamp-2
            ${compact ? 'text-xs' : 'text-sm'}
            ${isCompleted ? 'line-through text-gray-400 dark:text-gray-500' : ''}
          `}
          title={reminder.title}
        >
          {reminder.title}
        </div>

        {/* Footer Action (Complete) */}
        {!compact && (
          <div className="flex justify-end mt-1">
            <button
              onClick={(e) => { e.stopPropagation(); onComplete(reminder.id, isCompleted); }}
              className={`
                w-full py-1 px-2 rounded text-xs font-medium flex items-center justify-center gap-1 transition-colors
                ${isCompleted
                  ? 'bg-gray-100 text-gray-600 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700'
                  : 'bg-green-50 text-green-600 hover:bg-green-100 dark:bg-green-900/20 dark:text-green-400 dark:hover:bg-green-900/30'}
              `}
            >
              {isCompleted ? <Repeat2 size={12} /> : <Check size={12} />}
              {isCompleted ? "撤销" : "完成"}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
