import { Component, ElementRef, HostListener, viewChild, ViewChild } from '@angular/core';
import { PersonComponent } from '../person/person.component';
import { Person } from '../../classes/person';
import { TreeService } from '../../services/tree.service';

@Component({
  selector: 'app-tree',
  standalone: true,
  imports: [ 
    PersonComponent,
    
  ],
  templateUrl: './tree.component.html',
  styleUrl: './tree.component.css'
})
export class TreeComponent {
  
  persons:Person|undefined;
  mouseX = -1;
  mouseY = -1;

  treeFrame = viewChild<ElementRef<HTMLElement>>("treeframe")
  tree = viewChild<ElementRef<HTMLElement>>("tree")
  mouseDown = false

  constructor(private service: TreeService) {
    this.service.getTree().subscribe({
      next: (data) => {
        console.log("Tree loaded")
        this.persons = data;
      },
      error: (err) => {
        console.log(err)
      }
    });
  }

  @HostListener("window:mousewheel", ["$event"])
  onScroll(event: WheelEvent): void {
    var scaleMultiplier = 1.0
    if (event.deltaY > 0) {
      // console.log("down")
      scaleMultiplier = 0.95
    } else if (event.deltaY < 0) {
      // console.log("up")
      scaleMultiplier = 1.05
      
    }
    this.service.scale *= scaleMultiplier

    document.documentElement.style.setProperty("--scale-value", String(this.service.scale))

    const e = this.treeFrame();
    if (e) {
      e.nativeElement.scrollTo({
        top: (e.nativeElement.scrollTop * scaleMultiplier), 
        left: (e.nativeElement.scrollLeft * scaleMultiplier)
      })
    }
  }

  getServiceFunction(): void {
    console.log(this.persons)
  }

  onMouseDown(event:MouseEvent): void {
    this.mouseDown = true
    this.mouseX = event.x
    this.mouseY = event.y
    // console.log("is being pressed")
  }

  onMouseUp(event:MouseEvent): void {
    this.mouseDown = false
    // console.log("is being released")
  }

  onMouseMove(event:MouseEvent): void {
    if (this.mouseDown) {
      const e = this.treeFrame();
      if (e) {
        e.nativeElement.scrollTo({
          top: e.nativeElement.scrollTop + this.mouseY - event.y, 
          left: e.nativeElement.scrollLeft + this.mouseX - event.x
        })
        this.mouseX = event.x
        this.mouseY = event.y
      }
    }
  }
}
