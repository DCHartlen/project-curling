import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { Demo } from '../shared/demo';
import { DemoService } from '../shared/demo.service';

@Component({
  moduleId: module.id,
  selector: 'my-demos',
  templateUrl: './demos.component.html',
  styleUrls: [ './demos.component.css' ]
})

export class DemosComponent implements OnInit {
  selectedDemo: Demo;
  demos: Demo[];

  constructor(
    private router: Router,
    private demoService: DemoService) { }

  getDemos(): void {
    this.demoService.getDemos().then(demos => this.demos = demos);
  }

  ngOnInit(): void {
    this.getDemos();
  }

  onSelect(demo: Demo): void {
    this.selectedDemo = demo;
  }

  gotoDetail(): void {
    this.router.navigate(['/detail', this.selectedDemo.id]);
  }
}
