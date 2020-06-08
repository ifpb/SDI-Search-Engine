import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';
import { RETRIEVE_TYPE } from '../model/model';

@Injectable({
  providedIn: 'root'
})
export class RetrieveService {

  API: string = environment.SEARCH_ENGINE_API;

  constructor(
    private http: HttpClient
  ) { }

  retrieve(ids: string[], type: RETRIEVE_TYPE) {
    return this.http.post(this.API + `/retrieve/${type}`, ids).toPromise();
  }
}
