import { Component, OnInit } from '@angular/core';
import { Demo } from '../shared/demo';
import { DemoService } from '../shared/demo.service';

@Component({
  moduleId: module.id,
  selector: 'my-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: [ './dashboard.component.css' ]
})
export class DashboardComponent implements OnInit{
  demos: Demo[] = [];

  constructor(private demoService: DemoService) { }

  ngOnInit(): void {
      this.demoService.getMostRecentDemos(3).then(demos => this.demos = demos);
  }
}
