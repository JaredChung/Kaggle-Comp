--Questions to Answers
---Analyise Each Category Seperately (Find any Trend)?
--Vehicle Theft Drops in recent years? Causes
--Segmentation of Categories into Blue_colar,White_colar and Other
--Analyise what hour of the day is Safest/Dangerous
--Temperature have a correlation to crime

/*
drop table if exists crime;

create table crime
(
	dates TIMESTAMP,
	category varchar(100),
	description varchar(200),
	DayOfWeek varchar(50),
	PdDistrict varchar(50),
	Resolution varchar(50),
	Address varchar(100),
	X float,
	Y float
	)
*/

select 
extract(year from dates),
extract(week from dates),
extract(hour from dates),
*,
case 
when category = 'Fraud' then 'White_collar'
when category = 'FORGERY/COUNTERFEITING' then 'White_collar'
when category = 'BAD CHECKS' then 'White_collar'
when category = 'EXTORTION' then 'White_collar'
when category = 'EMBEZZLEMENT' then 'White_collar'
when category = 'SUSPICIOUS OCC' then 'White_collar'
when category = 'BRIBERY' then 'White_collar'
when category = 'VANDALISM' then 'Blue_collar'
when category = 'LARCENY/THEFT' then 'Blue_collar'
when category = 'STOLEN PROPERTY' then 'Blue_collar'
when category = 'ROBBERY' then 'Blue_collar'
when category = 'DRIVING UNDER THE INFLUENCE' then 'Blue_collar'
when category = 'DISORDERLY CONDUCT' then 'Blue_collar'
when category = 'LIQUOR LAWS' then 'Blue_collar'
when category = 'VEHICLE THEFT' then 'Blue_collar'
when category = 'ASSAULT' then 'Blue_collar'
when category = 'KIDNAPPING' then 'Blue_collar'
when category = 'TRESPASS' then 'Blue_collar'
when category = 'ARSON' then 'Blue_collar'
when category = 'RECOVERED VEHICLE' then 'Blue_collar'
else 'Other'
end as "Category Segment"


from crime

limit 100

------------------------------
--by category

select category,
	count(1)

from crime

group by category
order by 2 desc



----------------------------------
--by year
select 

extract(year from dates),
count(1)

from crime
group by 1
order by 2 desc

--------------------------------
--by day of week
select dayofweek,
	count(1)

from crime
group by dayofweek


----------------------------------
--by hour
select 
extract(hour from dates),
count(1)

from crime
group by 1
---------------------------------



select *
from crime

limit 100


