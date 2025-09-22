
from app.services.database import db_service
from datetime import datetime

class Vendor:
    def __init__(self, ven_code=None, ven_name=None, vendor_location=None, address1=None, address2=None,
                 city=None, post_code=None):
        self.ven_code = ven_code
        self.ven_name = ven_name
        self.vendor_location = vendor_location
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.post_code = post_code
    
    @classmethod
    def get_all(cls):
        """Get all vendors"""
        query = "SELECT * FROM VEN_MAST ORDER BY Ven_Code"
        return db_service.execute_query(query)
    
    @classmethod
    def get_by_code(cls, ven_code):
        """Get vendor by code"""
        query = "SELECT * FROM VEN_MAST WHERE Ven_Code = %s"
        return db_service.execute_query(query, (ven_code,), fetch_one=True)
    
    @classmethod
    def create(cls, vendor_data):
        """Create new vendor"""
        query = """
            INSERT INTO VEN_MAST 
            (Ven_Code, Ven_Name, vendor_Location, Address1, Address2, City, Post_Code)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            vendor_data['ven_code'], vendor_data['ven_name'], vendor_data.get('vendor_location'),
            vendor_data.get('address1'), vendor_data.get('address2'), vendor_data.get('city'),
            vendor_data.get('post_code')
        )
        return db_service.execute_query(query, params)
    
    @classmethod
    def update(cls, ven_code, vendor_data):
        """Update existing vendor"""
        query = """
            UPDATE VEN_MAST
            SET Ven_Name = %s, vendor_Location = %s, Address1 = %s, Address2 = %s,
                City = %s, Post_Code = %s
            WHERE Ven_Code = %s
        """
        params = (
            vendor_data['ven_name'], vendor_data.get('vendor_location'), vendor_data.get('address1'),
            vendor_data.get('address2'), vendor_data.get('city'), vendor_data.get('post_code'), ven_code
        )
        return db_service.execute_query(query, params)
    
    @classmethod
    def delete(cls, ven_code):
        """Delete vendor"""
        query = "DELETE FROM VEN_MAST WHERE Ven_Code = %s"
        return db_service.execute_query(query, (ven_code,))
