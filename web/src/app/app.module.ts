import { NgModule }       from '@angular/core';
import { BrowserModule }  from '@angular/platform-browser';
import { FormsModule }    from '@angular/forms';
import { HttpModule }     from '@angular/http';

import { ChartModule } from 'angular2-chartjs';

import { AppComponent }         from './app.component';
import { DashboardComponent }   from './dashboard/dashboard.component';
import { DemoDetailComponent }  from './demo-detail/demo-detail.component';
import { DemosComponent }       from './demos/demos.component';
import { DemoService }          from './shared/demo.service';

import { AppRoutingModule }     from './app-routing.module';

@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    HttpModule,
    ChartModule
  ],
  declarations: [
    AppComponent,
    DashboardComponent,
    DemoDetailComponent,
    DemosComponent
  ],
  providers: [ DemoService ],
  bootstrap: [ AppComponent ]
})

export class AppModule { }
