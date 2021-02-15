WITH RECURSIVE parents AS
(
    -- 'root'
    SELECT * FROM tree WHERE id = 5
    UNION ALL
    -- recursive
    SELECT tree.* FROM parents, tree WHERE tree.id = parents.pid
)
SELECT * FROM parents;
