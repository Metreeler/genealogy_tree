import { Component, computed, ElementRef, HostListener, Signal, signal, viewChild, ViewChild, WritableSignal } from '@angular/core';
import { PersonComponent } from '../person/person.component';
import { Person } from '../../classes/person';
import { TreeService } from '../../services/tree.service';
import { PersonService } from '../../services/person.service';

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
  
  persons: Signal<Person|undefined> = computed(() => {
    const tree = this.treeService.tree()
    return tree
  });
  mouseX = -1;
  mouseY = -1;

  treeFrame = viewChild<ElementRef<HTMLElement>>("treeframe")
  tree = viewChild<ElementRef<HTMLElement>>("tree")
  mouseDown = false
  mouseOver = false

  constructor(private treeService: TreeService, private personService: PersonService) {
    
  }

  @HostListener("window:mousewheel", ["$event"])
  onScroll(event: WheelEvent): void {
    if (this.mouseOver) {
      var scaleMultiplier = 1.0
      if (event.deltaY > 0) {
        // console.log("down")
        scaleMultiplier = 0.95
      } else if (event.deltaY < 0) {
        // console.log("up")
        scaleMultiplier = 1.05
        
      }
      this.treeService.scale.update(value => value * scaleMultiplier)
  
      document.documentElement.style.setProperty("--scale-value", String(this.treeService.scale()))
  
      const e = this.treeFrame();
      if (e) {
        e.nativeElement.scrollTo({
          top: (e.nativeElement.scrollTop * scaleMultiplier), 
          left: (e.nativeElement.scrollLeft * scaleMultiplier)
        })
      }
    }
  }

  @HostListener("mouseenter")
  onMouseEnter(): void {
    this.mouseOver = true
  }

  @HostListener("mouseleave")
  onMouseLeave(): void {
    this.mouseOver = false
  }

  getServiceFunction(): void {
    console.log(this.persons)
  }

  onMouseDown(event:MouseEvent): void {
    this.mouseDown = true
    this.mouseX = event.x
    this.mouseY = event.y
    this.personService.isDragging.set(false)
    // console.log("is being pressed")
  }

  onMouseUp(event:MouseEvent): void {
    this.mouseDown = false
    // console.log("is being released")
    
  }

  onMouseMove(event:MouseEvent): void {
    if (this.mouseDown) {
      this.personService.isDragging.set(true)
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
