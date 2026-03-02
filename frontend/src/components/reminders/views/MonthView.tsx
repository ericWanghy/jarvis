import React from 'react';
import dayjs from 'dayjs';
import { Reminder } from '../types';

interface MonthViewProps {
  reminders: Reminder[];
  currentDate: Date;
}

export const MonthView: React.FC<MonthViewProps> = ({ reminders, currentDate }) => {
  const getDayReminders = (date: Date) => {
    return reminders.filter(r => {
      if (!r.due_date) return false;
      const rd = new Date(r.due_date);
      return rd.getDate() === date.getDate() &&
        rd.getMonth() === date.getMonth() &&
        rd.getFullYear() === date.getFullYear();
    }).sort((a, b) => new Date(a.due_date!).getTime() - new Date(b.due_date!).getTime());
  };

  const startOfMonth = dayjs(currentDate).startOf('month');
  const startDay = startOfMonth.day(); // 0 (Sunday) to 6 (Saturday)
  const daysInMonth = startOfMonth.daysInMonth();

  // Generate calendar grid cells
  const cells = [];
  // Empty cells for previous month
  for (let i = 0; i < startDay; i++) {
    cells.push(<div key={`empty-${i}`} className="bg-gray-50/30 dark:bg-gray-900/30 border border-gray-100 dark:border-gray-800/50 min-h-[100px]"></div>);
  }
  // Days of current month
  for (let i = 1; i <= daysInMonth; i++) {
    const date = startOfMonth.date(i);
    const dayRems = getDayReminders(date.toDate());
    const isToday = date.isSame(dayjs(), 'day');

    cells.push(
      <div key={`day-${i}`} className={`border border-gray-200 dark:border-gray-700 p-2 min-h-[100px] flex flex-col gap-1 ${isToday ? 'bg-cyan-50/30 dark:bg-cyan-900/10' : 'bg-white dark:bg-gray-800/50'}`}>
        <div className="flex justify-between items-start">
          <span className={`text-sm font-medium w-6 h-6 flex items-center justify-center rounded-full ${isToday ? 'bg-cyan-600 text-white' : 'text-gray-700 dark:text-gray-300'}`}>
            {i}
          </span>
          {dayRems.length > 0 && (
            <span className="text-[10px] bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 px-1.5 rounded-full">
              {dayRems.length}
            </span>
          )}
        </div>
        <div className="flex flex-col gap-1 mt-1 overflow-y-auto max-h-[80px]">
          {dayRems.slice(0, 3).map(r => (
            <div key={r.id} className={`text-[10px] truncate px-1 py-0.5 rounded ${r.is_completed ? 'bg-gray-100 text-gray-400 line-through' : 'bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300'}`}>
              {r.title}
            </div>
          ))}
          {dayRems.length > 3 && (
            <div className="text-[10px] text-gray-400 pl-1">+{dayRems.length - 3} more</div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      <div className="grid grid-cols-7 mb-2">
        {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(d => (
          <div key={d} className="text-center text-xs font-bold text-gray-500 dark:text-gray-400 uppercase py-2">
            {d}
          </div>
        ))}
      </div>
      <div className="grid grid-cols-7 auto-rows-fr gap-px bg-gray-200 dark:bg-gray-700 border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden flex-1">
        {cells}
      </div>
    </div>
  );
};
