import { Component } from '@angular/core';
import { FrameComponent } from './components/frame/frame.component';
import { PersonEditorComponent } from './components/person-editor/person-editor.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    FrameComponent,
    PersonEditorComponent
],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'ng-genealogy';
  testDummy = {
    name: "malo",
    father: {
      name: "papa",
      father: {
        name: "grand père",
        father: null,
        mother: null
      },
      mother: {
        name: "grand mère",
        father: null,
        mother: null
      }
    },
    mother: {
      name: "maman",
      father: {
        name: "papy",
        father: null,
        mother: null
      },
      mother: {
        name: "mamie",
        father: null,
        mother: {
          name: "grand mamie",
          father: null,
          mother: null
        }
      }
    }
  }
}
