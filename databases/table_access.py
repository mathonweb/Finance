# -------------------------------------------------------------------------------
# Name:         table_access
# Purpose:      Class with methods for Table manipulation
#
# Author:       Mathieu Guilbault
#
# Created:      2020-03-08
# Copyright:    (c) Mathieu Guilbault 2020
# -------------------------------------------------------------------------------


class Table:
    def __init__(self, cur):
        self.cur = cur

    def create_table(self, table_name, columns):
        """ Create a table in the database

        @param table_name: Table name in the database
        @param columns: Tuple of columns (name type, name type)
        @return: None
        """
        # Verify is the table already exist
        query = "CREATE TABLE IF NOT EXISTS " + table_name + " " + columns + ";"
        self.cur.execute(query)

    def insert_values(self, table_name, values):
        """ Insert a row in the table

        @param table_name: Table name in the database
        @param values: List of values representing a row
        @return: None
        """
        # Add values in the table
        query = "INSERT INTO " + table_name + " VALUES (" + ', '.join(values) + ");"
        print("Insert values query= " + query)
        self.cur.execute(query)

    def get_table_values(self, table_name):
        """ Get table values.

        @param table_name: Table name in the database
        @return: Dict of values
        """

        query = "SELECT * FROM " + table_name + ";"
        self.cur.execute(query)

        # Create a list with values
        values = []
        for val in self.cur:
            values.append(val)

        return values

    def get_table_value(self, table_name, get_col, ref_col, ref_val):
        """ Get table value.

        @param table_name: Table name in the database
        @param get_col: Column name where we get the value
        @param ref_col: Column name used to select the line
        @param ref_val: Value to find in the ref_col for returning the line
        @return: First value
        """

        query = "SELECT " + get_col + " FROM " + table_name + " where " + ref_col + " = " + ref_val + ";"
        self.cur.execute(query)

        # Create a list with values
        values = []
        for val in self.cur:
            values.append(val)

        return values[0]

    def update_table_value(self, table_name, edit_col, new_value, ref_col, ref_val):
        """ Update a single value in the table

        @param table_name: Table name in the database
        @param edit_col: Column where the value to modify is located
        @param new_value: New value to replace
        @param ref_col: Column used to search the ref_val
        @param ref_val: Searching value to get the row where we update a value
        @return: None
        """
        query = "UPDATE " + table_name + " SET " + edit_col + " = " + new_value + " WHERE " + ref_col + " = " + \
                ref_val + ";"
        self.cur.execute(query)

