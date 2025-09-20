import mysql.connector
from mysql.connector import Error
from flask import current_app, g
import logging

class DatabaseService:
    def __init__(self):
        self.connection = None
    
    def get_connection(self):
        """Get database connection"""
        if 'db_connection' not in g:
            try:
                g.db_connection = mysql.connector.connect(
                    host=current_app.config['MYSQL_HOST'],
                    database=current_app.config['MYSQL_DATABASE'],
                    user=current_app.config['MYSQL_USER'],
                    password=current_app.config['MYSQL_PASSWORD'],
                    port=current_app.config['MYSQL_PORT'],
                    autocommit=True
                )
            except Error as e:
                current_app.logger.error(f"Database connection error: {e}")
                raise
        
        return g.db_connection
    
    def close_connection(self):
        """Close database connection"""
        db = g.pop('db_connection', None)
        if db is not None and db.is_connected():
            db.close()
    
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=True):
        """Execute database query"""
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute(query, params or ())
            
            if query.strip().upper().startswith('SELECT'):
                if fetch_one:
                    return cursor.fetchone()
                elif fetch_all:
                    return cursor.fetchall()
            else:
                connection.commit()
                return cursor.rowcount
        except Error as e:
            connection.rollback()
            current_app.logger.error(f"Query execution error: {e}")
            raise
        finally:
            cursor.close()
    
    def execute_many(self, query, data):
        """Execute multiple queries"""
        connection = self.get_connection()
        cursor = connection.cursor()
        
        try:
            cursor.executemany(query, data)
            connection.commit()
            return cursor.rowcount
        except Error as e:
            connection.rollback()
            current_app.logger.error(f"Batch query execution error: {e}")
            raise
        finally:
            cursor.close()

# Create global database service instance
db_service = DatabaseService()