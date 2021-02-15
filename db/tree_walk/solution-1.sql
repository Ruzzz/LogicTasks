WITH RECURSIVE children AS
(
    -- 'root'
    SELECT *,
        -- optional
        1 as level,
        tree.id::text as path,
        FALSE as looped
    FROM tree WHERE id = 100

    UNION ALL

    -- recursive
    SELECT tree.*,
        -- optional
        children.level + 1,
        concat_ws('.', children.path, tree.id),
        tree.id::text = ANY(string_to_array(children.path, '.'))
    FROM children, tree
    WHERE
        tree.pid = children.id AND NOT looped
)
SELECT * FROM children ORDER BY path;
