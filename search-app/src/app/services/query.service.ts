import { environment } from './../../environments/environment';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class QueryService {

  API: string = environment.SEARCH_ENGINE_API;

  constructor(
    private http: HttpClient
  ) {
    this.http.post(this.API + '/find-place/level-service/', {'place-name': 'cajazeiras'}).subscribe(result => {
      console.log(result);
    })
  }
}
