from flask import Blueprint, render_template, request, jsonify
from app.models.item import Item

items_bp = Blueprint('items', __name__, url_prefix='/items')

@items_bp.route('/')
def list_items():
    """List all items"""
    try:
        items = Item.get_all()
        return render_template('items/list.html', items=items,add_url="/items/addForm",view_url="/items",delete_url="/items/DeleteForm")
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@items_bp.route('/addForm')
def add_itemsForm():
    return render_template('forms/item_form.html',add_url="/items/addForm",view_url="/items",delete_url="/items/DeleteForm")

@items_bp.route('/add',methods=['POST'])
def add_items():
    Item_data = request.form
    print(Item_data)
    Item.create(Item_data)
    items = Item.get_all()
    return render_template('items/list.html',items = items,add_url="/items/addForm",view_url="/items",delete_url="/items/DeleteForm")

@items_bp.route('/DeleteForm')
def deleteCustomerForm():
    return render_template('items/delete.html',add_url="/items/addForm",view_url="/items",delete_url="/items/DeleteForm")

@items_bp.route('/delete',methods=['POST'])
def deleteCustomer():
    item_code = request.values.get('item_code')
    Item.delete(item_code)
    return render_template('items/delete.html',add_url="/items/addForm",view_url="/items",delete_url="/items/DeleteForm")