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

  findServices(body, isPlaceId: boolean) {
    const url = isPlaceId ? '/find/service?isPlaceId=true' : '/find/service';
    return this.http.post(this.API + url, body).toPromise();
  }
}
