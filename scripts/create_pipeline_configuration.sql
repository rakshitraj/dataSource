CREATE SCHEMA IF NOT EXISTS data_store;

CREATE TABLE IF NOT EXISTS data_store.pipeline_configuration (
    pipeline_id   VARCHAR,
    key_conf           VARCHAR,
    value_conf         VARCHAR,
    created_time  TIMESTAMP,
    updated_time  TIMESTAMP,
    active_from   TIMESTAMP,
    active_until  TIMESTAMP
);