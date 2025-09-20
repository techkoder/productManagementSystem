from flask import Blueprint, render_template, request, jsonify
from app.models.item import Item

items_bp = Blueprint('items', __name__, url_prefix='/items')

@items_bp.route('/')
def list_items():
    """List all items"""
    try:
        items = Item.get_all()
        return render_template('items/list.html', items=items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@items_bp.route('/api', methods=['GET'])
def api_get_items():
    """API endpoint to get all items"""
    try:
        items = Item.get_all()
        return jsonify({'items': items})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@items_bp.route('/api/<item_code>', methods=['GET'])
def api_get_item(item_code):
    """API endpoint to get single item"""
    try:
        item = Item.get_by_code(item_code)
        if item:
            return jsonify({'item': item})
        return jsonify({'error': 'Item not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@items_bp.route('/api', methods=['POST'])
def api_create_item():
    """API endpoint to create new item"""
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['item_code', 'desc', 'unit']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if item already exists
        existing_item = Item.get_by_code(data['item_code'])
        if existing_item:
            return jsonify({'error': 'Item code already exists'}), 409
        
        Item.create(data)
        return jsonify({'message': 'Item created successfully'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@items_bp.route('/api/<item_code>', methods=['PUT'])
def api_update_item(item_code):
    """API endpoint to update item"""
    try:
        data = request.get_json()
        
        # Check if item exists
        existing_item = Item.get_by_code(item_code)
        if not existing_item:
            return jsonify({'error': 'Item not found'}), 404
        
        Item.update(item_code, data)
        return jsonify({'message': 'Item updated successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@items_bp.route('/api/<item_code>', methods=['DELETE'])
def api_delete_item(item_code):
    """API endpoint to delete item"""
    try:
        # Check if item exists
        existing_item = Item.get_by_code(item_code)
        if not existing_item:
            return jsonify({'error': 'Item not found'}), 404
        
        Item.delete(item_code)
        return jsonify({'message': 'Item deleted successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@items_bp.route('/api/low-stock', methods=['GET'])
def api_low_stock_items():
    """API endpoint to get low stock items"""
    try:
        items = Item.get_low_stock_items()
        return jsonify({'items': items})
    except Exception as e:
        return jsonify({'error': str(e)}), 500