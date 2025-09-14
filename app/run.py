import flask

app = flask.Flask(__name__)

from flask import render_template

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/items')
def items():
    return render_template('forms/item_form.html')

@app.route('/items_list.html')
def items_list():
    return render_template('items/list.html')

@app.route('/vendors')
def vendors():
    return render_template('forms/vendor_form.html')

@app.route('/customers')
def customers():
    return render_template('forms/customer_form.html')

@app.route('/purchase')
def purchase_orders():
    return render_template('forms/purchase_order_form.html')

@app.route('/sales')
def sales_orders():
    return render_template('forms/sales_order_form.html')

@app.route('/reports')
def reports():
    return render_template('reports/report.html')

app.run(debug=True)
