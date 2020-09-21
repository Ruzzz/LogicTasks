import sqlalchemy as sa

meta = sa.MetaData()


users = sa.Table(
    'users',
    meta,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('login', sa.String(255), nullable=False),
    sa.Column('secret', sa.String(255), nullable=False),
    sa.Column('admin', sa.Boolean, nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('login', name='users_unq_login'),
)


posts = sa.Table(
    'posts',
    meta,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('uid', sa.Integer, nullable=False),
    sa.Column('date', sa.TIMESTAMP, nullable=False),
    sa.Column('text', sa.String(255), nullable=True),
    sa.PrimaryKeyConstraint('id', name='posts_pkey'),
    sa.Index('posts_idx_uid', 'uid'),
    sa.Index('posts_idx_date', 'date'),
    sa.ForeignKeyConstraint(('uid',),
                            (users.c.id,),
                            name='posts_fk_uid',
                            onupdate='CASCADE',
                            ondelete='CASCADE'),
)

tags = sa.Table(
    'tags',
    meta,
    sa.Column('tag', sa.String(30), nullable=False),
    sa.Column('pid', sa.Integer, nullable=False),
    sa.PrimaryKeyConstraint('tag', 'pid', name='tags_pkey'),
    sa.ForeignKeyConstraint(('pid',),
                            (posts.c.id,),
                            name='tags_fk_pid',
                            onupdate='CASCADE',
                            ondelete='CASCADE'),
)

incidents = sa.Table(
    'incidents',
    meta,
    sa.Column('uid', sa.Integer, nullable=False),
    sa.Column('date', sa.TIMESTAMP, nullable=False),
    sa.Column('device_id', sa.String(255), nullable=False),
    sa.Column('kind', sa.Integer, nullable=False),
    sa.PrimaryKeyConstraint('uid', 'date', 'device_id', 'kind', name='incidents_pkey'),
    sa.ForeignKeyConstraint(('uid',),
                            (users.c.id,),
                            name='incidents_fk_uid',
                            onupdate='CASCADE',
                            ondelete='CASCADE'),
)
