import pymysql
from config import DBconf

connect = pymysql.connect(
    host=DBconf.host,
    port=DBconf.port,
    user=DBconf.user,
    password=DBconf.password,
    database=DBconf.database,
)
def INSERT(TABLENAME,INTO,VALUES):
    print(f"INSERT INTO `{TABLENAME}` "
                    f"({INTO}) "
                    f"VALUES ({VALUES})")
    with connect.cursor() as con:
        con.execute(f"INSERT INTO `{TABLENAME}` "
                    f"({INTO}) "
                    f"VALUES ({VALUES})")
        connect.commit()
        con.close()
def SELECT(INTO,TABLENAME,WHERE):
    print(f"SELECT {INTO} "
                    f"FROM `{TABLENAME}` "
                     f"WHERE {WHERE}")
    with connect.cursor() as con:
        con.execute(f"SELECT {INTO} "
                    f"FROM `{TABLENAME}` "
                     f"WHERE {WHERE}")
        con.close()
        return con.fetchall()
def DELETE (TABLENAME,ID):
    with connect.cursor() as con:
        con.execute(f"DELETE FROM `{TABLENAME}` "
                    f"WHERE `{TABLENAME}`.`id` = {ID}")
        connect.commit()
        con.close()
def UPDATE(TABLENAME,SET,ID):
    with connect.cursor() as con:
        con.execute(f"UPDATE `{TABLENAME}` SET {SET} WHERE `{TABLENAME}`.`id` = {ID}")
        connect.commit()
        con.close()
def UPDATEWHERE(TABLENAME,SET,WHERE):
    print(f"UPDATE `{TABLENAME}` SET {SET} WHERE {WHERE}")
    with connect.cursor() as con:
        con.execute(f"UPDATE `{TABLENAME}` SET {SET} WHERE {WHERE}")
        connect.commit()
        con.close()
def IFUSERINDB(TABLENAME,USERNAME):
    with connect.cursor() as con:
        RES = con.execute(f"SELECT `userName` "
                              f"FROM `{TABLENAME}` "
                              f"WHERE `userName` = '{USERNAME}'")
        con.close()
        return bool(RES)
def IF(TABLENAME,INTO,WHERE):
    print(f"SELECT {INTO} "
          f"FROM `{TABLENAME}` "
          f"WHERE {WHERE}")
    with connect.cursor() as con:
        RESO = con.execute(f"SELECT {INTO} "
                            f"FROM `{TABLENAME}` "
                            f"WHERE {WHERE}")
        con.close()
        return bool(RESO)
def CREATE_TABLE(TABLENAME,ARGS):
    with connect.cursor() as con:
        con.execute(f"CREATE TABLE `{TABLENAME}` ({ARGS})")
        connect.commit()
def COUNT(TABLENAME,INTO,WHERE):
    with connect.cursor() as con:
        RESO = con.execute(f"SELECT {INTO} "
                               f"FROM `{TABLENAME}` "
                               f"WHERE {WHERE}")
        con.close()
        return RESO
