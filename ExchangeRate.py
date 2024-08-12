import pyodbc
import requests
import logging
from datetime import datetime

user = "santosam"
password = "Apocalipse@5951##"

credentials = (
    "Driver={SQL Server};"
    "Server=EQSAPDBS01;"
    "Database=YokineDB;"
    f"UID={user};"
    f"PWD={password}"
)

# Configuração do log no DW
def insertLogsSQL(level, message):
    connectionSQL = pyodbc.connect(credentials)
    cursor = connectionSQL.cursor()

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = "INSERT INTO YokineDB.dbo.ExchangeRateLogs (timestamp, level, message) VALUES (?, ?, ?)"

    cursor.execute(query, (timestamp, level, message))
    connectionSQL.commit()
    cursor.close()
    connectionSQL.close()

class SQLLogHandler(logging.Handler):
    def emit(self, record):
      logMessage = self.format(record)
      insertLogsSQL(record.levelname, logMessage)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')

SQLHandler = SQLLogHandler()
SQLHandler.setFormatter(formatter)
logger.addHandler(SQLHandler)

# Integração API
def main():
    endpoint = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
    request = requests.get(endpoint)

    if request.status_code == 200:
        data = request.json()
        # USDBRL
        codeUSD = data['USDBRL']['code']
        highUSD = data['USDBRL']['high']
        lowUSD = data['USDBRL']['low']
        dateUSD = data['USDBRL']['create_date']
        # EURBRL
        codeEUR = data['EURBRL']['code']
        highEUR = data['EURBRL']['high']
        lowEUR = data['EURBRL']['low']
        dateEUR = data['EURBRL']['create_date']
        # BTCBRL
        codeBTC = data['BTCBRL']['code']
        highBTC = data['BTCBRL']['high']
        lowBTC = data['BTCBRL']['low']
        dateBTC = data['BTCBRL']['create_date']

        logger.info('Request conectada!')
    else:
        logger.error('Erro na request')
        return

    infos = [
        (codeUSD, highUSD, lowUSD, dateUSD),
        (codeEUR, highEUR, lowEUR, dateEUR),
        (codeBTC, highBTC, lowBTC, dateBTC)
    ]

    # Conexão SQL
    try:
        connectionSQL = pyodbc.connect(credentials)
        cursor = connectionSQL.cursor()
        logger.info("Conexão com o DW bem-sucedida!")
    except Exception as e:
        logger.error("Erro ao conectar com o DW: %s", e)
        return

    # Inserção dos dados no SQL
    try:
        for i in infos:
          query = "INSERT INTO YokineDB.dbo.ExchangeRate (code, maxcotation, mincotation, date) VALUES (?, ?, ?, ?)"
          cursor.execute(query, i)

        connectionSQL.commit()
        logger.info("Query executada com sucesso!")

    except Exception as e:
        logger.error("Erro ao executar a Query: %s", e)

    finally:
        cursor.close()
        connectionSQL.close()
        logger.info("Integração concluída com sucesso!")

if __name__ == "__main__":
    main()
