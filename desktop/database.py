import json
import requests


API_URL = "https://outreach.cs.dal.ca/curling/api"


# Method for saving a demo session
def saveDemoSession(session):
    r = requests.post(API_URL + "/insert-demo.php", data={ "session": session.as_json_string() }).json()
    if (r["error"]):
        raise RuntimeError("Couldn't save session")
    else:
        return r["sessionId"]


# Base class for objects that can be converted to JSON string
class JsonBase():
    def __init__(self):
        self.values = {}

    def add_if_not_none(self, key, value):
        if value is not None:
            self.values[key] = value

    def as_json_string(self):
        return json.dumps(self.values)


# Represents a raw data point
class RawDataPoint(JsonBase):
    def __init__(self,
                 timestamp,
                 session_id,
                 head_ax,
                 head_ay,
                 head_az,
                 handle_imu_ax,
                 handle_imu_ay,
                 handle_imu_az,
                 handle_imu_qx,
                 handle_imu_qy,
                 handle_imu_qz,
                 strain_gauge_1,
                 strain_gauge_2,
                 strain_gauge_3,
                 strain_gauge_4,
                 v_reference):
        JsonBase.__init__(self)

        self.values["timestamp"] = timestamp
        self.values["headAx"] = head_ax
        self.values["headAy"] = head_ay
        self.values["headAz"] = head_az
        self.values["handleImuAx"] = handle_imu_ax
        self.values["handleImuAy"] = handle_imu_ay
        self.values["handleImuAz"] = handle_imu_az
        self.values["handleImuQx"] = handle_imu_qx
        self.values["handleImuQy"] = handle_imu_qy
        self.values["handleImuQz"] = handle_imu_qz
        self.values["strainGauge1"] = strain_gauge_1
        self.values["strainGauge2"] = strain_gauge_2
        self.values["strainGauge3"] = strain_gauge_3
        self.values["strainGauge4"] = strain_gauge_4
        self.values["vReference"] = v_reference


# Represents a processed data point
class ProcessedDataPoint(JsonBase):
    def __init__(self,
                 timestamp,
                 session_id,
                 broom_angle,
                 vertical_force,
                 horizontal_force):
        JsonBase.__init__(self)

        self.values["timestamp"] = timestamp
        self.values["sessionId"] = session_id
        self.values["broomAngle"] = broom_angle
        self.values["verticalForce"] = vertical_force
        self.values["horizontalForce"] = horizontal_force


# Represents an entire demo session including raw and processed data as well as metadata
class Session(JsonBase):
    def __init__(self,
                 first_name,
                 raw_data=None,
                 processed_data=None,
                 last_name=None,
                 notes=None,
                 email=None,
                 mean_maximum_force=None,
                 mean_sustained_force=None,
                 mean_brushing_force=None,
                 mean_stroke_rate=None):
        JsonBase.__init__(self)

        self.values["firstName"] = first_name
        self.values["rawData"] = raw_data
        self.values["processedData"] = processed_data

        self.add_if_not_none("lastName", last_name)
        self.add_if_not_none("notes", notes)
        self.add_if_not_none("email", email)
        self.add_if_not_none("meanMaximumForce", mean_maximum_force)
        self.add_if_not_none("meanSustainedForce", mean_sustained_force)
        self.add_if_not_none("meanBrushingForce", mean_brushing_force)
        self.add_if_not_none("meanStrokeRate", mean_stroke_rate)

    def as_json_string(self):
        rawDataArray = self.values["rawData"]
        processedDataArray = self.values["processedData"]
        self.values["rawData"] = [x.values for x in rawDataArray]
        self.values["processedData"] = [x.values for x in processedDataArray]
        json_str = JsonBase.as_json_string(self)
        self.values["rawData"] = rawDataArray
        self.values["processedData"] = processedDataArray
        return json_str

    def save(self):
        return saveDemoSession(self)
    

if __name__ == "__main__":
    # Example usage
    processed_data_points = [
        ProcessedDataPoint(1, 1, 12, 13, 14), 
        ProcessedDataPoint(2, 1, 13, 14, 15)
    ]

    raw_data_points = [
        RawDataPoint(1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14),
        RawDataPoint(2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
    ]

    session = Session('Aleysha',
                      raw_data_points,
                      processed_data_points,
                      'Mullen',
                      'These are my notes',
                      'email@email.com',
                      10,
                      20,
                      30,
                      40)

    try:
        id = session.save()
        print('Success! Saved session with id: ' + str(id))
    except RuntimeError as error:
        print(error)
