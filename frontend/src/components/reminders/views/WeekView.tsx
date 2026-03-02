import React from 'react';
import dayjs from 'dayjs';
import { Reminder } from '../types';
import { TaskCard } from '../TaskCard';

interface WeekViewProps {
  reminders: Reminder[];
  currentDate: Date;
  onEdit: (reminder: Reminder) => void;
  onDelete: (id: number) => void;
  onComplete: (id: number, currentStatus: boolean) => void;
}

export const WeekView: React.FC<WeekViewProps> = ({ reminders, currentDate, onEdit, onDelete, onComplete }) => {
  const getDayReminders = (date: Date) => {
    return reminders.filter(r => {
      if (!r.due_date) return false;
      const rd = new Date(r.due_date);
      return rd.getDate() === date.getDate() &&
        rd.getMonth() === date.getMonth() &&
        rd.getFullYear() === date.getFullYear();
    }).sort((a, b) => new Date(a.due_date!).getTime() - new Date(b.due_date!).getTime());
  };

  const startOfWeek = dayjs(currentDate).startOf('week');
  const days = Array.from({ length: 7 }, (_, i) => startOfWeek.add(i, 'day'));

  return (
    <div className="grid grid-cols-7 gap-2 h-full min-h-[500px]">
      {days.map((day, i) => {
        const dayRems = getDayReminders(day.toDate());
        const isToday = day.isSame(dayjs(), 'day');
        return (
          <div key={i} className={`flex flex-col h-full rounded-xl border ${isToday ? 'bg-cyan-50/50 border-cyan-200 dark:bg-cyan-900/20 dark:border-cyan-800' : 'bg-gray-50/50 border-gray-200 dark:bg-gray-800/30 dark:border-gray-700'}`}>
            <div className={`p-2 text-center border-b ${isToday ? 'border-cyan-100 dark:border-cyan-800' : 'border-gray-100 dark:border-gray-700'}`}>
              <div className={`text-xs font-bold ${isToday ? 'text-cyan-600 dark:text-cyan-400' : 'text-gray-500 dark:text-gray-400'}`}>{day.format('ddd')}</div>
              <div className={`text-sm font-bold ${isToday ? 'text-cyan-600 dark:text-cyan-400' : 'text-gray-800 dark:text-gray-200'}`}>{day.format('D')}</div>
            </div>
            <div className="flex-1 p-2 overflow-y-auto">
              <div className="flex flex-col gap-2">
                {dayRems.map(r => (
                  <TaskCard
                    key={r.id}
                    reminder={r}
                    compact
                    onEdit={onEdit}
                    onDelete={onDelete}
                    onComplete={onComplete}
                  />
                ))}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
