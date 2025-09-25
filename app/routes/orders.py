from flask import Blueprint, render_template, request, jsonify , flash
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
            transactions=SalesOrderTran.get_by_sales_order(order['Sal_Ord_No'])
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
        return render_template('orders/sales_orders_list.html',total_amount=total_amount,sales_transactions=sales_transactions,cust_names=cust_names,sales_orders=sales_orders,item_desc=item_desc,add_url="/order/sales/addForm",view_url="/order/sales",delete_url="/order/sales/deleteForm")
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/sales/addForm')
def add_sales_ordersForm():
    return render_template('forms/sales_order_form.html',delete_url="/order/sales/deleteForm",add_url="/order/sales/addForm",view_url="/order/sales")

@orders_bp.route('/sales/add',methods=['POST','GET'])
def add_sales_orders():
    sales_data = request.form.to_dict()
    SalesOrder.create(sales_data)
    return render_template('forms/sales_order_form.html',add_url="/order/sales/addForm",view_url="/order/sales",delete_url="/order/sales/deleteForm")

@orders_bp.route('/sales/addTransaction',methods=['POST','GET'])
def add_sales_Order_tran():
    sales_tran_data = request.form.to_dict()
    try:
        order_rate = float(sales_tran_data.get('order_rate', 0))
        order_qty = float(sales_tran_data.get('order_qty', 0))
        sales_tran_data['order_value'] = order_rate * order_qty
    except (TypeError, ValueError):
        sales_tran_data['order_value'] = 0
    SalesOrderTran.create(sales_tran_data)
    return render_template('forms/sales_order_form.html',add_url="/order/sales/addForm",view_url="/order/sales",delete_url="/order/sales/deleteForm")

@orders_bp.route('/sales/deleteForm',methods=['POST','GET'])
def deleteSalesOrderForm():
    return render_template('orders/sales_delete.html',delete_url="/order/sales/deleteForm",add_url="/order/sales/addForm",view_url="/order/sales")

@orders_bp.route('/sales/delete', methods=['POST','GET'])
def deleteSalesOrder():
    sal_ord_no = request.values.get('sal_ord_no')
    SalesOrder.delete(sal_ord_no)
    return render_template('orders/sales_delete.html',delete_url="/order/sales/deleteForm",add_url="/order/sales/addForm",view_url="/order/sales")

@orders_bp.route('/sales/deleteTransaction', methods=['POST','GET'])
def deleteSalesOrderItem():
    sal_ord_no = request.values.get('sal_ord_no')
    item_code = request.values.get('item_code')
    SalesOrderTran.delete_by_order_and_item(sal_ord_no,item_code)
    return render_template('orders/sales_delete.html',delete_url="/order/sales/deleteForm",add_url="/order/sales/addForm",view_url="/order/sales")

#Purchase Order Routes 
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
                           view_url="/order/purchase",
                           delete_url="/order/purchase/deleteForm")

@orders_bp.route('/purchase/purchaseForm')
def purchaseForm():
    return render_template('forms/purchase_order_form.html',delete_url="/order/purchase/deleteForm",add_url="/order/purchase/purchaseForm",view_url="/order/purchase")

@orders_bp.route('/purchase/add',methods=['POST','GET'])
def add_purchase_order():
    data = request.form.to_dict()
    purchaseOrdersHead.create(data)
    return render_template('forms/purchase_order_form.html',delete_url="/order/purchase/deleteForm",add_url="/order/purchase/purchaseForm",view_url="/order/purchase")

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
    return render_template('forms/purchase_order_form.html',delete_url="/order/purchase/deleteForm",add_url="/order/purchase/purchaseForm",view_url="/order/purchase")

@orders_bp.route('/purchase/deleteForm',methods=['POST','GET'])
def deletePurchaseOrderForm():
    return render_template('orders/purchase_delete.html',delete_url="/order/purchase/deleteForm",add_url="/order/purchase/purchaseForm",view_url="/order/purchase")

@orders_bp.route('/purchase/delete', methods=['POST','GET'])
def deletePurchaseOrder():
    pur_ord_no = request.values.get('pur_ord_no')
    purchaseOrdersHead.delete(pur_ord_no)
    return render_template('orders/purchase_delete.html',delete_url="/order/purchase/deleteForm",add_url="/order/purchase/purchaseForm",view_url="/order/purchase")

@orders_bp.route('/purchase/deleteTransaction', methods=['POST','GET'])
def deletePurchaseOrderItem():
    pur_ord_no = request.values.get('pur_ord_no')
    item_code = request.values.get('item_code')
    purchaseOrderTran.delete_by_order_and_item(pur_ord_no,item_code)
    return render_template('orders/purchase_delete.html',delete_url="/order/purchase/deleteForm",add_url="/order/purchase/purchaseForm",view_url="/order/purchase")
