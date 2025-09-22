
from app.services.database import db_service
from datetime import datetime

class Customer:
    def __init__(self, cust_code=None, cust_name=None, address1=None, address2=None,
                 city=None, post_code=None):
        self.cust_code = cust_code
        self.cust_name = cust_name
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.post_code = post_code
    
    @classmethod
    def get_all(cls):
        """Get all customers"""
        query = "SELECT * FROM CUST_MAST ORDER BY Cust_Code"
        return db_service.execute_query(query)
    
    @classmethod
    def get_by_code(cls, cust_code):
        """Get customer by code"""
        query = "SELECT * FROM CUST_MAST WHERE Cust_Code = %s"
        return db_service.execute_query(query, (cust_code,), fetch_one=True)
    
    @classmethod
    def create(cls, customer_data):
        """Create new customer"""
        query = """
            INSERT INTO CUST_MAST 
            (Cust_Code, Cust_Name, Address1, Address2, City, Post_Code)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            customer_data['cust_code'], customer_data['cust_name'],
            customer_data.get('address1'), customer_data.get('address2'),
            customer_data.get('city'), customer_data.get('post_code')
        )
        return db_service.execute_query(query, params)
    
    @classmethod
    def update(cls, cust_code, customer_data):
        """Update existing customer"""
        query = """
            UPDATE CUST_MAST
            SET Cust_Name = %s, Address1 = %s, Address2 = %s,
                City = %s, Post_Code = %s
            WHERE Cust_Code = %s
        """
        params = (
            customer_data['cust_name'], customer_data.get('address1'),
            customer_data.get('address2'), customer_data.get('city'),
            customer_data.get('post_code'), cust_code
        )
        return db_service.execute_query(query, params)
    
    @classmethod
    def delete(cls, cust_code):
        """Delete customer"""
        query = "DELETE FROM CUST_MAST WHERE Cust_Code = %s"
        return db_service.execute_query(query, (cust_code,))
