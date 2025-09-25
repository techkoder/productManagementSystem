from app.services.database import db_service


class purchaseOrdersHead:
    """Model for purchase order header mapped to PUR_ORDERS_HEAD.

    This mirrors the structure and API of SalesOrder in sales_order.py.
    """

    @classmethod
    def get_all(cls):
        """Get all purchase orders."""
        query = "SELECT * FROM PUR_ORDERS_HEAD ORDER BY Pur_Ord_No"
        return db_service.execute_query(query)

    @classmethod
    def get_by_number(cls, purchase_order_number):
        """Get a single purchase order by number."""
        query = "SELECT * FROM PUR_ORDERS_HEAD WHERE Pur_Ord_No = %s"
        return db_service.execute_query(query, (purchase_order_number,), fetch_one=True)

    @classmethod
    def create(cls, order_data):
        """Create a new purchase order header.

        Expected keys in order_data: pur_ord_no, order_qty, order_date, ven_code, purchase_status (optional)
        """
        query = """
            INSERT INTO PUR_ORDERS_HEAD 
            (Pur_Ord_No, Order_Qty, Order_Date, Ven_Code, purchaseStatus)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            order_data['pur_ord_no'],
            order_data['order_qty'],
            order_data['order_date'],
            order_data['ven_code'],
            order_data.get('purchase_status', 'Pending')
        )
        return db_service.execute_query(query, params)

    @classmethod
    def update(cls, purchase_order_number, order_data):
        """Update an existing purchase order header."""
        query = """
            UPDATE PUR_ORDERS_HEAD
            SET Order_Qty = %s,
                Order_Date = %s,
                Ven_Code = %s,
                purchaseStatus = %s
            WHERE Pur_Ord_No = %s
        """
        params = (
            order_data['order_qty'],
            order_data['order_date'],
            order_data['ven_code'],
            order_data.get('purchase_status', 'Pending'),
            purchase_order_number,
        )
        return db_service.execute_query(query, params)

    @classmethod
    def update_status(cls, purchase_order_number, purchase_status):
        """Update only the status of a purchase order."""
        query = "UPDATE PUR_ORDERS_HEAD SET purchaseStatus = %s WHERE Pur_Ord_No = %s"
        return db_service.execute_query(query, (purchase_status, purchase_order_number))

    @classmethod
    def delete(cls, purchase_order_number):
        """Delete a purchase order and its transaction lines."""
        purchaseOrderTran.delete_by_purchase_order(purchase_order_number)
        delete_head = "DELETE FROM PUR_ORDERS_HEAD WHERE Pur_Ord_No = %s"
        return db_service.execute_query(delete_head, (purchase_order_number,))


class purchaseOrderTran:
    """Model for purchase order transaction lines mapped to PUR_ORDERS_TRAN.

    Mirrors SalesOrderTran in sales_order.py.
    """

    @classmethod
    def get_all(cls):
        """Get all purchase order transaction lines."""
        query = "SELECT * FROM PUR_ORDERS_TRAN ORDER BY id"
        return db_service.execute_query(query)

    @classmethod
    def get_by_id(cls, line_id):
        """Get a single transaction line by id."""
        query = "SELECT * FROM PUR_ORDERS_TRAN WHERE id = %s"
        return db_service.execute_query(query, (line_id,), fetch_one=True)

    @classmethod
    def get_by_purchase_order(cls, purchase_order_number):
        """Get all transaction lines for a purchase order."""
        query = "SELECT * FROM PUR_ORDERS_TRAN WHERE Pur_Ord_No = %s ORDER BY id"
        return db_service.execute_query(query, (purchase_order_number,))

    @classmethod
    def create(cls, line_data):
        """Add a transaction line to a purchase order.

        Expected keys in line_data: pur_ord_no, item_code, ord_rate, ord_value, order_qty, recd_qty (optional)
        """
        # Optionally compute Ord_Value to mirror sales behavior if not provided
        try:
            ord_rate = float(line_data.get('ord_rate', line_data.get('order_rate', 0)))
            order_qty = float(line_data.get('order_qty', 0))
        except (TypeError, ValueError):
            ord_rate = 0
            order_qty = 0
        ord_value = ord_rate * order_qty

        query = """
            INSERT INTO PUR_ORDERS_TRAN 
            (Ord_Rate, Ord_Value, Order_Qty, Recd_Qty, Pur_Ord_No, Item_Code)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            ord_rate,
            ord_value,
            order_qty,
            line_data.get('recd_qty', 0),
            line_data['pur_ord_no'],
            line_data['item_code'],
        )
        return db_service.execute_query(query, params)

    @classmethod
    def update(cls, line_id, line_data):
        """Update a transaction line by id."""
        try:
            ord_rate = float(line_data.get('ord_rate', line_data.get('order_rate', 0)))
            order_qty = float(line_data.get('order_qty', 0))
        except (TypeError, ValueError):
            ord_rate = 0
            order_qty = 0
        ord_value = ord_rate * order_qty

        query = """
            UPDATE PUR_ORDERS_TRAN
            SET Ord_Rate = %s,
                Ord_Value = %s,
                Order_Qty = %s,
                Recd_Qty = %s,
                Item_Code = %s
            WHERE id = %s
        """
        params = (
            ord_rate,
            ord_value,
            order_qty,
            line_data.get('recd_qty', 0),
            line_data['item_code'],
            line_id,
        )
        return db_service.execute_query(query, params)

    @classmethod
    def delete(cls, line_id):
        """Delete a transaction line by id."""
        query = "DELETE FROM PUR_ORDERS_TRAN WHERE id = %s"
        return db_service.execute_query(query, (line_id,))

    @classmethod
    def delete_by_purchase_order(cls, purchase_order_number):
        """Delete all transaction lines for a purchase order."""
        query = "DELETE FROM PUR_ORDERS_TRAN WHERE Pur_Ord_No = %s"
        return db_service.execute_query(query, (purchase_order_number,))


