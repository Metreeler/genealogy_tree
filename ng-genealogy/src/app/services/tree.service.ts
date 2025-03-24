import { HttpClient } from '@angular/common/http';
import { Injectable, signal } from '@angular/core';
import { Observable } from 'rxjs';
import { Person } from '../classes/person';

@Injectable({
  providedIn: 'root'
})
export class TreeService {
  scale = 1.0

  constructor(private http: HttpClient) { 
  }

  getTree(): Observable<Person> {
    return this.http.get<Person>("http://localhost:8000/family")
  }
}
