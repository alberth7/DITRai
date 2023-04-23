/********************************************************************************

********************************************************************************/

/*
CREATE TABLE Trafico(
   ID  
   macAddress
   -- direction="original"
    originalDirection
   --layer 3
    originalProtoum_Layer3
    originalProtoname_Layer3
    originalSRC_Layer3
    originalDST_Layer3
    --layer 4
    originalProtoum_Layer4
    originalProtoname_Layer4
    originalSPORT_Layer4
    originalDPORT_Layer4
    --counters
    originalPackets
    originalBytes

    -- direction = "reply"
    replyDirection
    --layer 3
    replyProtoum_Layer3
    replyProtoname_Layer3
    replySRC_Layer3
    replyDST_Layer3
    --layer 4
    replyProtoum_Layer4
    replyProtoname_Layer4
    replySPORT_Layer4
    replyDPORT_Layer4
    --counters
    replyPackets
    replyBytes

    -- direction="independent"
    independentDirection
    estado
    timeout
    mark
    use
    id_pakage
    dateTime  

*/



SELECT * FROM trafico WHERE originalSRC_Layer3 = ''



SELECT date(datetime),id, originaldirection, originalprotoum_layer3, originalprotoname_layer3, originalsrc_layer3, originaldst_layer3, originalprotoum_layer4, originalprotoname_layer4, originalsport_layer4, originaldport_layer4, originalpackets, originalbytes, replydirection, replyprotoum_layer3, replyprotoname_layer3, replysrc_layer3, replydst_layer3, replyprotoum_layer4, replyprotoname_layer4, replysport_layer4, replydport_layer4, replypackets, replybytes, independentdirection, estado, timeout, mark, use, id_pakage, datetime
	FROM public.trafico limit 10;
	
	
	
SELECT * FROM trafico WHERE date(datetime) = '2021-10-28'


SELECT DISTINCT(originalsrc_layer3) FROM trafico WHERE date(datetime) = '2021-10-28' 
-- 11 IPS

SELECT DISTINCT(originaldst_layer3) FROM trafico WHERE date(datetime) = '2021-10-28' 
-- 66 ips

SELECT * FROM trafico WHERE originaldst_layer3 = '200.89.75.197'


delete from  trafico


SELECT * FROM trafico limit 100


SELECT DISTINCT(originalSRC_Layer3) FROM trafico where macaddress = ''



SELECT id, macaddress, originaldirection, originalprotoum_layer3, originalprotoname_layer3, originalsrc_layer3, originaldst_layer3, originalprotoum_layer4, originalprotoname_layer4, originalsport_layer4, originaldport_layer4, originalpackets, originalbytes, replydirection, replyprotoum_layer3, replyprotoname_layer3, replysrc_layer3, replydst_layer3, replyprotoum_layer4, replyprotoname_layer4, replysport_layer4, replydport_layer4, replypackets, replybytes, independentdirection, estado, timeout, mark, use, id_pakage, datetime
	FROM public.trafico;

-- Numero de tuplas
SELECT COUNT(*) FROM trafico


-- macs
SELECT DISTINCT(macaddress) FROM trafico


-- IP, sin mac

SELECT DISTINCT(originalsrc_layer3) FROM trafico WHERE macaddress = ''
/*
"10.0.1.60"
"10.0.0.1"
"10.167.175.192"
"10.0.1.1"
"0.0.0.0"
"10.169.224.1"
"10.0.0.10"
"127.0.0.1"
"10.186.57.107"
*/

SELECT DISTINCT(macaddress) FROM trafico WHERE originalsrc_layer3 = '10.186.57.107'


--
SELECT * FROM trafico limit 10


--


SELECT id, originalbytes, replybytes, datetime,*
FROM trafico
WHERE originalsrc_layer3 in ('10.0.1.155')
or originaldst_layer3 in ('10.0.0.90')
or replysrc_layer3 in ('10.0.1.155')
or replydst_layer3 in ('10.0.0.90')


select distinct(id_pakage) from trafico

select id, original from trafico where id_pakage = '423875620'

truncate table trafico




select * from TraficoMobile

truncate table TraficoMobile;


select count(*) from TraficoMobile;

-- Table: public.mobile

-- DROP TABLE public.test;

CREATE TABLE IF NOT EXISTS public.test
(
ID_test  SERIAL PRIMARY KEY,
years integer,
cadena text
)

select * from test


insert into test(years, cadena) values(2020, 'test');
insert into test(years, cadena) values(2020, 'test');
insert into test(years, cadena) values(2020, 'test');


ALTER TABLE test
DROP COLUMN id_test;


select * from test


ALTER TABLE test
	ADD COLUMN id_test SERIAL PRIMARY KEY;



--- 2021.11.09
SELECT id, macaddress, originaldirection, originalprotoum_layer3, originalprotoname_layer3, originalsrc_layer3, originaldst_layer3, originalprotoum_layer4, originalprotoname_layer4, originalsport_layer4, originaldport_layer4, originalpackets, originalbytes, replydirection, replyprotoum_layer3, replyprotoname_layer3, replysrc_layer3, replydst_layer3, replyprotoum_layer4, replyprotoname_layer4, replysport_layer4, replydport_layer4, replypackets, replybytes, independentdirection, estado, timeout, mark, use, id_pakage, datetime
	FROM public.traficomobile;

select count(*) from traficomobile

select distinct(macaddress)
from traficomobile

select *
from traficomobile
where to_char(datetime,'HH24:MI') like '18:12'
limit 100

-- get hour of datetime

select extract(hour from timestamp '2001-02-16 20:38:40')

select to_char(datetime,'HH:MI') from trafico limit 1

select distinct(datetime)
from traficomobile
limit 100


select  count(*) from trafico


select * from trafico where originalsrc_layer3 = '10.0.0.155'

-- 2021.11.10
SELECT id, macaddress, originaldirection, originalprotoum_layer3, originalprotoname_layer3, originalsrc_layer3, originaldst_layer3, originalprotoum_layer4, originalprotoname_layer4, originalsport_layer4, originaldport_layer4, originalpackets, originalbytes, replydirection, replyprotoum_layer3, replyprotoname_layer3, replysrc_layer3, replydst_layer3, replyprotoum_layer4, replyprotoname_layer4, replysport_layer4, replydport_layer4, replypackets, replybytes, independentdirection, estado, timeout, mark, use, id_pakage, datetime
	FROM public.traficomobile;



SELECT COUNT(*) FROM traficomobile

SELECT DISTINCT(originaldst_layer3)
into tmpDSTLayer3
FROM traficomobile
-- 2209

SELECT DISTINCT(originaldst_layer3)
into tmpDSTLayer3lOCAL
FROM public.trafico202010
-- 1705


SELECT COUNT(*)
FROM tmpDSTLayer3
























