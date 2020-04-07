import { FeatureTypeQueryComponent } from './feature-type-query/feature-type-query.component';
import { ServicesQueryComponent } from './services-query/services-query.component';
import { HomeComponent } from './home/home.component';
import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

const routes: Routes = [
    {
      path: 'home',
      component: HomeComponent,
    },
    {
      path: 'service/query',
      component: ServicesQueryComponent
    },
    {
      path: 'feature-type/query',
      component: FeatureTypeQueryComponent
    },
    {
      path: '',
      redirectTo: 'home',
      pathMatch: 'full'
    },
    {
      path: '**',
      redirectTo: 'home'
    }
];

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    RouterModule.forChild(routes)
  ],
  exports: [RouterModule]
})
export class PagesRoutingModule { }
