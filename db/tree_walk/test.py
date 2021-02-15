import psycopg2 as psycopg

INIT_SQL = '''DROP TABLE IF EXISTS tree;
CREATE TABLE tree (
    id int4 NOT NULL PRIMARY KEY,
    pid int4,  -- parent id
    payload VARCHAR(255)
);
ALTER TABLE tree ADD CONSTRAINT tree_fk_pid FOREIGN KEY (pid)
    REFERENCES tree (id) ON UPDATE CASCADE;

INSERT INTO tree VALUES
    (10, NULL, 'root'),
    (100, 10, 'son-1'),
    (4, 100, 'grandson-1-1'),
    (5, 100, 'grandson-1-2'),
    (101, 10, 'son-2'),
    (3, 101, 'grandson-2-1');'''


conn = psycopg.connect(
    database='logictasks', user='dev', password='dev',
    host='localhost', port=5432)
cur = conn.cursor()
cur.execute(INIT_SQL)
conn.commit()
