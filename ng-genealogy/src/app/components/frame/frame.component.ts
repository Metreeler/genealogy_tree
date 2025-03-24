import { Component } from '@angular/core';
import { TreeComponent } from "../tree/tree.component";

@Component({
  selector: 'app-frame',
  standalone: true,
  imports: [TreeComponent],
  templateUrl: './frame.component.html',
  styleUrl: './frame.component.css'
})
export class FrameComponent {

}
