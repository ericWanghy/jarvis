import { ActionIcon, Tooltip, ScrollArea, Text, Group, Button, Menu, Divider } from '@mantine/core';
import { IconMessagePlus, IconTrash, IconMessage, IconDotsVertical, IconEdit } from '@tabler/icons-react';
import { useChat } from '../../context/ChatContext';

export function SessionSidebar() {
  const { sessions, activeSessionId, loadSession, deleteSession } = useChat();

  const formatDate = (dateString: string) => {
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString([], { month: 'short', day: 'numeric' });
    } catch {
        return '';
    }
  };

  return (
    <div className="w-64 h-full flex flex-col bg-slate-50 border-r border-slate-200">
      {/* Session List */}
      <ScrollArea className="flex-1">
        <div className="p-2 space-y-1">
            {sessions.length === 0 && (
                <div className="text-center py-8 px-4">
                    <Text size="sm" c="dimmed">暂无历史对话</Text>
                </div>
            )}

            {sessions.map((session) => {
                const isActive = session.id === activeSessionId;
                return (
                    <div
                        key={session.id}
                        className={`
                            group relative flex items-center px-3 py-2.5 rounded-lg cursor-pointer transition-colors
                            ${isActive ? 'bg-white shadow-sm border border-slate-200' : 'hover:bg-slate-100 border border-transparent'}
                        `}
                        onClick={() => loadSession(session.id)}
                    >
                        <IconMessage
                            size={16}
                            className={`mr-3 shrink-0 ${isActive ? 'text-indigo-600' : 'text-slate-400'}`}
                        />
                        <div className="flex-1 min-w-0">
                            <Text size="sm" fw={isActive ? 500 : 400} truncate className="text-slate-700">
                                {session.title || '新对话'}
                            </Text>
                            <Text size="xs" c="dimmed" truncate>
                                {formatDate(session.created_at)}
                            </Text>
                        </div>

                        {/* Menu Actions */}
                        <div className="opacity-0 group-hover:opacity-100 transition-opacity" onClick={(e) => e.stopPropagation()}>
                            <Menu shadow="md" width={160} position="bottom-end">
                                <Menu.Target>
                                    <ActionIcon variant="subtle" color="gray" size="sm">
                                        <IconDotsVertical size={14} />
                                    </ActionIcon>
                                </Menu.Target>

                                <Menu.Dropdown>
                                    <Menu.Item leftSection={<IconEdit size={14} />}>
                                        重命名
                                    </Menu.Item>
                                    <Menu.Item
                                        color="red"
                                        leftSection={<IconTrash size={14} />}
                                        onClick={() => deleteSession(session.id)}
                                    >
                                        删除
                                    </Menu.Item>
                                </Menu.Dropdown>
                            </Menu>
                        </div>
                    </div>
                );
            })}
        </div>
      </ScrollArea>
    </div>
  );
}
