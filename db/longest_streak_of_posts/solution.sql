WITH t0(uid, start_date, days) AS (
    SELECT
        uid,
        min(ndate) as start_date,
        count(date_sequ_id) as days
    FROM (
        -- Generate unique id for consecutive identical values
        SELECT
            uid,
            ndate,
            SUM(CASE WHEN ndate - prev_date <> '1 day' THEN 1 ELSE 0 END)
                OVER (PARTITION BY uid ORDER BY ndate) as date_sequ_id
        FROM (
          -- Add 'previous date', because LAG cannot be used inside SUM
            SELECT 
                uid,
                ndate,
                LAG(ndate) OVER (PARTITION BY uid ORDER BY ndate) as prev_date
            FROM (
              -- Decrease precision of 'date' column
                SELECT DISTINCT
                    uid,
                    date_trunc('day', date) AS ndate
                FROM events
            ) as t1
        ) as t2
    ) as t3
    GROUP BY uid, date_sequ_id
)

SELECT * FROM t0 WHERE days = (SELECT MAX(days) FROM t0)
