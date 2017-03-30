import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/toPromise';

import { Demo } from './demo';

@Injectable()
export class DemoService {

  private baseUrl = 'https://outreach.cs.dal.ca/curling/api';

  constructor(private http: Http) { }

  getDemos(): Promise<Demo[]> {
      return this.http.get(this.baseUrl + '/get-demos.php')
          .map(this.extractData)
          .toPromise()
          .catch(this.handleError);
  }

  getDemosByDate(startDate: string, endDate: string): Promise<Demo[]> {
      return this.http.get(this.baseUrl + '/get-demos.php?startDate=' + startDate + '&endDate=' + endDate)
          .map(this.extractData)
          .toPromise()
          .catch(this.handleError);
  }

  getMostRecentDemos(numberOfDemos: number): Promise<Demo[]> {
      return this.http.get(this.baseUrl + '/get-demos.php?mostRecent=' + numberOfDemos)
          .map(this.extractData)
          .toPromise()
          .catch(this.handleError);
  }

  getDemoById(id: number): Promise<Demo> {
      return this.http.get(this.baseUrl + '/get-demo.php?id=' + id)
          .map(this.extractData)
          .toPromise()
          .catch(this.handleError);
  }

  private extractData(res: Response) : Demo[] {
      let body = res.json();
      return body || {};
  }

  private handleError(error: Response | any) {
      console.log(error);
  }
}
