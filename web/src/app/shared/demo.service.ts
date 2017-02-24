import { Injectable } from '@angular/core';
import { Demo } from './demo';
import { DEMOS } from './mock-demos';

@Injectable()
export class DemoService {
  getDemos(): Promise<Demo[]> {
    return Promise.resolve(DEMOS);
  }

  getDemo(id: number): Promise<Demo> {
    return this.getDemos()
               .then(demos => demos.find(demo => demo.id === id));
  }
}
