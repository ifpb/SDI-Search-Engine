import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ServicesQueryComponent } from './services-query.component';

describe('ServicesQueryComponent', () => {
  let component: ServicesQueryComponent;
  let fixture: ComponentFixture<ServicesQueryComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ServicesQueryComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ServicesQueryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
