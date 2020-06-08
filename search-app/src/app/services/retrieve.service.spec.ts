import { TestBed } from '@angular/core/testing';

import { RetrieveService } from './retrieve.service';

describe('RetrieveService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: RetrieveService = TestBed.get(RetrieveService);
    expect(service).toBeTruthy();
  });
});
