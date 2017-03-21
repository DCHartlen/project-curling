import { Demo } from './demo';
import { RawDataPoint } from './raw-data-point';
import { ProcessedDataPoint } from './processed-data-point';

let rawPoints: RawDataPoint[] = [
    {
        timestamp: 12424,
        sessionId: 1,
        headAx: 50,
        headAy: 51,
        headAz: 52,
        handleImuAx: 60,
        handleImuAy: 61,
        handleImuAz: 62,
        handleImuQx: 31,
        handleImuQy: 32,
        handleImuQz: 33,
        strainGauge1: 1001,
        strainGauge2: 1002,
        strainGauge3: 1003,
        strainGauge4: 1004,
        vReference: 15
    },
    {
        timestamp: 12425,
        sessionId: 1,
        headAx: 53,
        headAy: 54,
        headAz: 55,
        handleImuAx: 63,
        handleImuAy: 64,
        handleImuAz: 65,
        handleImuQx: 33,
        handleImuQy: 34,
        handleImuQz: 35,
        strainGauge1: 2001,
        strainGauge2: 2002,
        strainGauge3: 2003,
        strainGauge4: 2004,
        vReference: 16
    }
];

let processedPoints: ProcessedDataPoint[] = [
    {
        timestamp: 12424,
        sessionId: 1,
        broomAngle: 30,
        verticalForce: 50,
        horizontalForce: 60
    },
    {
        timestamp: 12425,
        sessionId: 1,
        broomAngle: 30,
        verticalForce: 50,
        horizontalForce: 60
    }
];

export const DEMOS: Demo[] = [
    {
        id: 1,
        timestamp: '04-04-2012',
        firstName: 'Aleysha',
        lastName: null,
        notes: 'Notes1',
        email: null,
        meanMaximumForce: 32,
        meanSustainedForce: 52,
        meanBrushingForce: 40,
        meanStrokeRate: 25,
        rawData: rawPoints,
        processedData: processedPoints
    },
    {
        id: 2,
        timestamp: '04-04-2012',
        firstName: 'Aisha',
        lastName: 'Abawajy',
        notes: null,
        email: 'email@email.ca',
        meanMaximumForce: 121,
        meanSustainedForce: 122,
        meanBrushingForce: 123,
        meanStrokeRate: 44,
        rawData: rawPoints,
        processedData: processedPoints
    }
];
