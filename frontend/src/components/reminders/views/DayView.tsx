import React from 'react';
import dayjs from 'dayjs';
import { Reminder } from '../types';
import { TaskCard } from '../TaskCard';

interface DayViewProps {
  reminders: Reminder[];
  currentDate: Date;
  onEdit: (reminder: Reminder) => void;
  onDelete: (id: number) => void;
  onComplete: (id: number, currentStatus: boolean) => void;
}

export const DayView: React.FC<DayViewProps> = ({ reminders, currentDate, onEdit, onDelete, onComplete }) => {
  const getDayReminders = (date: Date) => {
    return reminders.filter(r => {
      if (!r.due_date) return false;
      const rd = new Date(r.due_date);
      return rd.getDate() === date.getDate() &&
        rd.getMonth() === date.getMonth() &&
        rd.getFullYear() === date.getFullYear();
    }).sort((a, b) => new Date(a.due_date!).getTime() - new Date(b.due_date!).getTime());
  };

  const dayReminders = getDayReminders(currentDate);

  return (
    <div className="flex flex-col gap-4 py-4">
      <h2 className="text-lg font-bold text-gray-700 dark:text-gray-200 px-1">
        {dayjs(currentDate).format('YYYY年MM月DD日 dddd')}
      </h2>
      {dayReminders.length === 0 ? (
        <div className="text-center py-12 text-gray-400 dark:text-gray-500">今日无安排</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {dayReminders.map(r => (
            <TaskCard
              key={r.id}
              reminder={r}
              onEdit={onEdit}
              onDelete={onDelete}
              onComplete={onComplete}
            />
          ))}
        </div>
      )}
    </div>
  );
};
