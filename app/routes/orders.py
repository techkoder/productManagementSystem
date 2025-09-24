from flask import Blueprint, render_template, request, jsonify
from app.models.sales_order import SalesOrder
from app.models.customer import Customer
from app.models.sales_order import SalesOrderTran
from app.models.item import Item
orders_bp = Blueprint('sales_orders', __name__, url_prefix='/sales')

@orders_bp.route('/')
def list_sales_orders():
    """List all sales_orders"""
    try:
        sales_orders = SalesOrder.get_all()
        sales_transactions = SalesOrderTran.get_all()
        item_desc = []
        cust_names=[]
        for order in sales_orders:
            cust_code = order['Cust_Code']
            customer = Customer.get_by_code(cust_code)
            cust_names.append(customer['Cust_Name'])
        for transaction in sales_transactions:
            print(transaction)
            item_code = transaction['Item_Code']
            item = Item.get_by_code(item_code)
            item_desc.append(item['item_desc'])
        return render_template('orders/sales_orders_list.html',sales_transactions=sales_transactions,cust_names=cust_names,sales_orders=sales_orders,item_desc=item_desc,add_url="/sales/addForm",view_url="/sales")
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/addForm')
def add_sales_ordersForm():
    return render_template('forms/sales_order_form.html',add_url="/sales/addForm",view_url="/sales")

@orders_bp.route('/add',methods=['POST','GET'])
def add_sales_orders():
    sales_data = request.form
    SalesOrder.create(sales_data)
    return render_template('forms/sales_order_form.html',add_url="/sales/addForm",view_url="/sales")

@orders_bp.route('/addTransaction',methods=['POST','GET'])
def add_sales_Order_tran():
    sales_tran_data = request.form.to_dict()
    # Auto-calculate order_value = order_rate * order_qty (do not trust form input)
    try:
        order_rate = float(sales_tran_data.get('order_rate', 0))
        order_qty = float(sales_tran_data.get('order_qty', 0))
        sales_tran_data['order_value'] = order_rate * order_qty
    except (TypeError, ValueError):
        sales_tran_data['order_value'] = 0
    SalesOrderTran.create(sales_tran_data)
    return render_template('forms/sales_order_form.html',add_url="/sales/addForm",view_url="/sales")

