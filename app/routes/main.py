from flask import Blueprint, render_template, jsonify
from app.models.item import Item
# from app.models.vendor import Vendor
# from app.models.customer import Customer
# from app.models.purchase_order import PurchaseOrder
# from app.models.sales_order import SalesOrder

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/dashboard')
def dashboard():
    """Dashboard with overview statistics"""
    try:
        # Get dashboard statistics
        total_items = len(Item.get_all())
        # total_vendors = len(Vendor.get_all())
        # total_customers = len(Customer.get_all())
        low_stock_items = len(Item.get_low_stock_items())
        
        # Get recent activities
        # recent_purchase_orders = PurchaseOrder.get_recent(limit=5)
        # recent_sales_orders = SalesOrder.get_recent(limit=5)
        
        dashboard_data = {
            'total_items': total_items,
            # 'total_vendors': total_vendors,
            # 'total_customers': total_customers,
            'low_stock_items': low_stock_items,
            # 'recent_purchase_orders': recent_purchase_orders,
            # 'recent_sales_orders': recent_sales_orders
        }
        
        return render_template('dashboard.html', data=dashboard_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/api/dashboard/stats')
def dashboard_stats():
    """API endpoint for dashboard statistics"""
    try:
        stats = {
            'total_items': len(Item.get_all()),
            # 'total_vendors': len(Vendor.get_all()),
            # 'total_customers': len(Customer.get_all()),
            'low_stock_items': len(Item.get_low_stock_items())
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500