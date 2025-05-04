import sys
import os
import psycopg2
from ..config import DatabaseConfig

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)


def get_exchanges_and_securities():
    try:
        conn = psycopg2.connect(
            dbname=DatabaseConfig.dbname,
            user=DatabaseConfig.user,
            password=DatabaseConfig.password,
            host=DatabaseConfig.host,
            port=DatabaseConfig.port
        )
        cursor = conn.cursor()

        query = """
        SELECT e.exchange_code, s.ticker
        FROM tracker_securities s
        JOIN tracker_exchanges e ON s.exchange_id = e.id
        ORDER BY e.exchange_code, s.ticker;
        """

        cursor.execute(query)
        results = cursor.fetchall()

        exchanges = {}

        for exchange_code, ticker in results:
            if exchange_code not in exchanges:
                exchanges[exchange_code] = []
            exchanges[exchange_code].append(ticker)

        cursor.close()
        conn.close()

        return exchanges

    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        return {}


if __name__ == "__main__":
    exchanges = get_exchanges_and_securities()
    print(exchanges)
