
from app.services.database import db_service
from datetime import datetime

class Item:
    def __init__(self, item_code=None, desc=None, group_name=None, unit=None, 
                 current_stock=0, category=None, reorder_level=0, batch_size=1):
        self.item_code = item_code
        self.desc = desc
        self.group_name = group_name
        self.unit = unit
        self.current_stock = current_stock
        self.category = category
        self.reorder_level = reorder_level
        self.batch_size = batch_size
    
    @classmethod
    def get_all(cls):
        """Get all items"""
        query = "SELECT * FROM ITEM_MAST ORDER BY Item_Code"
        return db_service.execute_query(query)
    
    @classmethod
    def get_by_code(cls, item_code):
        """Get item by code"""
        query = "SELECT * FROM ITEM_MAST WHERE Item_Code = %s"
        return db_service.execute_query(query, (item_code,), fetch_one=True)
    
    @classmethod
    def create(cls, item_data):
        """Create new item"""
        query = """
            INSERT INTO ITEM_MAST 
            (Item_Code, item_desc, Group_Name, Unit, Current_Stock, Category, Reorder_Level, Batch_Size)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            item_data['item_code'], item_data['item_desc'], item_data['group_name'],
            item_data['unit'], item_data['current_stock'], item_data['category'],
            item_data['reorder_level'], item_data['batch_size']
        )
        return db_service.execute_query(query, params)
    
    @classmethod
    def update(cls, item_code, item_data):
        """Update existing item"""
        query = """
            UPDATE ITEM_MAST 
            SET Desc = %s, Group_Name = %s, Unit = %s, Current_Stock = %s,
                Category = %s, Reorder_Level = %s, Batch_Size = %s
            WHERE Item_Code = %s
        """
        params = (
            item_data['desc'], item_data['group_name'], item_data['unit'],
            item_data['current_stock'], item_data['category'],
            item_data['reorder_level'], item_data['batch_size'], item_code
        )
        return db_service.execute_query(query, params)
    
    @classmethod
    def delete(cls, item_code):
        """Delete item"""
        query = "DELETE FROM ITEM_MAST WHERE Item_Code = %s"
        return db_service.execute_query(query, (item_code,))
    
    @classmethod
    def get_low_stock_items(cls):
        """Get items below reorder level"""
        query = """
            SELECT * FROM ITEM_MAST 
            WHERE Current_Stock <= Reorder_Level 
            ORDER BY Item_Code
        """
        return db_service.execute_query(query)
    
    @classmethod
    def update_stock(cls, item_code, quantity, operation='add'):
        """Update item stock"""
        if operation == 'add':
            query = "UPDATE ITEM_MAST SET Current_Stock = Current_Stock + %s WHERE Item_Code = %s"
        else:
            query = "UPDATE ITEM_MAST SET Current_Stock = Current_Stock - %s WHERE Item_Code = %s"
        
        return db_service.execute_query(query, (quantity, item_code))
