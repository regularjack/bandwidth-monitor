import speedtest
import sqlite3
import time

def run_speedtest():
    ts = int(time.time())

    servers = []
    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    s.upload()
    s.download()

    results_dict = s.results.dict()
    return {
        'server': '{name} {sponsor}'.format(
            name=results_dict['server']['name'],
            sponsor=results_dict['server']['sponsor'],
        ),
        'ts': ts,
        'ping': int(results_dict['ping']),
        'download': int(results_dict['download']) // 1000000,
        'upload': int(results_dict['upload']) // 1000000,
    }

def main():
    with create_connection() as connection:
        result = run_speedtest()

        add_result(connection, result)

def add_result(connection, result):
    columns = ', '.join(result.keys())
    placeholders = ':'+', :'.join(result.keys())

    query = 'INSERT INTO results (%s) VALUES (%s)' % (columns, placeholders)

    cursor = connection.cursor()
    cursor.execute(query, result)

    return cursor.lastrowid

def create_connection():
    try:
        connection = sqlite3.connect('speedtest.db')

        connection.execute("""
            CREATE TABLE IF NOT EXISTS RESULTS(
                server TEXT,
                ts INTEGER,
                ping INTEGER,
                download INTEGER,
                upload INTEGER,
                PRIMARY KEY (server, ts)
            )
        """)

        return connection
    except Error as e:
        print(e)

    return None

if __name__ == '__main__':
    main()
