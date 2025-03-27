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
  isVisible = computed(() => this.treeService.scale() > 0.4 ? false : true);

  constructor(private personService: PersonService, private treeService: TreeService) {
  }

  selectPerson():void {
    if (!this.personService.isDragging()) {
      const person = this.person()
      
      this.personService.selectedPerson.set(person)
      document.documentElement.style.setProperty("--editor-width", "30vw")

      this.personService.getCities().subscribe({
        next: (data) => {
          console.log("Cities loaded")
          this.personService.cities.set(data)
        },
        error: (err) => {
          console.log(err)
        }
      });
      

      this.personService.getMaxId().subscribe({
        next: (data) => {
          console.log("Max Id loaded")
          this.personService.maxId.set(data)
        },
        error: (err) => {
          console.log(err)
        }
      });
    }
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
