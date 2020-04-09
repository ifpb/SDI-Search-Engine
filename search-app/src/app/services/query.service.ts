import { environment } from './../../environments/environment';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { first } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class QueryService {

  API: string = environment.SEARCH_ENGINE_API;

  constructor(
    private http: HttpClient
  ) {}

  findServices(placeName){
    return this.http.post(this.API + '/find-place/level-service/', {'place-name': placeName}).toPromise();
  }

  findeFeaturesTypes(placeName){
    return this.http.post(this.API + '/find-place/level-feature-type/', {'place-name': placeName}).toPromise();
  }

  choicePlace(choice: any, level: string){
    return this.http.post(this.API + '/find-place/choice?level=' + level, {'choice': choice}).toPromise();
  }
}
