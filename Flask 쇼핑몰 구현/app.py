from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'dev_secret_key_for_flask'

PRODUCTS = [
    {'id': 'P001', 'name': 'apple', 'price': 1000},
    {'id': 'P002', 'name': 'banana', 'price': 2000},
    {'id': 'P003', 'name': 'cherry', 'price': 3000},
]

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('해당 기능은 로그인이 필요합니다. 먼저 로그인해주세요.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_product_by_id(product_id):
    return next((p for p in PRODUCTS if p['id'] == product_id), None)

@app.context_processor
def inject_cart_data():
    cart_session = session.get('cart', {})
    cart_items = []
    total_price = 0
    total_quantity = 0

    for product_id, quantity in cart_session.items():
        product = get_product_by_id(product_id)
        if product:
            item_total = product['price'] * quantity
            total_price += item_total
            total_quantity += quantity
            cart_items.append({
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'quantity': quantity
            })
    return dict(global_cart_items=cart_items, global_total_price=total_price, global_total_quantity=total_quantity)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['username'] = username
            session['cart'] = {} 
            flash(f'환영합니다! 안녕하세요, {username}님! 로그인에 성공하셨습니다.', 'success')
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('cart', None)
    flash('로그아웃 되었습니다.', 'info')
    return redirect(url_for('index'))

@app.route('/products')
def products():
    return render_template('products.html', products=PRODUCTS)

# [추가] 전용 장바구니 페이지 라우트
@app.route('/cart')
@login_required
def cart_page():
    return render_template('cart.html')

@app.route('/cart/add/<product_id>')
@login_required
def add_to_cart(product_id):
    product = get_product_by_id(product_id)
    if product:
        cart = session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + 1
        session['cart'] = cart
        flash(f"[{product['name']}] 상품이 장바구니에 담겼습니다.", 'success')
    return redirect(request.referrer or url_for('products'))

# [추가] 장바구니 수량 1~99 변경 라우트
@app.route('/cart/update/<product_id>', methods=['POST'])
@login_required
def update_cart(product_id):
    cart = session.get('cart', {})
    if product_id in cart:
        try:
            # 폼에서 수량을 받아와 정수로 변환 후 1~99 사이로 제한
            new_quantity = int(request.form.get('quantity', 1))
            new_quantity = max(1, min(99, new_quantity)) 
            
            cart[product_id] = new_quantity
            session['cart'] = cart
            flash('상품 수량이 정상적으로 변경되었습니다.', 'success')
        except ValueError:
            flash('유효하지 않은 수량입니다.', 'danger')
            
    return redirect(request.referrer or url_for('cart_page'))

@app.route('/cart/remove/<product_id>')
@login_required
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if product_id in cart:
        cart.pop(product_id)
        session['cart'] = cart
        flash('상품이 장바구니에서 제거되었습니다.', 'info')
    return redirect(request.referrer or url_for('index'))

@app.route('/cart/clear')
@login_required
def clear_cart():
    session['cart'] = {}
    flash('장바구니를 모두 비웠습니다.', 'warning')
    return redirect(request.referrer or url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)