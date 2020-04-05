import { QueryService } from './../../services/query.service';
import { Component, OnInit } from '@angular/core';
import { ServiceResponse, Service } from 'src/app/model/service';

@Component({
  selector: 'app-services-query',
  templateUrl: './services-query.component.html',
  styleUrls: ['./services-query.component.scss']
})
export class ServicesQueryComponent implements OnInit {

  search: string = "";
  blocked_button: boolean = false;
  services: Service[];

  // pagination
  page: number = 1;
  pageSize: number = 10;

  constructor(
    private queryService: QueryService
  ) { }

  ngOnInit() {
    this.services = new Array();
  }

  searchServices() {
    console.log(this.search);
    this.blocked_button = true;
    this.queryService.findServices(this.search).then((services: Service[]) => {
      console.log(services);
      // services.forEach(s => {
      //   s.service.id = String(new Date().valueOf());
      // })
      this.services = services;
    }).catch(err => {
      console.log('falha no req', err);
    }).finally(() => {
      this.blocked_button = false;
      console.log('ae')
    })
  }

}
