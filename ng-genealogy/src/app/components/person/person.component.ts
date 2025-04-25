import { CommonModule } from '@angular/common';
import { Component, computed, input } from '@angular/core';
import { Person } from '../../classes/person';
import { PersonService } from '../../services/person.service';
import { TreeService } from '../../services/tree.service';

@Component({
  selector: 'app-person',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './person.component.html',
  styleUrl: './person.component.css',
})
export class PersonComponent {
  person = input.required<Person | undefined>();

  color = computed(() => {
    const person = this.person();
    const c = this.personService.colors();
    return (
      c.colors.find((color) => color.name == person?.name)?.color || '#3EF1B5'
    );
  });

  isVisible = computed(() => (this.treeService.scale() > 0.4 ? false : true));

  colorText = computed(() => {
    const color = this.color();
    const r = parseInt(color.substring(1, 3), 16);
    const g = parseInt(color.substring(3, 5), 16);
    const b = parseInt(color.substring(5, 7), 16);
    const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
    return luminance > 0.5 ? '#000000' : '#FFFFFF';
  });

  constructor(
    private personService: PersonService,
    private treeService: TreeService
  ) {}

  selectPerson(): void {
    if (!this.personService.isDragging()) {
      const person = this.person();

      this.personService.selectedPerson.set(person);
      document.documentElement.style.setProperty('--editor-width', '30vw');
    }
  }

  onRightClick(): boolean {
    const person = this.person();
    if (person?.id !== undefined) {
      this.personService.postUpdateParentVisibility(person.id).subscribe({
        next: (data) => {
          console.log(data);
          this.treeService.setTree();
          this.personService.selectedPerson.set(undefined);
          document.documentElement.style.setProperty('--editor-width', '0vw');
        },
        error: (err) => {
          console.log(err);
        },
      });
    }
    return false;
  }

  hasFather(): boolean {
    const person = this.person();
    if (person?.father?.id && person.show_parent) {
      return true;
    }
    return false;
  }

  hasMother(): boolean {
    const person = this.person();
    if (person?.mother?.id && person.show_parent) {
      return true;
    }
    return false;
  }
}
