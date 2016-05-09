from ora_adapter import Oracle



Oracle.try_execute("""
CREATE TABLE VehicleType (
    id INTEGER PRIMARY KEY,
    name VARCHAR2(30) UNIQUE NOT NULL
)
""")

Oracle.try_execute("""
CREATE TABLE CrashType (
    id INTEGER PRIMARY KEY,
    name VARCHAR2(30) UNIQUE NOT NULL
)
""")

Oracle.try_execute("""
CREATE TABLE VehicleFeatureType (
    id INTEGER PRIMARY KEY,
    name VARCHAR2(30) UNIQUE NOT NULL,
    variable_type INTEGER
)
""")

Oracle.try_execute("""
CREATE TABLE Person (
    id INTEGER PRIMARY KEY,
    is_organization NUMBER(1) DEFAULT 0,
    full_name VARCHAR2(60) NOT NULL,
    address VARCHAR2(60) NOT NULL,
    chief INTEGER
)
""")

Oracle.try_execute("""
CREATE TABLE Vehicle (
    id INTEGER PRIMARY KEY,
    vehicle_type INTEGER REFERENCES VehicleType(id) NOT NULL,
    reg_number VARCHAR2(10) NOT NULL,
    chief INTEGER REFERENCES Person(id) NOT NULL
)
""")

Oracle.try_execute("""
CREATE TABLE FeatureVehicleLinks (
    id INTEGER PRIMARY KEY,
    vehicle_id INTEGER REFERENCES Vehicle(id) NOT NULL ,
    vehicle_feature_type_id INTEGER REFERENCES VehicleFeatureType(id) NOT NULL,
    value_date DATE,
    data_str  VARCHAR2(100),
    data_int INTEGER,
    data_float FLOAT
)
""")

Oracle.try_execute("""
CREATE TABLE Crash (
    id INTEGER PRIMARY KEY,
    cdate DATE,
    crash_type INTEGER REFERENCES CrashType(id) NOT NULL,
    address VARCHAR2(100) NOT NULL,
    about VARCHAR2(1000) NOT NULL,
    victims INTEGER,
    damage_cost NUMBER(*, 2),
    cause VARCHAR2(100) NOT NULL,
    road_condition VARCHAR2(100) NOT NULL
)
""")

Oracle.try_execute("""
CREATE TABLE Searching (
    id INTEGER PRIMARY KEY,
    is_stolen NUMBER(1) DEFAULT 0,
    announced DATE NOT NULL,
    found DATE
)
""")

Oracle.try_execute("""
CREATE TABLE FreeRegNum (
    id INTEGER PRIMARY KEY,
    vehicle_type INTEGER REFERENCES VehicleType(id) NOT NULL,
    sta INTEGER NOT NULL,
    end INTEGER NOT NULL
)
""")


databases = [
    "VehicleType",
    "CrashType",
    "VehicleFeatureType",
    "Person",
    "Vehicle",
    "FeatureVehicleLinks",
    "Crash",
    "Searching",
    "FreeRegNum"
]

