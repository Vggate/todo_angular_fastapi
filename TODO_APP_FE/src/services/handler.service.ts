import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HandlerService {
  private _datachange = new Subject<void>();

  public datachange = this._datachange.asObservable()
  constructor() { }
  updateData() {
    this._datachange.next()
  }
}
