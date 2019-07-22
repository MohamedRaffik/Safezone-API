from sqlalchemy.sql import text
from datetime import timedelta, datetime, date
from typing import Dict

Dates: dict = {
    "week": 7,
    "month": 30,
    "3 month": 90,
    "6 month": 180,
    "9 month": 270,
    "year": 365
}

def closest_stations(db, latitude: float, longitude: float) -> list:
    query = text(
        '''
        WITH station_ids AS (
            SELECT 
                *
            FROM (
                SELECT 
                    id, name, line, latitude, longitude, ST_Distance( ST_MakePoint(longitude, latitude)::geography, ST_MakePoint(:lon, :lat)::geography) AS distance 
                FROM 
                    stations 
                ORDER BY distance 
                LIMIT 5
            ) AS t1
            UNION
            SELECT 
                * 
            FROM (
                SELECT 
                    id, name, line, latitude, longitude, ST_Distance( ST_MakePoint(longitude, latitude)::geography, ST_MakePoint(:lon, :lat)::geography) AS distance
                FROM stations
            ) AS t2 
            WHERE t2.distance < 152.4
        ),
        subquery AS (
            SELECT 
                t7.id, coalesce(t7.sum, 0) as sum, t7.count 
            FROM (
                SELECT 
                    t5.id, sum(t6.risk_points), count(t6.category) 
                FROM 
                    stations AS t5 
                LEFT JOIN (
                    SELECT * FROM crimes_by_station AS t3 
                    JOIN (
                        SELECT 
                            t1.category, t1.risk_points, t2.id 
                        FROM crime_categories AS t1 
                        JOIN crime_info AS t2 
                        ON t1.id = t2.category_id
                    ) AS t4 
                    ON t3.crime_id = t4.id
                ) AS t6 
                ON t5.id = t6.station_id 
                GROUP BY t5.id
            ) AS t7
        )
        SELECT 
            t4.id, t4.name, t4.line, t4.latitude, t4.longitude, t3.percentile 
        FROM ( 
            SELECT t1.id, 100 - (t1.sum / cast(t2.max as float) * 100) AS percentile 
            FROM subquery AS t1 
            JOIN (select max(sum) from subquery) AS t2 
            ON TRUE
        ) AS t3 
        JOIN station_ids AS t4 
        ON t3.id = t4.id 
        ORDER BY t4.distance
        '''
    )

    with db.connect() as conn:
        results = conn.execute(query, lat=latitude, lon=longitude).fetchall()

    return list(results)

def crimes_near_station(db, station_id: int, range: int) -> list:
    query = text(
        '''
        SELECT 
            t3.crime_date, t3.pd_desc, t3.ofns_desc, t3.latitude, t3.longitude, t4.category 
        FROM (
            SELECT
                t2.* 
            FROM crimes_by_station AS t1 
            JOIN crime_info AS t2 
            ON t1.crime_id = t2.id 
            WHERE t1.station_id = :id AND t2.crime_date > current_date - :range
        ) AS t3 JOIN crime_categories AS t4 ON t3.category_id = t4.id
        '''
    )

    with db.connect() as conn:
        results = conn.execute(query, id=station_id, range=range)

    return list(results)
    

def crimes_near_point(db, latitude: float, longitude: float, range: int) -> list:

    query = text(
        '''
        SELECT 
            t1.crime_date, t2.category, t1.ofns_desc, t1.pd_desc, t1.latitude, t1.longitude 
        FROM crime_info AS t1 
        JOIN crime_categories AS t2 
        ON t1.category_id = t2.id 
        WHERE ST_Distance( ST_MakePoint(longitude, latitude)::geography, ST_MakePoint(:lon, :lat)::geography) < 152.4
        '''
    )

    with db.connect() as conn:
        results = conn.execute(query, lat=latitude, lon=longitude, range=range).fetchall()

    return list(results)

def station_percentile_rank(db, station_ids: tuple, categories: tuple, range: int) -> list:
    
    where_clause = 'WHERE t1.id = any(:s_id)' if len(station_ids) > 0 else ''
    
    query = text(
        f'''
         WITH subquery AS (
            SELECT 
                t7.id, t7.name, t7.line, coalesce(t7.sum, 0) as sum, t7.count 
            FROM (
                SELECT 
                    t5.id, t5.name, t5.line, sum(t6.risk_points), count(t6.category) 
                FROM stations AS t5 
                LEFT JOIN (
                    SELECT 
                        * 
                    FROM crimes_by_station AS t3 
                    JOIN (
                        SELECT 
                            t1.category, t1.risk_points, t2.id 
                        FROM crime_categories AS t1 
                        JOIN crime_info AS t2 
                        ON t1.id = t2.category_id
                        WHERE t1.id = any(:cat) AND t2.crime_date > current_date - :range
                    ) AS t4 
                    ON t3.crime_id = t4.id
                ) AS t6 
                ON t5.id = t6.station_id 
                GROUP BY t5.id
            ) as t7
        )
        SELECT 
            t1.id, t1.name, t1.line, 100 - (t1.sum / cast(t2.max as float) * 100) AS percentile 
        FROM subquery AS t1 
        JOIN (select max(coalesce(subquery.sum, 0)) from subquery) AS t2 
        ON TRUE {where_clause} 
        ORDER BY percentile 
        '''
    )
    
    with db.connect() as conn:
        results = conn.execute(query, cat=categories, range=range, s_id=station_ids) if len(station_ids) > 0 else conn.execute(query, cat=categories, range=range).fetchall()

    return list(results)

# Give Crime Category IDs
# For each station display occurences for given ids

def crime_category_occurrence_all_stations(db, categories: tuple, range: int) -> list:
    query = text(
        '''
        SELECT 
            t7.id, t7.name, t7.line, t7.count 
        FROM (
            SELECT 
                t5.id, t5.name, t5.line, sum(t6.risk_points), count(t6.category) 
            FROM stations AS t5 
            LEFT JOIN (
                SELECT 
                    * 
                FROM crimes_by_station AS t3 
                JOIN (
                    SELECT 
                        t1.category, t1.risk_points, t2.id 
                    FROM crime_categories AS t1 
                    JOIN crime_info AS t2 
                    ON t1.id = t2.category_id 
                    WHERE t1.id = any(:cat) AND t2.crime_date > current_date - :range
                ) AS t4 
                ON t3.crime_id = t4.id
            ) AS t6 
            ON t5.id = t6.station_id 
            GROUP BY t5.id
        ) as t7
        '''
    )

    with db.connect() as conn:
        results = conn.execute(query, cat=categories, range=range).fetchall()

    return list(results)

def crime_categories_occurrences_per_station(db, station_id: int, range: int) -> list:
    query = text(
        '''
        SELECT
            t3.category, coalesce(sum(t4.category_id) / t4.category_id, 0) AS occurrences 
        FROM crime_categories AS t3 
        LEFT JOIN (
            SELECT 
                t1.station_id, t2.category_id from crimes_by_station AS t1 
            JOIN crime_info AS t2 
            ON t1.crime_id = t2.id 
            WHERE t1.station_id = :s_id AND t2.crime_date > current_date - :range
        ) AS t4 
        ON t3.id = t4.category_id 
        GROUP BY t3.category, t4.category_id
        '''
    )

    with db.connect() as conn:
        results = conn.execute(query, s_id=station_id, range=range)

    return list(results)