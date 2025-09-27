# Product Management System

A web-based platform for managing products, vendors, customers, orders, stock, and transactions. Built using Flask, MySQL, HTML, CSS, and Jinja2.

---

## ⭐️ Features

- **Dashboard** for overview stats and low-stock alerts
- **Product, Vendor, Customer CRUD**
- **Purchase & Sales Orders:** Place, view, update, delete
- **Stock Management** with automated reorder checks
- **Production Budget & Reports**
- **Role-based Templates:** User-friendly web forms and tables

---

## 🧩 Tech Stack

- **Backend**: Python (Flask), MySQL (mysql-connector-python)
- **Frontend**: HTML, CSS, Jinja2 templates
- **Config**: Python-dotenv, config.py for flexible environments
---

## 🚀 Setup & Usage

### 1. Clone and Install

git clone https://github.com/techkoder/productManagementSystem
cd productManagementSystem
pip install -r requirements.txt


### 2. Configure Database

Edit `config.py` or create a `.env` file:
MYSQL_HOST=localhost
MYSQL_USER=techkoder
MYSQL_PASSWORD=your-password
MYSQL_DATABASE=product_management_system
MYSQL_PORT=3306


### 3. Initialize Database

Run MySQL shell and execute `database/schema.sql` to create all tables:

### 4. Launch Application

python run.py


App runs at [http://localhost:5000](http://localhost:5000).

---

## ⛏️ Core Modules

- **app/models/item.py**: Product model with CRUD, stock ops, reorder checks
- **app/routes**: Modular route code for items, vendors, customers, orders, reports (`main.py` for dashboard)
- **app/services/database**: Abstraction for SQL queries
- **config.py**: Config/ENV loader for secret keys, DB access

---

## 🛠️ API & Main Routes

- `/` or `/dashboard`: Home dashboard
- `/items`: Manage products
- `/vendors`: Manage vendors
- `/customers`: Manage customers
- `/orders`: Purchase and sales orders
- `/reports`: View and export reports

All operations available via web forms—add, view, update, and delete.

---

## future plans
- add an option to update the order transaction status.
- give the option to print the transaction bill in any format(PDF, DOCX, etc).
- show the net profit/loss in reports at month's end.
- Add a feature to notify if the stock is below the reorder level.

---
## 👤 Contributors

- [techkoder](https://github.com/techkoder)
- [nagarjun1302](https://github.com/nagarjun1302)



