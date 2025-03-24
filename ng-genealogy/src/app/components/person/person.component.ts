import { Component, computed, ElementRef, input, Input, signal } from '@angular/core';
import { Person } from '../../classes/person';
import { CommonModule } from '@angular/common';
import { PersonService } from '../../services/person.service';
import { Colors } from '../../classes/colors';
import { TreeService } from '../../services/tree.service';

@Component({
  selector: 'app-person',
  standalone: true,
  imports: [
    CommonModule
  ],
  templateUrl: './person.component.html',
  styleUrl: './person.component.css'
})
export class PersonComponent{
  person = input.required<Person|undefined>();
  color = computed(() => {
    const person = this.person()
    const c = this.personService.colors()
    return (c.colors.find(color => color.name == person?.name)?.color || "#3EF1B5")
  });

  constructor(private personService: PersonService, private treeService: TreeService) {
  }

  getName():void {
    console.log("here");
  }

  hasFather():boolean {
    const person = this.person()
    if (person?.father?.id) {
      return true
    }
    return false
  }

  hasMother():boolean {
    const person = this.person()
    if (person?.mother?.id) {
      return true
    }
    return false
  }
}
