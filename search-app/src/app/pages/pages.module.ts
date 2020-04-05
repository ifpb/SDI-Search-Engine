import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { BrowserModule } from '@angular/platform-browser';
import { PagesRoutingModule } from './pages-routing.module';
import { HomeComponent } from './home/home.component';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ServicesQueryComponent } from './services-query/services-query.component';
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    HomeComponent,
    ServicesQueryComponent
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
