import { Paper, Text, Group, Checkbox, Badge, ActionIcon, Menu, rem } from '@mantine/core';
import { IconClock, IconDots, IconTrash } from '@tabler/icons-react';

export interface Reminder {
  id: number;
  title: string;
  due_date: string | null;
  recurrence_rule: string | null;
  is_completed: boolean;
}

interface ReminderCardProps {
  reminder: Reminder;
  onComplete: (id: number) => void;
  onDelete: (id: number) => void;
  variant?: 'default' | 'overdue' | 'today';
}

export function ReminderCard({ reminder, onComplete, onDelete, variant = 'default' }: ReminderCardProps) {
  const isOverdue = variant === 'overdue';
  const isToday = variant === 'today';

  // Format date nicely
  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toLocaleString('zh-CN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
  };

  return (
    <Paper
      withBorder
      p="md"
      radius="md"
      className={`
        transition-all duration-200 hover:shadow-md hover:-translate-y-0.5
        ${isOverdue ? 'border-l-4 border-l-red-500 bg-red-50/30' : 'border-l-4 border-l-transparent hover:border-l-indigo-400'}
        ${isToday ? 'border-indigo-200 bg-indigo-50/20' : 'bg-white'}
      `}
    >
      <Group align="flex-start" wrap="nowrap" gap="sm">
        <Checkbox
          checked={reminder.is_completed}
          onChange={() => onComplete(reminder.id)}
          color={isOverdue ? 'red' : 'indigo'}
          radius="xl"
          size="sm"
          className="mt-1"
        />

        <div style={{ flex: 1 }}>
          <Text
            size="sm"
            fw={500}
            c={reminder.is_completed ? 'dimmed' : 'dark'}
            td={reminder.is_completed ? 'line-through' : undefined}
            className="leading-snug"
          >
            {reminder.title}
          </Text>

          <Group gap={6} mt={6}>
            {reminder.due_date && (
              <Badge
                variant={isOverdue ? "filled" : "light"}
                color={isOverdue ? "red" : "gray"}
                size="xs"
                radius="sm"
                leftSection={<IconClock style={{ width: rem(10), height: rem(10) }} />}
              >
                {formatDate(reminder.due_date)}
              </Badge>
            )}

            {reminder.recurrence_rule && (
              <Badge
                variant="dot"
                color="blue"
                size="xs"
                radius="sm"
              >
                循环
              </Badge>
            )}
          </Group>
        </div>

        <Menu position="bottom-end" shadow="sm" withinPortal>
          <Menu.Target>
            <ActionIcon variant="subtle" color="gray" size="sm">
              <IconDots style={{ width: rem(16), height: rem(16) }} />
            </ActionIcon>
          </Menu.Target>
          <Menu.Dropdown>
            <Menu.Item
              color="red"
              leftSection={<IconTrash style={{ width: rem(14), height: rem(14) }} />}
              onClick={() => onDelete(reminder.id)}
            >
              删除
            </Menu.Item>
          </Menu.Dropdown>
        </Menu>
      </Group>
    </Paper>
  );
}
