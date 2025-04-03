import { Injectable, InputSignal, Signal, signal, WritableSignal } from '@angular/core';
import { Colors } from '../classes/colors';
import { map, Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Person } from '../classes/person';
import { BackResponse } from '../classes/back-response';

@Injectable({
  providedIn: 'root'
})
export class PersonService {
  colors = signal<Colors>(new Colors())
  selectedPerson: WritableSignal<Person|undefined> = signal(undefined);
  isDragging = signal(false)
  maxId = signal(-1)
  cities: WritableSignal<String[]> = signal([])

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

  getCities(): Observable<String[]> {
    return this.http.get<String[]>("http://localhost:8000/cities")
  }

  getMaxId(): Observable<number> {
    return this.http.get<number>("http://localhost:8000/max-id")
  }

  postUpdatePerson(person: Person): Observable<BackResponse> {
    return this.http.post<BackResponse>("http://localhost:8000/update", person)
  }

  postUpdateParentVisibility(childId: number): Observable<BackResponse> {
    const url = `http://localhost:8000/parent-visibility/${childId}`
    return this.http.post<BackResponse>(url, {})
  }

  postAddParent(childId: number, parent: Person): Observable<BackResponse> {
    const url = `http://localhost:8000/parent/${childId}`
    return this.http.post<BackResponse>(url, parent)
  }
  
  deletePerson(id: number): Observable<BackResponse> {
    const url = `http://localhost:8000/person/${id}`
    return this.http.delete<BackResponse>(url)
  }
}