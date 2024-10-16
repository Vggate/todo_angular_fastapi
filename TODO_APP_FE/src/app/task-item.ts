export interface TaskItem {
  id: number;
  title: string;
  description?: string;
  completed?: boolean;
  due_date?: Date;
}

export interface CreateTaskItem {
  title: string;
  description?: string;
  due_date?: Date;
}

export interface TaskListResponse {
  length: number;
  records: TaskItem[];
}
