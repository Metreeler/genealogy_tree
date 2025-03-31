import { Component, computed, input, signal, Signal, WritableSignal } from '@angular/core';
import { Person } from '../../classes/person';
import { PersonService } from '../../services/person.service';
import { FormControl, FormsModule } from '@angular/forms';
import { TreeService } from '../../services/tree.service';

@Component({
  selector: 'app-person-editor',
  standalone: true,
  imports: [ 
    FormsModule
  ],
  templateUrl: './person-editor.component.html',
  styleUrl: './person-editor.component.css'
})
export class PersonEditorComponent {
  servicePerson: Signal<Person|undefined> = computed(() => {

    const person = this.personService.selectedPerson()

    this.person = person ? Object.assign({}, person) : new Person()
    this.person.father = undefined
    this.person.mother = undefined
    
    return this.personService.selectedPerson()}
  );

  deletionWanted = signal(true)

  person: Person = new Person();

  dataUpdated = signal(false)

  cities: WritableSignal<String[]> = signal([])

  constructor(private personService: PersonService, private treeService: TreeService) {    
    this.personService.getCities().subscribe({
      next: (data) => {
        console.log("Cities loaded");
        this.cities.set(data)
      },
      error: (err) => {
        console.log(err);
      }
    })
  }

  onClicked():void {
    this.personService.selectedPerson.set(undefined)
    document.documentElement.style.setProperty("--editor-width", "0vw")
    this.deletionWanted.set(true)
  }

  onSaveClicked(): void{
    this.saveData()
  }

  onDataUpdated(): void {
    this.dataUpdated.set(true)
  }

  onShowParent():void {
    this.onDataUpdated()
    this.saveData()
  }

  saveData(): void {
    if (this.dataUpdated()) {
      this.personService.postUpdatePerson(this.person).subscribe({
        next: (data) => {
          console.log(data)
          this.dataUpdated.set(false)
          this.treeService.setTree()
        },
        error: (err) => {
          console.log(err)
        }
      });
    }
  }

  onDeleteClicked(): void{
    this.deletionWanted.update(value => !value)
  }

  onSureDeleteClicked(): void {
    this.personService.deletePerson(this.person.id).subscribe({
      next: (data) => {
        console.log(data)
        this.treeService.setTree()
      },
      error: (err) => {
        console.log(err)
      }
    });
    this.deletionWanted.set(true)
    this.onClicked()
  }

  hasFather():boolean {
    const person = this.servicePerson()
    if (person?.father?.id) {
      return true
    }
    return false
  }

  hasMother():boolean {
    const person = this.servicePerson()
    if (person?.mother?.id) {
      return true
    }
    return false
  }

  onAddParentClicked(isFather:boolean):void {
    const parent = new Person()
    if (isFather) {
      parent.gender = "M"
    } else {
      parent.gender = "F"
    }
    parent.generation = this.person.generation + 1
    this.personService.getMaxId().subscribe({
      next: (data) => {
        parent.id = data + 1

        this.personService.postAddParent(this.person.id, parent).subscribe({
          next: (data) => {
            console.log(data)
            this.treeService.setTree()
            this.onClicked()
          },
          error: (err) => {
            console.log(err)
          }
        });
      },
      error: (err) => {
        console.log(err)
      }
    });
  }
}
