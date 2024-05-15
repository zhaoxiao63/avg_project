-- init.sql

CREATE DATABASE agv_traffic_db;

\connect agv_traffic_db;

CREATE TABLE agv_total_traffic (
    route_id TEXT,
    vehicle_type TEXT,
    total_count BIGINT,
    timestamp TIMESTAMP,
    record_date TEXT, -- timestamp字段的"yyyy-MM-dd"字符串格式
    PRIMARY KEY (route_id, record_date, vehicle_type)
);

CREATE TABLE agv_window_traffic (
    route_id TEXT,
    vehicle_type TEXT,
    total_count BIGINT,
    timestamp TIMESTAMP, -- 该字段为计算时的时间戳
    record_date TEXT, -- timestamp字段的"yyyy-MM-dd"字符串格式
    PRIMARY KEY (route_id, record_date, vehicle_type)
);

CREATE TABLE agv_poi_traffic (
    vehicle_id TEXT, -- 工厂中心位置1000km内小车编号
    vehicle_type TEXT, -- 工厂中心位置1000km内小车的类型
    distance BIGINT, -- 距离工厂中心位置的距离
    timestamp TIMESTAMP, -- 计算时的时间戳
    PRIMARY KEY (vehicle_id)
);

