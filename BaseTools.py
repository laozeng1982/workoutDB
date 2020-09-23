import pymysql
from pandas import DataFrame
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError

from datamodel.Data import DataBase


def createEngine(schema):
    """
    Create a MySQL context before operation.
    :param schema
    :return:
    """
    # engine = create_engine("mysql+pymysql://root:root123@127.0.0.1:3306/{schema}?charset=utf8".format(schema=schema))
    engine = create_engine(
        "mysql+mysqlconnector://root:root123@127.0.0.1:3306/{schema}?charset=utf8".format(schema=schema))
    # print(engine)
    return engine


def createConnect(schema):
    """

    :param schema:
    :return:
    """
    connect = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='root123',
        db=schema,
        charset='utf8mb4'
    )
    return connect


def updateTable(schema, tableName: str, dataFrame: DataFrame, index=True, if_exists='replace'):
    """
    Basic function to update whole table.
    :param schema:
    :param tableName:
    :param index:
    :param dataFrame:
    :param if_exists:
    :return: {'fail', 'replace', 'append'}, default 'fail', How to behave if the table already exists.
    """

    # Save to MySQL
    # DataFrame 对大小写敏感，统一转成小写
    engine = createEngine(schema)
    try:
        dataFrame.to_sql(name=tableName.lower(), index=index, if_exists=if_exists, con=engine)
        return True
    except ProgrammingError as e:
        print(e)
        return False


def save(dataFrame: DataFrame, tableName):
    con = createConnect(DataBase.Workout)
    sql = "show global variables like 'max_allowed_packet';"
    con.cursor().execute(sql)
    con.commit()
    con.close()
    return updateTable(DataBase.Workout, tableName, dataFrame, index=True)


def updateColumns(schema, table: str, indexKeyValues: dict, updatedKeyValues: dict):
    """

    :param schema: Database name.
    :param table: Table name in this database.
    :param indexKeyValues:
    :param updatedKeyValues:
    :return:
    """

    con = createConnect(schema)
    cursor = con.cursor()

    indexKeys = " and ".join(["%s='%s'" % (key, indexKeyValues.get(key)) for key in indexKeyValues.keys()])
    updatedKeys = ",".join(["%s='%s'" % (key, updatedKeyValues.get(key)) for key in updatedKeyValues.keys()])

    sql = "update %s.%s set %s where %s;" % (schema, table, updatedKeys, indexKeys)
    # print(sql)
    cursor.execute(sql)

    con.commit()
    con.close()


if __name__ == '__main__':
    # Test 1
    # keys = [x.Name for x in [Financial.code, Financial.statDate, Financial.roe]]
    # query(DataBase.General, DataTable.Financial, ','.join(keys), "roe>=20")

    # Test 2
    # idxKey = {
    #     StockInfo.JqIndex.Name: '000001.XSHE'
    # }
    #
    # updated = {
    #     StockInfo.BarStartDate.Name: '2014-10-10',
    #     StockInfo.BarEndDate.Name: '2021-12-10'
    # }
    #
    # updateColumns(DataBase.General, DataTable.StockInfo, idxKey, updated)

    # Test 3
    pass
