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
  ) { }

  buildBody(name: string, startDate: string, endDate: string, theme: string) {
    return {
      place_name: name,
      start_date: startDate,
      end_date: endDate,
      theme,
    };
  }

  choicePlace(choice: any, level: string) {
    return this.http.post(this.API + '/find-place/choice?level=' + level, { 'choice': choice }).toPromise();
  }
}
