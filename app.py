from flask import Flask, render_template, request, jsonify, flash, session, redirect, url_for
import pyodbc

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

server = 'DESKTOP-A1C3D5S\SPARTA'
database = 'master'
username = 'Happy'
password = '1234'

def get_db_connection():
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    return conn

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("EXEC LoginUser_website ?,?", (username, password))
            result = cursor.fetchone()
            conn.close()

            if result and result[0] == 1:
                session['user'] = username  # Save user in session
                flash("Login Successful!", "success")
                return redirect(url_for('index')) 

            flash("Invalid username or password.", "danger")
            return redirect(url_for('login'))

        except Exception as e:
            flash("An error occurred. Please try again later.", "danger")
            print("Unexpected error:", e)
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('signup'))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("EXEC SignupUser_website ?,?,?", (username, password, email))
            result = cursor.fetchone()
            conn.commit()
            conn.close()

            if result and result[0] == -1:
                flash('Username or Email already exists. Try a different one.', 'warning')
                return redirect(url_for('signup'))
            elif result and result[0] == 1:
                flash('Signup successful! You can now log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Signup failed due to an unknown error.', 'danger')

        except Exception as e:
            print("Unexpected error:", e)
            flash("An error occurred. Please try again.", "danger")

        return redirect(url_for('signup'))

    return render_template('signup.html')


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.json
    product_name = data.get('product_name')
    price = data.get('price')
    quantity = int(data.get('quantity'))

    if 'cart' not in session:
        session['cart'] = []

    cart = session['cart']

    # Check if item already exists in cart
    for item in cart:
        if item['product_name'] == product_name:
            item['quantity'] += quantity
            break
    else:
        cart.append({'product_name': product_name, 'price': price, 'quantity': quantity})

    session['cart'] = cart  # Save cart in session
    session.modified = True  # 🔧 Ensure session updates
    return jsonify({'status': 'success', 'cart': session['cart']})


@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart=cart_items, total=total)


@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.json
    cart_items = data.get('cart', [])
    
    if not cart_items:
        return jsonify({"status": "error", "message": "Cart is empty"}), 400

    # Process payment, store order in database, etc.
    print("Processing Order:", cart_items)

    return jsonify({"status": "success"})

@app.route('/checkout')
def checkout_page():
    return render_template("checkout.html")  # Create a checkout.html file


if __name__ == "__main__":
    app.run(debug=True)