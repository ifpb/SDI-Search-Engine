import { RetrieveService } from './../../services/retrieve.service';
import { ServiceService } from './../../services/service.service';
import { CHOICE_LEVEL, Resource, RETRIEVE_TYPE } from './../../model/model';
import { QueryService } from './../../services/query.service';
import { Component, OnInit } from '@angular/core';
import { ServiceResponse, Service } from 'src/app/model/model';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-services-query',
  templateUrl: './services-query.component.html',
  styleUrls: ['./services-query.component.scss']
})
export class ServicesQueryComponent implements OnInit {

  // data
  resources: Resource[];

  search: string = '';
  startDate: string = '2015-01-01';
  endDate: string = '2015-12-31';
  blockedButton: boolean = false;
  services: Service[];
  error: string;
  choices: any[];

  // pagination
  page: number = 1;
  pageSize: number = 10;

  // log
  time: Date;

  constructor(
    private queryService: QueryService,
    private serviceService: ServiceService,
    private retrieveService: RetrieveService,
  ) { }

  ngOnInit() {
    this.services = null;
    this.error = '';
  }

  searchServices() {
    this.initSearch();
    const body = this.queryService.buildBody(this.search, this.startDate, this.endDate, '');
    this.serviceService.findServices(body, false).then((resources: Resource[]) => {
      this.manageData(resources);
      this.afterRequest();
    })
      .catch((err: HttpErrorResponse) => {
        this.manageError(err);
      })
      .finally(() => {
        this.blockedButton = false;
      });
  }

  initSearch() {
    this.page = 1;
    if (this.services && this.services.length >= 0) {
      this.services = null;
    }
    console.log(this.search);
    this.error = '';
    this.blockedButton = true;
    this.choices = null;
    this.time = new Date();
    console.log(this.time.getMinutes() + ' - ' + this.time.getSeconds());
  }

  afterRequest() {
    this.time = new Date();
    console.log(this.time.getMinutes() + ' - ' + this.time.getSeconds())
  }

  manageData(resources: Resource[]) {
    if (resources && resources.length > 0) {
      this.resources = resources;
      this.resources.sort((a, b) => b.similarity - a.similarity);
      const pageResources = this.resources.slice((this.page - 1) * this.pageSize, (this.page - 1) * this.pageSize + this.pageSize);
      const ids = [];
      pageResources.forEach(i => ids.push(i.id));
      this.retrieveService.retrieve(ids, RETRIEVE_TYPE.SERVICE).then((services: Service[]) => {
        resources.forEach(r => {
          services = services.map(s => {
            if (s.id === r.id) {
              s.similarity = r.similarity;
            }
            return s;
          });
        });
        this.services = services;
        this.services.sort((a, b) => b.similarity - a.similarity);
      }).catch(err => console.log(err));
    } else {
      this.services = [];
      this.resources = [];
    }
  }

  manageError(err: HttpErrorResponse) {
    console.log('falha', err);
    switch (err.status) {
      case 204:
        this.error = `Nenhum recurso foi encontrado vinculado ao local: ${this.search}!`;
        break;
      case 300:
        this.choices = err.error;
        this.error = `Mais de um recuso para ${this.search} foi encontrado, escolha um local listado abaixo.`;
        break;
      case 404:
        this.error = `Nenhuma localidade foi encontrada com a pesquisa: ${this.search}!`;
        break;
    }
  }

  selectChoice(item: any) {
    this.initSearch();
    const body = {
      place_name: item.id,
      start_date: this.startDate,
      end_date: this.endDate,
      theme: ''
    };
    this.serviceService.findServices(body, true).then((resources: Resource[]) => {
      this.afterRequest();
      this.manageData(resources);
    }).catch((err: HttpErrorResponse) => {
      this.manageError(err);
    }).finally(() => {
      this.blockedButton = false;
    });
  }

}
