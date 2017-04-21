import 'rxjs/add/operator/switchMap';
import { Component, OnInit }      from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Location, DatePipe }     from '@angular/common';

import { Demo }         from '../shared/demo';
import { DemoService }  from '../shared/demo.service';
import { ProcessedDataPoint } from '../shared/processed-data-point';

import {IMyOptions, IMyDateModel, IMyDate} from 'mydatepicker';

@Component({
    moduleId: module.id,
    selector: 'my-demo-detail',
    templateUrl: './demo-detail.component.html',
    styleUrls: ['./demo-detail.component.css']
})
export class DemoDetailComponent implements OnInit {
    demo: Demo;
    showDetails = false;

    selectedDate: Date = undefined;
    demos: Demo[];

    type: string = undefined;
    data: any = undefined;
    options: any = undefined;

    searchMessage = "";

    private datePickerOptions: IMyOptions = {
        dateFormat: 'mmm dd, yyyy',
        showClearDateBtn: false,
        editableDateField: false
    };
    private selDate: IMyDate = {
        year: 0, month: 0, day: 0
    };

    constructor(
        private demoService: DemoService,
        private route: ActivatedRoute,
        private location: Location,
        private datePipe: DatePipe
    ) {
        let now = new Date();
        this.selDate = {
            year: now.getFullYear(),
            month: now.getMonth() + 1,
            day: now.getDate()
        };
    }

    ngOnInit(): void {
        this.route.params
            .switchMap((params: Params) => this.demoService.getDemoById(+params['id']))
            .subscribe((demo: Demo) => {
                this.demo = demo;
                if (this.demo) {
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
                                display: true,
                                ticks: {
                                    autoskip: true,
                                    maxTicksLimit: 25
                                },
                                scaleLabel: {
                                    display: true,
                                    labelString: 'Point Number',
                                }
                            }],
                        }
                    };
                }
            });
        this.updateDemos(this.dateAsString(new Date()), this.dateAsString(this.addDays(new Date(), 1)));
    }

    updateDemos(start: string, end: string) {
        this.searchMessage = "Looking for demos...";
        this.demoService.getDemosByDate(start, end).then((demos: Demo[]) => {
            this.demos = demos;
            if (this.demos.length === 0) {
                this.searchMessage = "No demos found";
            } else {
                this.searchMessage = "";
            }
        });

    }

    onDateChanged(event: IMyDateModel) {
        this.selDate = event.date;
        if (this.selDate && event.jsdate) {
            this.updateDemos(this.dateAsString(event.jsdate), this.dateAsString(this.addDays(event.jsdate, 1)));
        }
    }

    dateAsString(date: Date) {
        return this.datePipe.transform(date, 'yyyy-MM-dd');
    }

    addDays(date: Date, days: number) {
        let result = new Date(date.valueOf());
        result.setDate(result.getDate() + days);
        return result;
    }

    goBack(): void {
        this.location.back();
    }
}
