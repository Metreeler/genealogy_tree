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
}
