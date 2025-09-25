import imp
from flask import Blueprint, render_template, request, jsonify
from app.models.sales_order import SalesOrder
from app.models.customer import Customer
from app.models.sales_order import SalesOrderTran
from app.models.item import Item
from app.models.purchase_order import purchaseOrdersHead
from app.models.purchase_order import purchaseOrderTran
from app.models.vendor import Vendor

orders_bp = Blueprint('sales_orders', __name__, url_prefix='/order')

@orders_bp.route('/sales')
def list_sales_orders():
    """List all sales_orders"""
    try:
        sales_orders = SalesOrder.get_all()
        sales_transactions = SalesOrderTran.get_all()
        item_desc = []
        cust_names=[]
        total_amount =[]
        for order in sales_orders:
            print(order)
            cust_code = order['Cust_Code']
            customer = Customer.get_by_code(cust_code)
            cust_names.append(customer['Cust_Name'])
            Amount =0
            transactions=SalesOrderTran.get_by_id(order['Sal_Ord_No'])
            print(transactions)
            try:
                for transaction in transactions:
                    Amount+=transaction['Order_Value']
            except:
                    Amount =0
            total_amount.append(Amount) 
        for transaction in sales_transactions:
            print(transaction)
            item_code = transaction['Item_Code']
            item = Item.get_by_code(item_code)
            item_desc.append(item['item_desc'])
        return render_template('orders/sales_orders_list.html',total_amount=total_amount,sales_transactions=sales_transactions,cust_names=cust_names,sales_orders=sales_orders,item_desc=item_desc,add_url="/order/sales/addForm",view_url="/order/sales")
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/sales/addForm')
def add_sales_ordersForm():
    return render_template('forms/sales_order_form.html',add_url="/order/sales/addForm",view_url="/order/sales")

@orders_bp.route('/sales/add',methods=['POST','GET'])
def add_sales_orders():
    sales_data = request.form
    SalesOrder.create(sales_data)
    return render_template('forms/sales_order_form.html',add_url="/order/sales/addForm",view_url="/order/sales")

@orders_bp.route('/sales/addTransaction',methods=['POST','GET'])
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
    return render_template('forms/sales_order_form.html',add_url="/order/sales/addForm",view_url="/order/sales")

@orders_bp.route('/purchase')
def listPurchase():
    purchase_order= purchaseOrdersHead.get_all()
    purchase_order_items=purchaseOrderTran.get_all()
    ven_names = []
    item_desc = []
    total_amount = []
    for order in purchase_order:
        ven_code = order['Ven_Code']
        vendors = Vendor.get_by_code(ven_code)
        Amount =0
        transactions=purchaseOrderTran.get_by_purchase_order(order['Pur_Ord_No'])
        print(transactions)
        try:
            for transaction in transactions:
                Amount+=transaction['Ord_Value']
        except:
            Amount =0
        total_amount.append(Amount) 
        ven_names.append(vendors['Ven_Name'])
    for transaction in purchase_order_items:
        print(transaction)
        item_code = transaction['Item_Code']
        item = Item.get_by_code(item_code)
        item_desc.append(item['item_desc'])
    return render_template('orders/purchase_orders_list.html'
                           ,purchase_order_items=purchase_order_items,
                           purchase_order=purchase_order,  
                           total_amount=total_amount,
                           ven_names=ven_names,
                           item_desc=item_desc,
                           add_url="/order/purchase/purchaseForm",
                           view_url="/order/purchase")

@orders_bp.route('/purchase/purchaseForm')
def purchaseForm():
    return render_template('forms/purchase_order_form.html',add_url="/order/purchase/purchaseForm",view_url="/order/purchase")

@orders_bp.route('/purchase/add',methods=['POST','GET'])
def add_purchase_order():
    data = request.form
    purchaseOrdersHead.create(data)
    return render_template('forms/purchase_order_form.html',add_url="/order/purchase/purchaseForm",view_url="/order/purchase")

@orders_bp.route('/purchase/addTransaction',methods=['POST','GET'])
def add_purchase_Order_tran():
    pur_tran_data = request.form.to_dict()
    try:
        order_rate = float(pur_tran_data.get('order_rate', 0))
        order_qty = float(pur_tran_data.get('order_qty', 0))
        pur_tran_data['order_value'] = order_rate * order_qty
    except (TypeError, ValueError):
        pur_tran_data['order_value'] = 0
    purchaseOrderTran.create(pur_tran_data)
    return render_template('forms/purchase_order_form.html',add_url="/order/purchase/purchaseForm",view_url="/order/purchase")
