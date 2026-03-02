export interface Reminder {
  id: number;
  title: string;
  due_date: string | null;
  recurrence_rule: string | null;
  is_completed: boolean;
}
