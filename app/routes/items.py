from flask import Blueprint, render_template, request, jsonify
from app.models.item import Item

items_bp = Blueprint('items', __name__, url_prefix='/items')

@items_bp.route('/')
def list_items():
    """List all items"""
    try:
        items = Item.get_all()
        return render_template('items/list.html', items=items,add_url="/items/addForm",view_url="/items")
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@items_bp.route('/addForm')
def add_itemsForm():
    return render_template('forms/item_form.html',add_url="/items/addForm",view_url="/items")

@items_bp.route('/add',methods=['POST'])
def add_items():
    Item_data = request.form
    print(Item_data)
    Item.create(Item_data)
    items = Item.get_all()
    return render_template('items/list.html',items = items,add_url="/items/addForm",view_url="/items")