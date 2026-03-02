import { useEffect, useRef } from 'react';
import { notifications } from '@mantine/notifications';
import { Button, Group, Text, Box, ThemeIcon, RingProgress } from '@mantine/core';
import { IconAlarm, IconCheck, IconX, IconClock, IconBellRinging } from '@tabler/icons-react';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
import 'dayjs/locale/zh-cn';

dayjs.extend(relativeTime);
dayjs.locale('zh-cn');

interface Reminder {
    id: number;
    title: string;
    due_date: string | null;
    is_completed: boolean;
}

export function ReminderPoller() {
    // Track notified reminders to prevent duplicate toasts
    const notifiedReminders = useRef<Set<number>>(new Set());

    const checkReminders = async () => {
        try {
            // Fetch pending reminders
            const res = await fetch('http://127.0.0.1:3721/api/v1/reminders/pending');
            if (!res.ok) return;
            const reminders: Reminder[] = await res.json();

            const now = new Date();

            reminders.forEach(reminder => {
                if (!reminder.due_date) return;

                const dueDate = new Date(reminder.due_date);
                const timeDiff = dueDate.getTime() - now.getTime();
                const isOverdue = timeDiff < 0;
                const isDueSoon = timeDiff > 0 && timeDiff <= 15 * 60 * 1000; // Within 15 mins

                // Only notify if overdue or due soon, and not already notified
                if ((isOverdue || isDueSoon) && !notifiedReminders.current.has(reminder.id)) {
                    showNotification(reminder, isOverdue);
                    notifiedReminders.current.add(reminder.id);
                }
            });
        } catch (e) {
            console.error("Failed to poll reminders:", e);
        }
    };

    const handleComplete = async (id: number, notificationId: string) => {
        try {
            await fetch(`http://127.0.0.1:3721/api/v1/reminders/${id}/complete`, { method: 'POST' });
            notifications.hide(notificationId);
            notifications.show({
                title: '已完成',
                message: '提醒已标记为完成',
                color: 'teal',
                icon: <IconCheck size={18} />,
                autoClose: 2000,
                withCloseButton: true,
                radius: "md",
                className: "shadow-md border border-teal-100"
            });
        } catch (e) {
            console.error(e);
        }
    };

    const showNotification = (reminder: Reminder, isOverdue: boolean) => {
        const notificationId = `reminder-${reminder.id}`;
        const dueDate = dayjs(reminder.due_date);
        const relativeStr = dueDate.fromNow();

        // Elegant Modern Style Configuration
        const config = isOverdue ? {
            color: 'red',
            icon: <IconAlarm size={20} />,
            title: '已过期',
            bg: 'bg-red-50',
            border: 'border-red-200',
            text: 'text-red-800'
        } : {
            color: 'indigo',
            icon: <IconBellRinging size={20} />,
            title: '即将到期',
            bg: 'bg-indigo-50',
            border: 'border-indigo-200',
            text: 'text-indigo-800'
        };

        notifications.show({
            id: notificationId,
            title: null, // Custom title in message
            message: (
                <div className="flex flex-col gap-3">
                    {/* Header */}
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <ThemeIcon
                                variant="light"
                                color={config.color}
                                size="md"
                                radius="md"
                            >
                                {config.icon}
                            </ThemeIcon>
                            <div>
                                <Text size="sm" fw={700} className={config.text}>
                                    {config.title}
                                </Text>
                                <Text size="xs" c="dimmed" fw={500}>
                                    {relativeStr}
                                </Text>
                            </div>
                        </div>
                    </div>

                    {/* Content */}
                    <div className={`p-3 rounded-lg ${config.bg} border ${config.border}`}>
                        <Text size="sm" fw={600} className="text-slate-800 leading-snug mb-1">
                            {reminder.title}
                        </Text>
                        <Group gap={4}>
                            <IconClock size={12} className="text-slate-500" />
                            <Text size="xs" c="dimmed" fw={500}>
                                {dueDate.format('YYYY-MM-DD HH:mm')}
                            </Text>
                        </Group>
                    </div>

                    {/* Actions */}
                    <Group gap="xs" grow>
                        <Button
                            size="xs"
                            variant="filled"
                            color="teal"
                            radius="md"
                            leftSection={<IconCheck size={14} />}
                            onClick={() => handleComplete(reminder.id, notificationId)}
                            className="shadow-sm hover:shadow transition-shadow"
                        >
                            完成
                        </Button>
                        <Button
                            size="xs"
                            variant="default"
                            color="gray"
                            radius="md"
                            leftSection={<IconX size={14} />}
                            onClick={() => notifications.hide(notificationId)}
                            className="border-slate-200 hover:bg-slate-50"
                        >
                            稍后
                        </Button>
                    </Group>
                </div>
            ),
            color: 'transparent', // Hide default color bar
            autoClose: false, // Persistent
            withCloseButton: false,
            radius: "lg",
            className: "shadow-xl border border-slate-100 !bg-white/95 backdrop-blur-sm",
            style: { padding: '12px' } // Custom padding
        });
    };

    useEffect(() => {
        // Initial check
        checkReminders();

        // Poll every minute
        const interval = setInterval(checkReminders, 60 * 1000);

        return () => clearInterval(interval);
    }, []);

    return null; // This component renders nothing visible
}
