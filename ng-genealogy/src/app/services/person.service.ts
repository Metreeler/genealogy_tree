import { Injectable, signal } from '@angular/core';
import { Colors } from '../classes/colors';
import { map, Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Person } from '../classes/person';

@Injectable({
  providedIn: 'root'
})
export class PersonService {
  colors = signal<Colors>(new Colors())

  constructor(private http: HttpClient) {
    this.getColors().subscribe({
      next: (data) => {
        console.log("Colors loaded")
        
        this.colors.set(data);
      },
      error: (err) => {
        console.log(err)
      }
    }); 
  }

  getColors(): Observable<Colors> {
    return this.http.get<Colors>("http://localhost:8000/colors").pipe(map(data => Object.assign(new Colors(), data)))
  }
}