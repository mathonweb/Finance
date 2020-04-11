# -------------------------------------------------------------------------------
# Name:         database_access
# Purpose:      Class with methods for Database manipulation
#
# Author:       Mathieu Guilbault
#
# Created:      2020-03-08
# Copyright:    (c) Mathieu Guilbault 2020
# -------------------------------------------------------------------------------

import mysql.connector
from mysql.connector import errorcode
from table_access import Table

import database_config as cfg


class Database(Table):
    """ Database class with Table subclass"""

    def __init__(self, ip_address, username, password, database_name):
        """ Create a Database which includes tables

        @param ip_address: MySQL server IP
        @param username: MySQL username
        @param password: MySQL password
        @param database_name: MySQL database name
        """
        self.cnx = self.open_connection(ip_address, username, password, database_name)
        self.cur = self.cnx.cursor()
        query = "USE " + database_name
        self.cur.execute(query)
        Table.__init__(self, self.cur)

    def open_connection(self, ip_address, username, password, database_name):
        """ Establish a connection with MySQL database

        @param ip_address: MySQL server IP
        @param username: MySQL username
        @param password: MySQL password
        @param database_name: MySQL database name
        @return: MySQL Connector/Python instance
        """
        try:
            cnx = mysql.connector.connect(user=username, password=password, host=ip_address, database=database_name,
                                          auth_plugin='mysql_native_password')

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        else:
            print("Connected to database " + database_name)
            return cnx

    def close_connection(self):
        """ Close the MySQL connection"""
        self.cnx.commit()
        self.cur.close()
        self.cnx.close()

    def __del__(self):
        self.cur.close()
        self.cnx.close()


def main():
    test_db = Database(cfg.my_sql["host"], cfg.my_sql["user"], cfg.my_sql["passwd"], cfg.my_sql["db"])
    test_db.create_table("test_table", "(year CHAR(4), return_val DOUBLE)")
    #test_db.insert_values("test_table", ["2013", "5.67"])
    #test_db.insert_values("test_table", ["2014", "15.67"])
    test_db.update_table_value("test_table", "return_val", "10.67", "year", "2013")
    values = test_db.get_table_values("test_table")

    for val in values:
        print(val[0])

    test_db.close_connection()


if __name__ == '__main__':
    main()
