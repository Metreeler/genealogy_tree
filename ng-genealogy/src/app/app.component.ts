import { Component } from '@angular/core';
import { DummyComponent } from "./components/dummy/dummy.component";
import { TreeComponent } from "./components/tree/tree.component";
import { FrameComponent } from './components/frame/frame.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    FrameComponent
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
