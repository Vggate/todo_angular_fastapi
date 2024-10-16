import { Component, Input, output } from '@angular/core';
import { RouterLink } from '@angular/router';

import { take } from 'rxjs';

import { TaskItem } from '../task-item'
import { TaskService } from '../app.todo.service'
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-task-item',
  standalone: true,
  imports: [RouterLink, DatePipe],
  templateUrl: './task-item.component.html',
  styleUrl: './task-item.component.css'
})
export class TaskItemComponent {
  editable = false;
  removeTask = output<number>();
  toggleTask = output<TaskItem>();
  
  @Input() task!: TaskItem;

  constructor(private taskService: TaskService) {}

  removeTaskItem(taskId: number) {
    this.removeTask.emit(taskId);
  }

  toggleTaskItem() {
    this.task.completed = ! this.task.completed
    this.taskService.editTask(this.task).pipe(take(1)).subscribe((response) => {
      console.log(response)
    })
  }
}