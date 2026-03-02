import { useState, useEffect, useMemo } from 'react';
import dayjs from 'dayjs';
import { Reminder } from './types';
import { apiGet, apiPost, apiPut, apiDelete } from '../../api/client';

export const useReminders = () => {
  const [viewMode, setViewMode] = useState<'list' | 'day' | 'week' | 'month'>('list');
  const [currentDate, setCurrentDate] = useState(new Date());
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // Edit/Create Modal State
  const [modalOpen, setModalOpen] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [title, setTitle] = useState('');
  const [date, setDate] = useState<string>('');
  const [time, setTime] = useState('');
  const [recurrence, setRecurrence] = useState('');

  // Delete Modal State
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [reminderToDelete, setReminderToDelete] = useState<number | null>(null);

  const fetchReminders = async () => {
    setIsLoading(true);
    try {
      const data = await apiGet<Reminder[]>('/api/v1/reminders/all?limit=500');
      if (Array.isArray(data)) {
        setReminders(data);
      } else {
        setReminders([]);
      }
    } catch (e) {
      console.error(e);
      setReminders([]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchReminders();
  }, []);

  const stats = useMemo(() => {
    const total = reminders.length;
    const now = dayjs();

    const pending = reminders.filter(r => !r.is_completed);
    const completed = reminders.filter(r => r.is_completed).length;

    const overdue = pending.filter(r => r.due_date && dayjs(r.due_date).isBefore(now)).length;

    const todayStart = now.startOf('day');
    const todayEnd = now.endOf('day');
    const pendingToday = pending.filter(r => {
      if (!r.due_date) return false;
      const d = dayjs(r.due_date);
      return d.isAfter(todayStart) && d.isBefore(todayEnd);
    }).length;

    const weekEnd = now.add(7, 'day');
    const upcomingWeek = pending.filter(r => {
      if (!r.due_date) return false;
      const d = dayjs(r.due_date);
      return d.isAfter(now) && d.isBefore(weekEnd);
    }).length;

    return { total, overdue, pendingToday, upcomingWeek, completed };
  }, [reminders]);

  const resetForm = () => {
    setEditingId(null);
    setTitle('');
    setDate(new Date().toISOString().split('T')[0]);
    setTime('');
    setRecurrence('');
  };

  const handleSave = async () => {
    try {
      let due_date = null;
      if (date) {
        const d = new Date(date);
        if (time) {
          const [h, m] = time.split(':').map(Number);
          d.setHours(h, m, 0);
        } else {
          d.setHours(9, 0, 0);
        }
        due_date = d.toISOString();
      }

      const payload = {
        title,
        due_date,
        recurrence_rule: recurrence || null,
        is_completed: false
      };

      if (editingId) {
        await apiPut(`/api/v1/reminders/${editingId}`, payload);
      } else {
        await apiPost('/api/v1/reminders', payload);
      }

      setModalOpen(false);
      resetForm();
      fetchReminders();
    } catch (e) {
      console.error(e);
    }
  };

  const handleComplete = async (id: number, currentStatus: boolean) => {
    try {
      // Optimistic update
      setReminders(prev => prev.map(r => r.id === id ? { ...r, is_completed: !currentStatus } : r));

      if (currentStatus) {
        // Undo complete (PUT)
        await apiPut(`/api/v1/reminders/${id}`, { is_completed: false });
      } else {
        // Complete (POST action)
        await apiPost(`/api/v1/reminders/${id}/complete`);
      }
      fetchReminders();
    } catch (e) {
      console.error(e);
      fetchReminders(); // Revert on error
    }
  };

  const handleDeleteClick = (id: number) => {
    setReminderToDelete(id);
    setDeleteModalOpen(true);
  };

  const confirmDelete = async () => {
    if (!reminderToDelete) return;
    try {
      setReminders(prev => prev.filter(r => r.id !== reminderToDelete));
      await apiDelete(`/api/v1/reminders/${reminderToDelete}`);
      setDeleteModalOpen(false);
      setReminderToDelete(null);
    } catch (e) {
      console.error(e);
      fetchReminders();
    }
  };

  const openEdit = (reminder: Reminder) => {
    setEditingId(reminder.id);
    setTitle(reminder.title);
    if (reminder.due_date) {
      const d = new Date(reminder.due_date);
      setDate(d.toISOString().split('T')[0]);
      setTime(`${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`);
    } else {
      setDate('');
      setTime('');
    }
    setRecurrence(reminder.recurrence_rule || '');
    setModalOpen(true);
  };

  const openNew = () => {
    resetForm();
    setModalOpen(true);
  };

  return {
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
  };
};
