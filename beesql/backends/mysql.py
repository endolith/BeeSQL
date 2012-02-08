#!/usr/bin/env python

''' Contains Mysql Database Connection. '''

# Author: Kasun Herath <kasunh01@gmail.com>
# Source: https://github.com/kasun/beesql

import pymysql

from base import BeeSQLBaseConnection
from beesql import BeeSQLError
from beesql import BeeSQLDatabaseError

class MYSQLConnection(BeeSQLBaseConnection):
    ''' MySQL Database Connection. '''
    def __init__(self, username, password, host='localhost', port=3306, db=None, unix_socket=None):
        ''' Initialize MysqlConnection. Initialize BaseConnection, register database connection and cursor.
            If db is specified issue a use query. '''
        BeeSQLBaseConnection.__init__(self)
        if (not username or password is None):
            raise BeeSQLError('Engine mysql requires username and password')
        try:
            if not unix_socket:
                self.db_connection = pymysql.connect(user=username, passwd=password, host=host, port=port)
            else:
                self.db_connection = pymysql.connect(user=username, passwd=password, unix_socket=unix_socket)
            self.cursor = self.db_connection.cursor(pymysql.cursors.DictCursor)
            if db and db != '':
                self.cursor.execute('use %s' % (db))
        except pymysql.err.DatabaseError, de:
            raise BeeSQLDatabaseError(str(de))

    def query(self, sql, escapes=None):
        ''' Run provided query.
        Arguments:
            sql: Query to run.
            escapes: Optional, A tuple of escape values to escape provided sql. '''
        try:
            return self.run_query(sql, escapes)
        except pymysql.err.DatabaseError, de:
            raise BeeSQLDatabaseError(str(de))

    def close(self):
        ''' Close connection to Databaes. '''
        self.db_connection.close()
