import { RetrieveService } from './../../services/retrieve.service';
import { FeatureTypeService } from './../../services/feature-type.service';
import { HttpErrorResponse } from '@angular/common/http';
import { QueryService } from './../../services/query.service';
import { FeatureType, CHOICE_LEVEL, RETRIEVE_TYPE, Resource } from './../../model/model';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-feature-type-query',
  templateUrl: './feature-type-query.component.html',
  styleUrls: ['./feature-type-query.component.scss']
})
export class FeatureTypeQueryComponent implements OnInit {

  // data
  resources: Resource[];

  features: FeatureType[];
  placeName: string = 'barro';
  startDate: string = '2015-01-01';
  endDate: string = '2015-12-31';
  blockedButton: boolean = false;
  error: string;
  choices: any[];

  // pagination
  page: number = 1;
  pageSize: number = 10;

  // log
  time: Date;

  constructor(
    private queryService: QueryService,
    private featureService: FeatureTypeService,
    private retrieveService: RetrieveService
  ) { }

  ngOnInit() {
    this.features = null;
    this.error = '';
  }

  search() {
    this.initSearch();
    const body = this.queryService.buildBody(this.placeName, this.startDate, this.endDate, '');
    console.log('body', body);
    this.featureService.find(body, false).then((resources: Resource[]) => {
      this.manageData(resources);
      this.afterRequest();
    }).catch((err: HttpErrorResponse) => {
      this.manageError(err);
    }).finally(() => {
      this.blockedButton = false;
    });
  }

  initSearch() {
    this.page = 1;
    if (this.features && this.features.length >= 0) {
      this.features = null;
    }
    this.placeName = this.placeName.trim();
    console.log(this.placeName);
    this.blockedButton = true;
    this.error = '';
    this.choices = null;
    this.time = new Date();
    console.log(this.time.getMinutes() + ' - ' + this.time.getSeconds() + ' - ' + this.time.getMilliseconds());
  }

  afterRequest() {
    this.time = new Date();
    console.log(this.time.getMinutes() + ' - ' + this.time.getSeconds() + ' - ' + this.time.getMilliseconds());
  }

  manageData(resources: Resource[]) {
    if (resources && resources.length > 0) {
      this.resources = resources;
      this.resources.sort((a, b) => b.similarity - a.similarity);
      const pageResources = this.resources.slice((this.page - 1) * this.pageSize, (this.page - 1) * this.pageSize + this.pageSize);
      const ids = [];
      pageResources.forEach(i => ids.push(i.id));
      this.retrieveService.retrieve(ids, RETRIEVE_TYPE.FEATURE_TYPE).then((features: FeatureType[]) => {
        resources.forEach(r => {
          features = features.map(f => {
            if (f.id === r.id) {
              return { ...f, similarity: r.similarity };
            }
            return f;
          });
        });
        this.features = features;
        this.features.sort((a, b) => b.similarity - a.similarity);
      }).catch(err => {
        console.log(err);
      });
    } else {
      this.features = [];
      this.resources = [];
    }
  }

  manageError(err: HttpErrorResponse) {
    console.log('falha no req', err);
    switch (err.status) {
      case 204:
        this.error = `Nenhum recurso foi encontrado vinculado ao local: ${this.placeName}!`;
        break;
      case 300:
        this.choices = err.error;
        this.error = `Mais de um recuso para ${this.placeName} foi encontrado, escolha um local listado abaixo.`;
        break;
      case 404:
        this.error = `Nenhuma localidade foi encontrada com a pesquisa: ${this.placeName}!`;
        break;
    }
  }

  selectChoice(item: any) {
    this.initSearch();
    const body = {
      place_name: item.id,
      start_date: this.startDate,
      end_date: this.endDate,
    };
    this.featureService.find(body, true).then((resources: Resource[]) => {
      this.manageData(resources);
      this.afterRequest();
    }).catch((err: HttpErrorResponse) => {
      this.manageError(err);
    }).finally(() => {
      this.blockedButton = false;
    });
  }

  async paginationChange(e) {
    const pageResources = this.resources.slice((e - 1) * this.pageSize, (e - 1) * this.pageSize + this.pageSize);
    const ids = [];
    pageResources.forEach(r => ids.push(r.id));
    this.retrieveService.retrieve(ids, RETRIEVE_TYPE.FEATURE_TYPE).then((features: FeatureType[]) => {
      pageResources.forEach(r => {
        features = features.map(f => {
          if (f.id === r.id) {
            return { ...f, similarity: r.similarity };
          }
          return f;
        });
      });
      this.features = features;
      this.features.sort((a, b) => b.similarity - a.similarity);
    })
      .catch(err => console.log(err));
  }

}
