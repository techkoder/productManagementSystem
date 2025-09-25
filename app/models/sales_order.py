from app.services.database import db_service

class SalesOrder:
    """Model for sales order header mapped to SAL_ORDERS_HEAD."""

    @classmethod
    def get_all(cls):
        """Get all sales orders."""
        query = "SELECT * FROM SAL_ORDERS_HEAD ORDER BY Sal_Ord_No"
        return db_service.execute_query(query)

    @classmethod
    def get_by_number(cls, sales_order_number):
        """Get a single sales order by number."""
        query = "SELECT * FROM SAL_ORDERS_HEAD WHERE Sal_Ord_No = %s"
        return db_service.execute_query(query, (sales_order_number,), fetch_one=True)

    @classmethod
    def create(cls, order_data):
        """Create a new sales order header.

        Expected keys in order_data: sal_ord_no, order_qty, order_date, cust_code, sale_status (optional)
        """
        query = """
            INSERT INTO SAL_ORDERS_HEAD 
            (Sal_Ord_No, Order_Qty, Order_Date, Cust_Code, saleStatus)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            order_data['sal_ord_no'],
            order_data['order_qty'],
            order_data['order_date'],
            order_data['cust_code'],
            order_data.get('sale_status', 'Pending')
        )
        return db_service.execute_query(query, params)

    @classmethod

    def update(cls, sales_order_number, order_data):
        """Update an existing sales order header."""
        query = """
            UPDATE SAL_ORDERS_HEAD
            SET Order_Qty = %s,
                Order_Date = %s,
                Cust_Code = %s,
                saleStatus = %s
            WHERE Sal_Ord_No = %s
        """
        params = (
            order_data['order_qty'],
            order_data['order_date'],
            order_data['cust_code'],
            order_data.get('sale_status', 'Pending'),
            sales_order_number,
        )
        return db_service.execute_query(query, params)

    @classmethod
    def update_status(cls, sales_order_number, sale_status):
        """Update only the status of a sales order."""
        query = "UPDATE SAL_ORDERS_HEAD SET saleStatus = %s WHERE Sal_Ord_No = %s"
        return db_service.execute_query(query, (sale_status, sales_order_number))

    @classmethod
    def delete(cls, sales_order_number):
        """Delete a sales order and its transaction lines."""
        # Delete dependent lines first due to FK constraint
        SalesOrderTran.delete_by_sales_order(sales_order_number)
        delete_head = "DELETE FROM SAL_ORDERS_HEAD WHERE Sal_Ord_No = %s"
        return db_service.execute_query(delete_head, (sales_order_number,))


class SalesOrderTran:
    """Model for sales order transaction lines mapped to SAL_ORDERS_TRAN."""

    @classmethod
    def get_all(cls):
        """Get all sales order transaction lines."""
        query = "SELECT * FROM SAL_ORDERS_TRAN ORDER BY id"
        return db_service.execute_query(query)

    @classmethod
    def get_by_id(cls, line_id):
        """Get a single transaction line by id."""
        query = "SELECT * FROM SAL_ORDERS_TRAN WHERE id = %s"
        return db_service.execute_query(query, (line_id,), fetch_one=True)

    @classmethod
    def get_by_sales_order(cls, sales_order_number):
        """Get all transaction lines for a sales order."""
        query = "SELECT * FROM SAL_ORDERS_TRAN WHERE Sal_Ord_No = %s ORDER BY id"
        return db_service.execute_query(query, (sales_order_number,))

    @classmethod
    def create(cls, line_data):
        """Add a transaction line to a sales order.

        Expected keys in line_data: sal_ord_no, item_code, order_rate, order_value, order_qty, despatch_qty (optional)
        """
        query = """
            INSERT INTO SAL_ORDERS_TRAN 
            (Order_Rate, Order_Value, Order_Qty, Despatch_Qty, Sal_Ord_No, Item_Code)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            line_data['order_rate'],
            line_data['order_value'],
            line_data['order_qty'],
            line_data.get('despatch_qty', 0),
            line_data['sal_ord_no'],
            line_data['item_code'],
        )
        return db_service.execute_query(query, params)

    @classmethod
    def update(cls, line_id, line_data):
        """Update a transaction line by id."""
        query = """
            UPDATE SAL_ORDERS_TRAN
            SET Order_Rate = %s,
                Order_Value = %s,
                Order_Qty = %s,
                Despatch_Qty = %s,
                Item_Code = %s
            WHERE id = %s
        """
        params = (
            line_data['order_rate'],
            line_data['order_value'],
            line_data['order_qty'],
            line_data.get('despatch_qty', 0),
            line_data['item_code'],
            line_id,
        )
        return db_service.execute_query(query, params)

    @classmethod
    def delete(cls, line_id):
        """Delete a transaction line by id."""
        query = "DELETE FROM SAL_ORDERS_TRAN WHERE id = %s"
        return db_service.execute_query(query, (line_id,))

    @classmethod
    def delete_by_sales_order(cls, sales_order_number):
        """Delete all transaction lines for a sales order."""
        query = "DELETE FROM SAL_ORDERS_TRAN WHERE Sal_Ord_No = %s"
        return db_service.execute_query(query, (sales_order_number,))
