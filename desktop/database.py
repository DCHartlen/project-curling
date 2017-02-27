from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from sqlalchemy.dialects.mysql import DOUBLE, SMALLINT, VARCHAR, TIMESTAMP, INTEGER
from sqlalchemy import Column, ForeignKey, create_engine

# Database information

PORT = 3306
DB_NAME = "curling"
URI = "mysql://{0}:{1}@{2}:{3}/{4}".format(USERNAME, PASSWORD, HOSTNAME, PORT, DB_NAME)

# Database connection engine
engine = create_engine(URI, echo=False)
Session = sessionmaker(bind=engine)

# Base class for table mappings
Base = declarative_base()


def save(table_object):
    """
    Saves to the database

    Args:
        table_object: an instance of a class that is mapped to a table in the database

    Throws:
        TypeError: if class type cannot be saved
        (Also SqlAlchemy errors)

    Returns:
        Primary key of saved object
    """
    session = Session()
    session.add(table_object)
    session.commit()

    if isinstance(table_object, DemoSession):
        return table_object.id
    elif isinstance(table_object, RawData) or isinstance(table_object, ProcessedData):
        return table_object.timestamp
    else:
        raise TypeError("Class type cannot be saved")


def save_all(table_objects):
    """
    Saves iterable of objects to the database

    Args:
        table_object: an iterable containing instances of classes that are mapped to a table in the database
    """
    session = Session()
    for table_object in table_objects:
        session.add(table_object)
    session.commit()


def print_instances(table_class):
    """
    Prints the attributes of each instance in table_class

    Example:
        > print_instances(DemoSession)
    """
    try:
        session = Session()
        for instance in session.query(table_class):
            print(vars(instance))

    except OperationalError as e:
        print(e)


class DemoSession(Base):
    __tablename__ = 'Session'

    def __init__(self,
                 first_name,
                 last_name=None,
                 notes=None,
                 email=None,
                 mean_maximum_force=None,
                 mean_sustained_force=None,
                 mean_brushing_force=None,
                 mean_stroke_rate=None):
        self.firstName = first_name
        self.lastName = last_name
        self.notes = notes
        self.email = email
        self.meanMaximumForce = mean_maximum_force
        self.meanSustainedFoce = mean_sustained_force
        self.meanBrushingForce = mean_brushing_force
        self.meanStrokeRate = mean_stroke_rate

    # Fields
    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    timestamp = Column(TIMESTAMP(), nullable=False)
    firstName = Column(VARCHAR(20), nullable=False)
    lastName = Column(VARCHAR(20))
    notes = Column(VARCHAR(255))
    email = Column(VARCHAR(50))
    meanMaximumForce = Column(DOUBLE())
    meanSustainedFoce = Column(DOUBLE())
    meanBrushingForce = Column(DOUBLE())
    meanStrokeRate = Column(DOUBLE())

    # Relationships
    rawData = relationship("RawData", back_populates="session")
    processedData = relationship("ProcessedData", back_populates="session")


class RawData(Base):
    __tablename__ = 'RawData'

    # Fields
    timestamp = Column(DOUBLE(), primary_key=True)
    sessionId = Column(INTEGER(), ForeignKey('Session.id'), nullable=False)
    headAx = Column(SMALLINT())
    headAy = Column(SMALLINT())
    headAz = Column(SMALLINT())
    handleImuAx = Column(SMALLINT())
    handleImuAy = Column(SMALLINT(), nullable=False)
    handleImuAz = Column(SMALLINT(), nullable=False)
    handleImuQx = Column(SMALLINT())
    handleImuQy = Column(SMALLINT())
    handleImuQz = Column(SMALLINT())
    strainGauge1 = Column(SMALLINT())
    strainGauge2 = Column(SMALLINT(), nullable=False)
    strainGauge3 = Column(SMALLINT(), nullable=False)
    strainGauge4 = Column(SMALLINT())
    vReference = Column(SMALLINT())

    # Relationships
    session = relationship("DemoSession", back_populates="rawData")


class ProcessedData(Base):
    __tablename__ = 'ProcessedData'

    def __init__(self,
                 timestamp,
                 session_id,
                 broom_angle,
                 vertical_force,
                 horizontal_force):
        self.timestamp = timestamp
        self.sessionId = session_id
        self.broomAngle = broom_angle
        self.verticalForce = vertical_force
        self.horizontalForce = horizontal_force

    # Fields
    timestamp = Column(DOUBLE(), primary_key=True)
    sessionId = Column(INTEGER(), ForeignKey('Session.id'), nullable=False)
    broomAngle = Column(DOUBLE(), nullable=False)
    verticalForce = Column(DOUBLE(), nullable=False)
    horizontalForce = Column(DOUBLE(), nullable=False)

    # Relationships
    session = relationship("DemoSession", back_populates="processedData")


# Create tables
Base.metadata.create_all(engine)


if __name__ == "__main__":
    # Example usage
    demo = DemoSession("Kermit")
    id = save(demo)
    print(id)
    raw_data = RawData(timestamp=23,
                       sessionId=id,
                       headAx=12,
                       headAy=13,
                       headAz=-2,
                       handleImuAx=2000,
                       handleImuAy=-2000,
                       handleImuAz=0,
                       handleImuQx=1212,
                       handleImuQy=1409,
                       handleImuQz=65,
                       strainGauge1=15,
                       strainGauge2=16,
                       strainGauge3=17,
                       strainGauge4=18,
                       vReference=2012)

    processed_data = ProcessedData(23, id, 12, 15, 18)
    print(save(raw_data))
    print(save(processed_data))
