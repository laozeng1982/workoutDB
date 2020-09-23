import pandas as pd
from pandas import DataFrame

from BaseTools import createConnect, updateTable, createEngine
from datamodel.Data import DataBase, DataTable


def saveUser(dataFrame: DataFrame, tableName):
    con = createConnect(DataBase.General)
    sql = "show global variables like 'max_allowed_packet';"
    con.cursor().execute(sql)
    con.commit()
    con.close()
    return updateTable(DataBase.General, tableName, dataFrame, index=True)


def loadUsers(queryColumns: str, queryStockList: list, conditions: str = None, groupBy: str = None):
    """

    :param queryColumns:
    :param queryStockList: If selectedStockList has items, filter it, else return all items.
    :param conditions:
    :param groupBy:
    :return: pandas DataFrame.
    """
    schema = DataBase.General
    tableName = DataTable.Financial
    engine = createEngine(schema)

    if conditions:
        if groupBy:
            sql = "select %s from %s.%s where %s %s;" % (queryColumns, schema, tableName, conditions, groupBy)
        else:
            sql = "select %s from %s.%s where %s;" % (queryColumns, schema, tableName, conditions)
    else:
        if groupBy:
            sql = "select %s from %s.%s %s;" % (queryColumns, schema, tableName, groupBy)
        else:
            sql = "select %s from %s.%s;" % (queryColumns, schema, tableName)

    # print("sql:", sql)

    df = pd.read_sql(sql, con=engine)

    return df


if __name__ == '__main__':
    pass
