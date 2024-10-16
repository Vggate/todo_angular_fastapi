import { Component, inject, Input } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

import { take } from 'rxjs';
import { HandlerService } from '../../services/handler.service';
import { TaskService } from '../app.todo.service';
import { TaskItem } from '../task-item';
import { Router } from '@angular/router';

@Component({
  selector: 'app-task-form',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './task-form.component.html',
  styleUrl: './task-form.component.css'
})
export class TaskFormComponent {
  task: TaskItem | null = null


  myTaskForm: FormGroup;

  @Input()
  set id(task_id: string) {
    const taskSearchParam = `task_id=${task_id}`
    if (task_id) {
      this.taskService.getTasks(taskSearchParam).pipe(take(1)).subscribe((response) => {
        this.task = response.records && response.records[0] || null
        if (this.task) {
          this.myTaskForm.disable()
          const task_val = this._parseTaskVal(this.task)
          this.myTaskForm.setValue(task_val)
        }
      });
    } else {
      this.task = null
      this.myTaskForm.reset()
    }
  }

  _parseTaskVal(task:TaskItem){
    /**
   * Fillter out some value of task should not put in Form.
   * @param {TaskItem} task - The task.
   * @returns {object} - The value to set in Form
   */
    return {
      title: task.title,
      description: task.description,
      due_date: task.due_date,
    }
  }

  eventHandler = inject(HandlerService)

  constructor(private taskService: TaskService, private router: Router) {
    this.myTaskForm = new FormGroup({
      title: new FormControl<string>('', Validators.required),
      description: new FormControl<string|null>(null),
      due_date: new FormControl<Date|null>(null),
    });
  }

  onSubmit() {
    const resource = {...this.myTaskForm.value };
    this.taskService.addTask(resource)
    .pipe(take(1)) // Memory leak
      .subscribe({
        next: response => {
          this.myTaskForm.reset();
          this.eventHandler.updateData();
          this.back();
        }, error: (error) => {
          console.log(error);
        }
      });
  }

  editTaskForm(){
    if (this.task) {
      this.myTaskForm.enable()
    }
  }

  saveTaskForm(){
    this.myTaskForm.disable()
    if (this.task) {
      const task_data = {
        ...this.myTaskForm.value,
        id: this.task.id
      }
      this.taskService.editTask(task_data).pipe(take(1)).subscribe(response => {
        if (response) {
          this.task = response
          this.eventHandler.updateData();
          this.back();
        }
      });

    }
  }
  
  back() {
    this.router.navigate(['']);
  }
}
