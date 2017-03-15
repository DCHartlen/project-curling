import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DashboardComponent }   from './dashboard/dashboard.component';
import { DemosComponent }      from './demos/demos.component';
import { DemoDetailComponent }  from './demo-detail/demo-detail.component';

const routes: Routes = [
  { path: '', redirectTo: '/recent', pathMatch: 'full' },
  { path: 'recent',  component: DashboardComponent },
  { path: 'detail/:id', component: DemoDetailComponent },
  { path: 'all',     component: DemosComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})

export class AppRoutingModule {}
