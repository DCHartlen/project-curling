import 'rxjs/add/operator/switchMap';
import { Component, OnInit }      from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Location }               from '@angular/common';

import { Demo }         from '../shared/demo';
import { DemoService }  from '../shared/demo.service';
import { ProcessedDataPoint } from '../shared/processed-data-point';


@Component({
    moduleId: module.id,
    selector: 'my-demo-detail',
    templateUrl: './demo-detail.component.html',
    styleUrls: ['./demo-detail.component.css']
})
export class DemoDetailComponent implements OnInit {
    demo: Demo;
    showDetails = false;
    demos: Demo[];

    type: string = undefined;
    data: any = undefined;
    options: any = undefined;


    constructor(
        private demoService: DemoService,
        private route: ActivatedRoute,
        private location: Location
    ) { }

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
            .subscribe((demo: Demo) => {
                this.demo = demo;
                this.type = 'line';
                this.data = {
                    labels: this.demo.processedData.map(function (point, index) {
                        return index.toString();
                    }),
                    datasets: [
                        {
                            label: this.demo.firstName,
                            data: this.demo.processedData.map(function (point: ProcessedDataPoint) {
                                return point.verticalForce;
                            }),
                            fill: true,
                            lineTension: 0.1,
                            backgroundColor: "rgba(75,192,192,0.4)",
                            borderColor: "rgba(75,192,192,1)",
                            borderCapStyle: 'butt',
                            borderDash: [],
                            borderDashOffset: 0.0,
                            borderJoinStyle: 'miter',
                            pointBorderColor: "rgba(75,192,192,1)",
                            pointBackgroundColor: "#fff",
                            pointBorderWidth: 1,
                            pointHoverRadius: 5,
                            pointHoverBackgroundColor: "rgba(75,192,192,1)",
                            pointHoverBorderColor: "rgba(220,220,220,1)",
                            pointHoverBorderWidth: 2,
                            pointRadius: 1,
                            pointHitRadius: 10,
                            spanGaps: false
                        }
                    ]
                };
                this.options = {
                    responsive: true,
                    maintainAspectRatio: false,
                    scaleShowLabels: false,
                    scales: {
                        yAxes: [{
                            scaleLabel: {
                                display: true,
                                labelString: 'Brushing Force (kg)'
                            }
                        }],
                        xAxes: [{
                            display: false,
                            scaleLabel: {
                                display: true,
                                labelString: 'Point Number',
                            }
                        }],
                    }
                };
            });

        this.demoService.getMostRecentDemos(10).then((demos: Demo[]) => this.demos = demos);
    }

    goBack(): void {
        this.location.back();
    }
}
