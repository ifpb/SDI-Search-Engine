import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ServiceService {

  API: string = environment.SEARCH_ENGINE_API;

  constructor(
    private http: HttpClient
  ) { }

  findServices(placeName) {
    return this.http.post(this.API + '/find-place/level-service/', { 'place-name': placeName }).toPromise();
  }
}
