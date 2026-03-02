import { Card, Text, Badge, Group, ActionIcon, Menu, ThemeIcon, Box } from '@mantine/core';
import { IconDots, IconTrash, IconPencil, IconPin, IconBrain, IconCalendar } from '@tabler/icons-react';

interface Memory {
  id: number;
  content: string;
  category: string;
  created_at: string;
}

interface MemoryCardProps {
  memory: Memory;
  onDelete: (id: number) => void;
  onEdit: (memory: Memory) => void;
}

export function MemoryCard({ memory, onDelete, onEdit }: MemoryCardProps) {
  if (!memory) return null;

  const getCategoryColor = (cat: string) => {
    switch (cat) {
      case 'core': return 'violet';
      case 'preference': return 'indigo';
      case 'fact': return 'cyan';
      default: return 'gray';
    }
  };

  const color = getCategoryColor(memory.category);

  return (
    <Card
      padding="sm"
      radius="md"
      className="bg-white border border-slate-200 transition-all duration-300 hover:shadow-[0_8px_30px_rgba(0,0,0,0.04)] hover:-translate-y-1 group relative overflow-visible"
    >
      {/* Decorative bar - added pointer-events-none to prevent click interception */}
      <div className={`absolute top-0 left-0 w-1 h-full rounded-l-md bg-${color}-500/50 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none`}></div>

      <Group justify="space-between" mb="xs" align="start">
        <Group gap={6}>
            <ThemeIcon variant="light" color={color} size="sm" radius="sm">
                <IconBrain size={14} />
            </ThemeIcon>
            <Badge size="xs" variant="light" color={color} radius="sm" className="font-mono">
                {memory.category ? memory.category.toUpperCase() : 'GENERAL'}
            </Badge>
        </Group>

        <Menu position="bottom-end" shadow="md" width={140} radius="md">
          <Menu.Target>
            <ActionIcon variant="subtle" color="gray" size="xs" className="opacity-0 group-hover:opacity-100 transition-opacity">
              <IconDots size={16} />
            </ActionIcon>
          </Menu.Target>
          <Menu.Dropdown>
            <Menu.Item leftSection={<IconPencil size={14} />} onClick={() => onEdit(memory)}>
              编辑
            </Menu.Item>
            <Menu.Item leftSection={<IconPin size={14} />}>
              固定
            </Menu.Item>
            <Menu.Divider />
            <Menu.Item
              color="red"
              leftSection={<IconTrash size={14} />}
              onClick={(e) => {
                e.stopPropagation();
                onDelete(memory.id);
              }}
            >
              删除
            </Menu.Item>
          </Menu.Dropdown>
        </Menu>
      </Group>

      <Text size="xs" className="text-slate-700 leading-relaxed line-clamp-4 min-h-[4rem]">
        {memory.content}
      </Text>

      <Group justify="flex-end" mt="xs" gap={4}>
        <IconCalendar size={10} className="text-slate-400" />
        <Text size="10px" c="dimmed">
            {memory.created_at ? new Date(memory.created_at).toLocaleDateString() : 'Unknown'}
        </Text>
      </Group>
    </Card>
  );
}
