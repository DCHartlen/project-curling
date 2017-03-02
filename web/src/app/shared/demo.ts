import { RawDataPoint } from './raw-data-point';
import { ProcessedDataPoint } from './processed-data-point';

export class Demo {
    id: number;
    timestamp: string;
    firstName: string;
    lastName: string;
    notes: string;
    email: string;
    meanMaximumForce: number;
    meanSustainedForce: number;
    meanBrushingForce: number;
    meanStrokeRate: number;

    rawData: RawDataPoint[];
    processedData: ProcessedDataPoint[];
}
