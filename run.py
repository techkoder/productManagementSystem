# import flask

# app = flask.Flask(__name__)
from app import models
import os

app = models.create_app(os.environ.get('FLASK_CONFIG') or 'default')

# @app.route('/sales')
# def sales_orders():
#     return render_template('forms/sales_order_form.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
# @app.route('/')
# def dashboard():
#     return render_template('dashboard.html')

# @app.route('/items')
# def items():
#     return render_template('forms/item_form.html')

# @app.route('/items_list.html')
# def items_list():
#     return render_template('items/list.html')

# @app.route('/vendors')
# def vendors():
#     return render_template('forms/vendor_form.html')

# @app.route('/customers')
# def customers():
#     return render_template('forms/customer_form.html')

# @app.route('/purchase')
# def purchase_orders():
#     return render_template('forms/purchase_order_form.html')



# @app.route('/reports')
# def reports():
#     return render_template('reports/report.html')

# app.run(debug=True)
