import { Component, computed, input, signal, Signal } from '@angular/core';
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

  constructor(private personService: PersonService, private treeService: TreeService) {    
  }

  onClicked():void {
    this.personService.selectedPerson.set(undefined)
    document.documentElement.style.setProperty("--editor-width", "0vw")
    this.deletionWanted.set(true)
  }

  onSaveClicked(): void{
    this.personService.postUpdatePerson(this.person).subscribe({
      next: (data) => {
        console.log(data)
        this.treeService.setTree()
      },
      error: (err) => {
        console.log(err)
      }
    });
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
  }
}
