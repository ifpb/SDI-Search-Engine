import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { BrowserModule } from '@angular/platform-browser';
import { PagesRoutingModule } from './pages-routing.module';
import { HomeComponent } from './home/home.component';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ServicesQueryComponent } from './services-query/services-query.component';
import { FormsModule } from '@angular/forms';
import { FeatureTypeQueryComponent } from './feature-type-query/feature-type-query.component';

@NgModule({
  declarations: [
    HomeComponent,
    ServicesQueryComponent,
    FeatureTypeQueryComponent
  ],
  imports: [
    NgbModule.forRoot(),
    CommonModule,
    BrowserModule,
    FormsModule,
    PagesRoutingModule
  ]
})
export class PagesModule { }
