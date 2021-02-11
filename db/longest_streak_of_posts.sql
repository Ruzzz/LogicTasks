SELECT
  uid,
  max(date_sequence_count) as max_date_sequence_count
FROM (
  SELECT
    uid,
    COUNT(date_sequence_id) + 1 AS date_sequence_count
  FROM (
    -- same rank for sequence
    SELECT
      uid,
      RANK() OVER(ORDER BY uid, linked_with_prev_date) AS date_sequence_id
    FROM (
      -- calc new feature 'linked with prev date'
      SELECT
        uid,
        (ndate - (LAG(ndate) OVER(PARTITION BY uid ORDER BY ndate)) = '1 day') AS linked_with_prev_date
      FROM (
        -- decrease precision
        SELECT DISTINCT
          uid,
          date_trunc('day', date) "ndate"
        FROM
          posts
      ) AS p2
    ) AS p3
    WHERE linked_with_prev_date
  ) AS p4
  GROUP BY
    uid,
    date_sequence_id
) AS p5
GROUP BY
  uid;
