import { PagesRoutingModule } from './pages-routing.module';
import { HomeComponent } from './home/home.component';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ServicesQueryComponent } from './services-query/services-query.component';

@NgModule({
  declarations: [
    HomeComponent,
    ServicesQueryComponent
  ],
  imports: [
    CommonModule,
    PagesRoutingModule
  ]
})
export class PagesModule { }
