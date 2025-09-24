from flask import Blueprint, render_template, request, jsonify
from app.models.sales_order import SalesOrder

orders_bp = Blueprint('sales_orders', __name__, url_prefix='/sales')

@orders_bp.route('/')
def list_sales_orders():
    """List all sales_orders"""
    try:
        sales_orders = SalesOrder.get_all()
        return render_template('orders/sales_orders_list.html', sales_orders=sales_orders,add_url="/sales/addForm",view_url="/sales")
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/addForm')
def add_sales_ordersForm():
    return render_template('forms/sales_order_form.html',add_url="/sales/addForm",view_url="/sales")

@orders_bp.route('/add',methods=['POST','GET'])
def add_sales_orders():
    sales_data = request.form
    print(sales_data)
    SalesOrder.create(sales_data)
    sales_orders = SalesOrder.get_all()
    return render_template('orders/sales_orders_list.html',sales_orders = sales_orders,add_url="/sales/addForm",view_url="/sales")

