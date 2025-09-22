from flask import Blueprint, render_template, request, jsonify
from app.models.customer import Customer

customer_bp = Blueprint('customer', __name__, url_prefix='/customers')

@customer_bp.route('/')
def list_customer():
    """List all customers"""
    try:
        customers = Customer.get_all()
        return render_template('customers/list.html', customers=customers,add_url="/customers/addForm",view_url="/customers")
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/addForm')
def add_customerForm():
    return render_template('forms/customer_form.html',add_url="/customers/addForm",view_url="/customers")

@customer_bp.route('/add', methods=['POST'])
def add_customer():
    Item_data = request.form
    print(Item_data)
    Customer.create(Item_data)
    customer = Customer.get_all()
    return render_template('customers/list.html',customer = customer)