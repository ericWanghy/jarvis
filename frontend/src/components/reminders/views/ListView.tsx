import React, { useMemo } from 'react';
import { Inbox } from 'lucide-react';
import { Reminder } from '../types';
import { TaskCard } from '../TaskCard';

interface ListViewProps {
  reminders: Reminder[];
  onEdit: (reminder: Reminder) => void;
  onDelete: (id: number) => void;
  onComplete: (id: number, currentStatus: boolean) => void;
}

export const ListView: React.FC<ListViewProps> = ({ reminders, onEdit, onDelete, onComplete }) => {
  const filteredReminders = useMemo(() => {
    // Sort: Overdue first, then today, then future. Completed last.
    return [...reminders].sort((a, b) => {
      if (a.is_completed !== b.is_completed) return a.is_completed ? 1 : -1;
      const da = a.due_date ? new Date(a.due_date).getTime() : 9999999999999;
      const db = b.due_date ? new Date(b.due_date).getTime() : 9999999999999;
      return da - db;
    });
  }, [reminders]);

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {filteredReminders.map(r => (
        <TaskCard
          key={r.id}
          reminder={r}
          onEdit={onEdit}
          onDelete={onDelete}
          onComplete={onComplete}
        />
      ))}
      {filteredReminders.length === 0 && (
        <div className="col-span-full flex flex-col items-center justify-center py-20 text-gray-400">
          <Inbox size={48} strokeWidth={1} className="opacity-20 mb-2" />
          <p className="text-sm">暂无提醒</p>
        </div>
      )}
    </div>
  );
};
