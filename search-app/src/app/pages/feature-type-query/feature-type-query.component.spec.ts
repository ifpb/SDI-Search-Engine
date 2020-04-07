import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FeatureTypeQueryComponent } from './feature-type-query.component';

describe('FeatureTypeQueryComponent', () => {
  let component: FeatureTypeQueryComponent;
  let fixture: ComponentFixture<FeatureTypeQueryComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FeatureTypeQueryComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FeatureTypeQueryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
