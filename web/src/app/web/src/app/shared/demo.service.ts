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

  getDemo(id: number): Promise<Demo> {
    return this.getDemos()
        .then(demos => {
            return demos.find(demo => demo.id === id);
        });
  }

  private extractData(res: Response) : Demo[] {
      let body = res.json();
      return body || {};
  }

  private handleError(error: Response | any) {
      console.log(error);
      return Observable.throw(error || "Database Error");
  }
}
