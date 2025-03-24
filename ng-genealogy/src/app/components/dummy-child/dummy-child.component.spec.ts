import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DummyChildComponent } from './dummy-child.component';

describe('DummyChildComponent', () => {
  let component: DummyChildComponent;
  let fixture: ComponentFixture<DummyChildComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DummyChildComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DummyChildComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
