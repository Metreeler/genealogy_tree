import { HttpClient } from '@angular/common/http';
import { Injectable, signal, WritableSignal } from '@angular/core';
import { Observable } from 'rxjs';
import { Person } from '../classes/person';
import { BackResponse } from '../classes/back-response';

@Injectable({
  providedIn: 'root'
})
export class TreeService {
  scale = signal(0.5)
  tree: WritableSignal<Person> = signal(new Person())

  constructor(private http: HttpClient) { 
    this.checkFields().subscribe({
      next: (data) => {
        console.log(data)
        this.setTree()
      },
      error: (err) => {
        console.log(err)
      }
    });
  }

  getTree(): Observable<Person> {
    return this.http.get<Person>("http://localhost:8000/family")
  }

  checkFields(): Observable<BackResponse> {
    const url = `http://localhost:8000/fields`
    return this.http.post<BackResponse>(url, new Person())
  }

  setTree():void {

    this.getTree().subscribe({
      next: (data) => {
        console.log("Tree loaded")
        this.tree.set(data);
      },
      error: (err) => {
        console.log(err)
      }
    });
  }
}
