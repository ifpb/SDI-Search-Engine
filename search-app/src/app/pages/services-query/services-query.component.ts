import { QueryService } from './../../services/query.service';
import { Component, OnInit } from '@angular/core';
import { ServiceResponse, Service } from 'src/app/model/service';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-services-query',
  templateUrl: './services-query.component.html',
  styleUrls: ['./services-query.component.scss']
})
export class ServicesQueryComponent implements OnInit {

  search: string = "";
  blocked_button: boolean = false;
  services: Service[];
  error: string;

  // pagination
  page: number = 1;
  pageSize: number = 10;

  // log
  time: Date;

  constructor(
    private queryService: QueryService
  ) { }

  ngOnInit() {
    this.services = null;
    this.error = '';
  }

  searchServices() {
    this.initSearch();
    this.queryService.findServices(this.search).then((services: any) => {
      this.services = services;
      this.services.sort((a, b) => {return b.similarity - a.similarity});
      this.afterRequest(services);
    }).catch((err: HttpErrorResponse) => {
      console.log('falha no req', err);
      switch (err.status) {
        case 204:
          this.error = `Nenhum recurso foi encontrado vinculado ao local: ${this.search}!`;
          break;
        case 300:
          this.error = `Mais de um recuso para 
          ${this.search} foi encontrado, aplicação ainda em desenvolvimento para oferecer a escolha.`;
          break;
        case 404:
          this.error = `Nenhuma localidade foi encontrada com a pesquisa: ${this.search}!`;
          break;
      }
    }).finally(() => {
      this.blocked_button = false;
    });
  }

  initSearch(){
    if(this.services && this.services.length > 0)
      this.services = null;
    console.log(this.search);
    this.error = '';
    this.blocked_button = true;
    this.time = new Date();
    console.log(this.time.getMinutes() + " - " + this.time.getSeconds());
  }

  afterRequest(services){
    console.log(services);
    this.time = new Date();
    console.log(this.time.getMinutes() + " - " + this.time.getSeconds())
  }

}
