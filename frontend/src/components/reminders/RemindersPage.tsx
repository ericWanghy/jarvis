import React from 'react';
import {
  Calendar as CalendarIcon,
  List,
  CheckCircle,
  AlertCircle,
  CalendarDays
} from 'lucide-react';
import 'dayjs/locale/zh-cn';
import dayjs from 'dayjs';

import { useReminders } from './useReminders';
import { StatsCard } from './StatsCard';
import { ReminderForm } from './ReminderForm';
import { DeleteModal } from './DeleteModal';
import { ViewModeSwitcher, DateNavigation } from './ReminderFilters';
import { ListView } from './views/ListView';
import { DayView } from './views/DayView';
import { WeekView } from './views/WeekView';
import { MonthView } from './views/MonthView';

dayjs.locale('zh-cn');

export default function RemindersPage() {
  const {
    viewMode, setViewMode,
    currentDate, setCurrentDate,
    reminders,
    isLoading,
    stats,
    modalOpen, setModalOpen,
    editingId,
    title, setTitle,
    date, setDate,
    time, setTime,
    recurrence, setRecurrence,
    deleteModalOpen, setDeleteModalOpen,
    handleSave,
    handleComplete,
    handleDeleteClick,
    confirmDelete,
    openEdit,
    openNew
  } = useReminders();

  return (
    <div className="h-full flex flex-col bg-gray-50 dark:bg-gray-950 overflow-hidden">
      {/* Header & Stats */}
      <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl sticky top-0 z-10 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
          <div>
            <h3 className="text-2xl font-bold text-gray-800 dark:text-gray-100 flex items-center gap-2">
              <CheckCircle className="w-8 h-8 text-cyan-600 dark:text-cyan-500" />
              日程管理
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">管理您的待办事项与提醒</p>
          </div>
          <ViewModeSwitcher
            viewMode={viewMode}
            setViewMode={setViewMode}
            onNew={openNew}
          />
        </div>

        {/* Stats Grid */}
        <div className="flex gap-4 overflow-x-auto pb-2 mb-2">
          <StatsCard title="总任务" value={stats.total} icon={List} color="bg-cyan-500 text-cyan-600" total={0} />
          <StatsCard title="今日待办" value={stats.pendingToday} icon={CalendarDays} color="bg-orange-500 text-orange-600" total={stats.total} />
          <StatsCard title="已过期" value={stats.overdue} icon={AlertCircle} color="bg-red-500 text-red-600" total={stats.total} />
          <StatsCard title="未来一周" value={stats.upcomingWeek} icon={CalendarIcon} color="bg-blue-500 text-blue-600" total={stats.total} />
          <StatsCard title="已完成" value={stats.completed} icon={CheckCircle} color="bg-teal-500 text-teal-600" total={stats.total} />
        </div>

        {/* Date Navigation */}
        <DateNavigation
          viewMode={viewMode}
          currentDate={currentDate}
          setCurrentDate={setCurrentDate}
        />
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6 bg-gray-50/50 dark:bg-gray-900/50">
        {isLoading && reminders.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-64 gap-4 text-gray-400">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-500"></div>
            <p className="text-sm">正在加载...</p>
          </div>
        ) : (
          <>
            {viewMode === 'list' && (
              <ListView
                reminders={reminders}
                onEdit={openEdit}
                onDelete={handleDeleteClick}
                onComplete={handleComplete}
              />
            )}
            {viewMode === 'day' && (
              <DayView
                reminders={reminders}
                currentDate={currentDate}
                onEdit={openEdit}
                onDelete={handleDeleteClick}
                onComplete={handleComplete}
              />
            )}
            {viewMode === 'week' && (
              <WeekView
                reminders={reminders}
                currentDate={currentDate}
                onEdit={openEdit}
                onDelete={handleDeleteClick}
                onComplete={handleComplete}
              />
            )}
            {viewMode === 'month' && (
              <MonthView
                reminders={reminders}
                currentDate={currentDate}
              />
            )}
          </>
        )}
      </div>

      {/* Edit Modal */}
      <ReminderForm
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        onSave={handleSave}
        editingId={editingId}
        title={title}
        setTitle={setTitle}
        date={date}
        setDate={setDate}
        time={time}
        setTime={setTime}
        recurrence={recurrence}
        setRecurrence={setRecurrence}
      />

      {/* Delete Confirmation Modal */}
      <DeleteModal
        isOpen={deleteModalOpen}
        onClose={() => setDeleteModalOpen(false)}
        onConfirm={confirmDelete}
      />
    </div>
  );
}
