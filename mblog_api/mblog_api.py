import click

from mblog.web_app import start_web_app


@click.command()
@click.option('--host', default='127.0.0.1', envvar='HOST')
@click.option('--port', default=8080, envvar='PORT')
@click.option('--db-host', default='localhost', envvar='DB_HOST')
@click.option('--db-port', default=5432, envvar='DB_PORT')
@click.option('--db', default='mblog', envvar='DB')
@click.option('--db-user', default='mblog', envvar='DB_USER')
@click.option('--db-password', default='mblog', envvar='DB_PASSWORD')
@click.option('--secret', default='mblog', envvar='SECRET')
@click.option('--init-sql', default=None, envvar='INIT_SQL')
def main(**kwargs):
    init_sql = kwargs.pop('init_sql', None)
    if not init_sql:
        init_sql = 'db/data.sql'
    with open(init_sql) as f:
        init_sql = f.read()

    start_web_app(**kwargs, init_sql=init_sql)


if __name__ == '__main__':
    main(auto_envvar_prefix='MBLOG')
