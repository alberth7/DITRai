--CREATE DATABASE networktraffic ;

CREATE TABLE Trafico(
   ID  SERIAL PRIMARY KEY,
   macAddress                 TEXT,
   -- direction="original"
    originalDirection         TEXT,
   --layer 3
    originalProtoum_Layer3    TEXT,
    originalProtoname_Layer3  TEXT,
    originalSRC_Layer3        TEXT,
    originalDST_Layer3        TEXT,
    --layer 4
    originalProtoum_Layer4    TEXT,
    originalProtoname_Layer4  TEXT,
    originalSPORT_Layer4      TEXT,
    originalDPORT_Layer4      TEXT,
    --counters
    originalPackets           TEXT,
    originalBytes             TEXT,

    -- direction = "reply"
    replyDirection         TEXT,
    --layer 3
    replyProtoum_Layer3    TEXT,
    replyProtoname_Layer3  TEXT,
    replySRC_Layer3        TEXT,
    replyDST_Layer3        TEXT,
    --layer 4
    replyProtoum_Layer4    TEXT,
    replyProtoname_Layer4  TEXT,
    replySPORT_Layer4      TEXT,
    replyDPORT_Layer4      TEXT,
    --counters
    replyPackets           TEXT,
    replyBytes             TEXT,

    -- direction="independent"
    independentDirection TEXT,
    estado TEXT,
    timeout TEXT,
    mark    TEXT,
    use    TEXT,
    id_pakage      TEXT,
    assured TEXT,
    unreplied TEXT,
    dateTime  timestamp without time zone
);


-- Table location


CREATE TABLE UbicationIpPublic(
ip TEXT,
latitude TEXT,
longitude TEXT
);






