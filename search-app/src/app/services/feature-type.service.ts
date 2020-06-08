import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class FeatureTypeService {

  API: string = environment.SEARCH_ENGINE_API;

  constructor(
    private http: HttpClient
  ) { }

  findeFeaturesTypes(placeName) {
    return this.http.post(this.API + '/find-place/level-feature-type/', { 'place_name': placeName }).toPromise();
  }

  find(filters, isPlaceId: boolean) {
    const url = isPlaceId ? '/find/feature-type?isPlaceId=true' : '/find/feature-type';
    return this.http.post(this.API + url, filters).toPromise();
  }
}
