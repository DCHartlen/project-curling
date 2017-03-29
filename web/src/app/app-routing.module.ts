import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DashboardComponent }   from './dashboard/dashboard.component';
import { DemosComponent }      from './demos/demos.component';
import { DemoDetailComponent }  from './demo-detail/demo-detail.component';

const routes: Routes = [
  { path: '', redirectTo: '/detail/-1', pathMatch: 'full' },
  { path: 'detail/:id', component: DemoDetailComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})

export class AppRoutingModule {}
