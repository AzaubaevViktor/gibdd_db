from ora_adapter import Oracle


Oracle.try_execute("""
CREATE TABLE VehicleType (
    id INTEGER PRIMARY KEY,
    name NVARCHAR2(30) UNIQUE NOT NULL
)
""")

Oracle.try_execute("""
CREATE TABLE CrashType (
    id INTEGER PRIMARY KEY,
    name NVARCHAR2(30) UNIQUE NOT NULL
)
""")

Oracle.try_execute("""
CREATE TABLE VehicleFeatureType (
    id INTEGER PRIMARY KEY,
    name NVARCHAR2(30) UNIQUE NOT NULL,
    variable_type INTEGER
)
""")

Oracle.try_execute("""
CREATE TABLE Person (
    id INTEGER PRIMARY KEY,
    is_organization NUMBER(1) DEFAULT 0,
    full_name NVARCHAR2(60) NOT NULL,
    address NVARCHAR2(60) NOT NULL,
    chief_id INTEGER
)
""")

Oracle.try_execute("""
CREATE TABLE Vehicle (
    id INTEGER PRIMARY KEY,
    vehicle_type INTEGER REFERENCES VehicleType(id) NOT NULL,
    reg_number NVARCHAR2(10) NOT NULL,
    chief_id INTEGER REFERENCES Person(id) NOT NULL
)
""")

Oracle.try_execute("""
CREATE TABLE VehicleFeatureLink (
    id INTEGER PRIMARY KEY,
    vehicle_id INTEGER REFERENCES Vehicle(id) NOT NULL ,
    vehicle_feature_type_id INTEGER REFERENCES VehicleFeatureType(id) NOT NULL,
    value_date DATE,
    data_str  NVARCHAR2(100),
    data_int INTEGER,
    data_float FLOAT
)
""")

Oracle.try_execute("""
CREATE TABLE VehicleTypeFeatureTypeLink (
    id INTEGER PRIMARY KEY,
    vehicle_type_id INTEGER REFERENCES VehicleType(id) NOT NULL ,
    vehicle_feature_type_id INTEGER REFERENCES VehicleFeatureType(id) NOT NULL
)
""")

Oracle.try_execute("""
CREATE TABLE Crash (
    id INTEGER PRIMARY KEY,
    cdate DATE,
    crash_type INTEGER REFERENCES CrashType(id) NOT NULL,
    address NVARCHAR2(100) NOT NULL,
    about NVARCHAR2(1000) NOT NULL,
    victims INTEGER,
    damage_cost NUMBER(*, 2),
    cause NVARCHAR2(100) NOT NULL,
    road_condition NVARCHAR2(100) NOT NULL
)
""")

Oracle.try_execute("""
CREATE TABLE Searching (
    id INTEGER PRIMARY KEY,
    vehicle_id INTEGER REFERENCES Vehicle(id) NOT NULL,
    is_stolen NUMBER(1) DEFAULT 0,
    announced DATE NOT NULL,
    found DATE
)
""")

Oracle.try_execute("""
CREATE TABLE FreeRegNum (
    id INTEGER PRIMARY KEY,
    vehicle_type_id INTEGER REFERENCES VehicleType(id) NOT NULL,
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
    "VehicleFeatureLink",
    "VehicleTypeFeatureTypeLink",
    "Crash",
    "Searching",
    "FreeRegNum"
]

