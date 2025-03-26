import { HttpClient } from '@angular/common/http';
import { Injectable, signal, WritableSignal } from '@angular/core';
import { Observable } from 'rxjs';
import { Person } from '../classes/person';

@Injectable({
  providedIn: 'root'
})
export class TreeService {
  scale = signal(0.5)
  tree: WritableSignal<Person|undefined> = signal(undefined)

  constructor(private http: HttpClient) { 
    this.setTree()
  }

  getTree(): Observable<Person> {
    return this.http.get<Person>("http://localhost:8000/family")
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
