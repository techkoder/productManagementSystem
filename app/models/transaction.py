from app.services.database import db_service

class Transaction:
    """Model for inventory transactions mapped to TRANS_DETL."""

    @classmethod
    def get_all(cls):
        """Get all transactions ordered by date and code."""
        query = "SELECT * FROM TRANS_DETL ORDER BY Txn_Date DESC, Txn_Code DESC"
        return db_service.execute_query(query)

    @classmethod
    def get_by_code(cls, txn_code):
        """Get a single transaction by code."""
        query = "SELECT * FROM TRANS_DETL WHERE Txn_Code = %s"
        return db_service.execute_query(query, (txn_code,), fetch_one=True)

    @classmethod
    def create(cls, txn_data):
        """Create a new transaction record.

        Expected keys: txn_code, txn_date, txn_type, qty_issued, qty_recd,
        item_code, ven_code (opt), cust_code (opt)
        """
        query = """
            INSERT INTO TRANS_DETL 
            (Txn_Code, Txn_Date, Txn_Type, Qty_Issued, Qty_Recd, Item_Code, Ven_Code, Cust_Code)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            txn_data['txn_code'],
            txn_data['txn_date'],
            txn_data['txn_type'],
            txn_data.get('qty_issued', 0),
            txn_data.get('qty_recd', 0),
            txn_data['item_code'],
            txn_data.get('ven_code'),
            txn_data.get('cust_code'),
        )
        return db_service.execute_query(query, params)

    @classmethod
    def update(cls, txn_code, txn_data):
        """Update an existing transaction."""
        query = """
            UPDATE TRANS_DETL
            SET Txn_Date = %s,
                Txn_Type = %s,
                Qty_Issued = %s,
                Qty_Recd = %s,
                Item_Code = %s,
                Ven_Code = %s,
                Cust_Code = %s
            WHERE Txn_Code = %s
        """
        params = (
            txn_data['txn_date'],
            txn_data['txn_type'],
            txn_data.get('qty_issued', 0),
            txn_data.get('qty_recd', 0),
            txn_data['item_code'],
            txn_data.get('ven_code'),
            txn_data.get('cust_code'),
            txn_code,
        )
        return db_service.execute_query(query, params)

    @classmethod
    def delete(cls, txn_code):
        """Delete a transaction by code."""
        query = "DELETE FROM TRANS_DETL WHERE Txn_Code = %s"
        return db_service.execute_query(query, (txn_code,))

    @classmethod
    def list_by_item(cls, item_code):
        query = "SELECT * FROM TRANS_DETL WHERE Item_Code = %s ORDER BY Txn_Date DESC, Txn_Code DESC"
        return db_service.execute_query(query, (item_code,))

    @classmethod
    def list_by_vendor(cls, ven_code):
        query = "SELECT * FROM TRANS_DETL WHERE Ven_Code = %s ORDER BY Txn_Date DESC, Txn_Code DESC"
        return db_service.execute_query(query, (ven_code,))

    @classmethod
    def list_by_customer(cls, cust_code):
        query = "SELECT * FROM TRANS_DETL WHERE Cust_Code = %s ORDER BY Txn_Date DESC, Txn_Code DESC"
        return db_service.execute_query(query, (cust_code,))

    @classmethod
    def record_issue(cls, txn_code, txn_date, item_code, quantity, ven_code=None, cust_code=None):
        """Convenience method to record an issue transaction (stock out)."""
        data = {
            'txn_code': txn_code,
            'txn_date': txn_date,
            'txn_type': 'ISSUE',
            'qty_issued': quantity,
            'qty_recd': 0,
            'item_code': item_code,
            'ven_code': ven_code,
            'cust_code': cust_code,
        }
        return cls.create(data)

    @classmethod
    def record_receipt(cls, txn_code, txn_date, item_code, quantity, ven_code=None, cust_code=None):
        """Convenience method to record a receipt transaction (stock in)."""
        data = {
            'txn_code': txn_code,
            'txn_date': txn_date,
            'txn_type': 'RECEIPT',
            'qty_issued': 0,
            'qty_recd': quantity,
            'item_code': item_code,
            'ven_code': ven_code,
            'cust_code': cust_code,
        }
        return cls.create(data)
