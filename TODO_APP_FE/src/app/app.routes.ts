import { Routes } from '@angular/router';

import { TaskFormComponent } from './task-form/task-form.component';
import { TaskListComponent } from './task-list/task-list.component';


export const routes: Routes = [
  {
    path: '',
    title: 'Todo-App: List',
    component: TaskListComponent
  },
  {
    path: 'task-form/create',
    title: 'Todo-App: Create',
    component: TaskFormComponent
  },
  {
    path: 'task-form/:id',
    title: 'Todo-App: Form',
    component: TaskFormComponent
  },
];
