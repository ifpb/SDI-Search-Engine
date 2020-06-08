import { TestBed } from '@angular/core/testing';

import { FeatureTypeService } from './feature-type.service';

describe('FeatureTypeService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: FeatureTypeService = TestBed.get(FeatureTypeService);
    expect(service).toBeTruthy();
  });
});
