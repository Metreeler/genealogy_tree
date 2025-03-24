import { Component, HostListener, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DummyChildComponent } from "../dummy-child/dummy-child.component";

@Component({
  selector: 'app-dummy',
  standalone: true,
  imports: [
    CommonModule,
    DummyChildComponent
],
  templateUrl: './dummy.component.html',
  styleUrl: './dummy.component.css'
})
export class DummyComponent {
    scale = 1.0;
  
    @HostListener("window:mousewheel", ["$event"])
    onScroll(event: WheelEvent): void {
      if (event.deltaY > 0) {
        console.log("down")
        this.scale *= 1.05
        document.documentElement.style.setProperty("--scale-value", String(this.scale))
      } else if (event.deltaY < 0) {
        console.log("up")
        this.scale *= 0.95
        document.documentElement.style.setProperty("--scale-value", String(this.scale))
      }
    }
}
