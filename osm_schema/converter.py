
import os, subprocess, time


SOURCE_DB_HOST = os.getenv('SOURCE_DB_HOST', '192.168.1.124:5432')
SOURCE_DB_NAME = os.getenv('SOURCE_DB_NAME', 'aquagis_pernik')
SOURCE_DB_USER = os.getenv('SOURCE_DB_USER', 'gis')

TEMP_AQUAGIS_FILE = os.getenv('TEMP_OSM', 'tmp.osm')
TEMP_FOLDER = os.getenv('TEMP_FOLDER', '/srv/tmp/')
AQUAGIS_STYLE_PATH = os.getenv('AQUAGIS_STYLE_PATH', '/srv/tools/aquagis/aquagis_default.style')
AQUAGIS_WAREHOUSE_PREFIX = os.getenv('AQUAGIS_WAREHOUSE_PREFIX', 'aquagis_20210624')

DESTINATION_WAREHOUSE = os.getenv('DESTINATION_WAREHOUSE', 'aquagis_warehouse')
DESTINATION_DB_USER = os.getenv('DESTINATION_DB_USER', 'gis')
DESTINATION_DB_HOST = os.getenv('DESTINATION_DB_HOST', '192.168.1.124')
DESTINATION_DB_PORT = os.getenv('DESTINATION_DB_PORT', '5432')


def aquagis_to_osm():
    # osmosis --read-apidb validateSchemaVersion=no host="192.168.1.124:5432" database="aquagis_pernik" user="gis" --write-xml file="export.osm"

    host = f'host={SOURCE_DB_HOST}'
    db = f'database={SOURCE_DB_NAME}'
    user = f'user={SOURCE_DB_USER}'
    export = f'file={TEMP_FOLDER}{TEMP_AQUAGIS_FILE}'

    command = ['/srv/tools/osmosis/bin/osmosis', '--read-apidb', 'validateSchemaVersion=no', host, db, user, '--write-xml', export]
    subprocess.check_call(command)


def osm_to_warehouse():
    # osm2pgsql -c -S /srv/tools/aquagis/aquagis_default.style --prefix aquagis -d aquagis_warehouse -U gis -H 192.168.1.124 -P 5432 export.osm

    aquagis_style_path = AQUAGIS_STYLE_PATH
    prefix = AQUAGIS_WAREHOUSE_PREFIX
    export = f'{TEMP_FOLDER}{TEMP_AQUAGIS_FILE}'
    warehouse_db = DESTINATION_WAREHOUSE
    warehouse_user = DESTINATION_DB_USER
    warehouse_host = DESTINATION_DB_HOST
    warehouse_port = DESTINATION_DB_PORT

    command = ['osm2pgsql', '-c', '-S', aquagis_style_path, '--prefix', prefix, '-d', warehouse_db, '-U', warehouse_user, '-H', warehouse_host, '-P', warehouse_port, export]
    subprocess.check_call(command)


if __name__ == '__main__':
    s = time.perf_counter()
    aquagis_to_osm()
    time.sleep(0.5)
    osm_to_warehouse()
    print(f'exec costs ~ {time.perf_counter() - s} seconds')

