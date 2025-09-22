from flask import Blueprint, render_template, request, jsonify
from app.models.vendor import Vendor

vendors_bp = Blueprint('vendors', __name__, url_prefix='/vendors')

@vendors_bp.route('/')
def list_vendors():
    """List all vendors"""
    try:
        vendors = Vendor.get_all()
        return render_template('vendors/list.html', vendors=vendors,add_url="/vendors/addForm",view_url="/vendors")
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@vendors_bp.route('/addForm')
def add_vendorsForm():
    return render_template('forms/vendor_form.html',add_url="/vendors/addForm",view_url="/vendors")

@vendors_bp.route('/add',methods=['POST'])
def add_vendors():
    vendor_data = request.form
    print(vendor_data)
    Vendor.create(vendor_data)
    vendors = Vendor.get_all()
    return render_template('vendors/list.html',vendors = vendors,add_url="/vendors/addForm",view_url="/vendors")