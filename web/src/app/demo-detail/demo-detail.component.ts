import 'rxjs/add/operator/switchMap';
import { Component, OnInit }      from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Location }               from '@angular/common';

import { Demo }         from '../shared/demo';
import { DemoService }  from '../shared/demo.service';
@Component({
  moduleId: module.id,
  selector: 'my-demo-detail',
  templateUrl: './demo-detail.component.html',
  styleUrls: [ './demo-detail.component.css' ]
})
export class DemoDetailComponent implements OnInit {
  demo: Demo;
  showDetails = false;
  demos: Demo[];

  constructor(
    private demoService: DemoService,
    private route: ActivatedRoute,
    private location: Location
  ) {}

  public showDiv(): void {
      this.showDetails = true;
  }

  public reset(): void {
      this.showDetails = false;
  }

  public demoLink(id: number): string {
      return "detail/" + id;
  }

  ngOnInit(): void {
    this.route.params
      .switchMap((params: Params) => this.demoService.getDemoById(+params['id']))
        .subscribe(demo => {
            this.demo = demo;
        });

    this.demoService.getMostRecentDemos(10).then((demos: Demo[]) => this.demos = demos);
  }

  goBack(): void {
    this.location.back();
  }
}
