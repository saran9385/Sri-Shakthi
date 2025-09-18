import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from models import db, Inquiry, Admin, Room
from sqlalchemy.exc import OperationalError

app = Flask(__name__)

# =======================
# Configuration
# =======================
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://srishakthidb_user:UaYdKphKpV9irglaXElOQBULuz2dwFwT@dpg-cvbv6i2n91rc73cf919g-a/srishakthidb'
)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "connect_args": {"sslmode": "require"},  # Ensure SSL
    "pool_pre_ping": True,                   # Check connections before use
    "pool_size": 5,
    "max_overflow": 10,
    "pool_recycle": 1800                     # Recycle connections after 30 min
}

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')

# Upload folder
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =======================
# Initialize DB
# =======================
db.init_app(app)

with app.app_context():
    db.create_all()


# =======================
# Helper Functions
# =======================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


# =======================
# Routes
# =======================

@app.route('/', methods=['GET', 'POST'])
def home1():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        message = request.form['message']

        new_inquiry = Inquiry(name=name, phone=phone, email=email, message=message)
        db.session.add(new_inquiry)
        db.session.commit()
        flash("We will reach out to you shortly for further steps")
        return redirect(url_for('home'))

    try:
        rooms = Room.query.limit(3).all()
    except OperationalError:
        db.session.rollback()
        rooms = Room.query.limit(3).all()

    return render_template('home.html', rooms=rooms)


@app.route('/contactform', methods=['POST'])
def contactform():
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    email = request.form.get('email', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not phone or not email or not message:
        return jsonify({'error': 'Please fill all the fields!'}), 400

    new_inquiry = Inquiry(name=name, phone=phone, email=email, message=message)
    db.session.add(new_inquiry)
    db.session.commit()
    return jsonify({'success': 'We will reach out to you shortly!'}), 200


# =======================
# Admin Routes
# =======================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):
            session['admin'] = username
            return redirect(url_for('admin_dashboard'))

        flash("Invalid credentials!", "danger")

    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))


@app.route('/admin', methods=['GET'])
def admin_dashboard():
    if 'admin' not in session:
        flash("You must be logged in to access the admin panel.", "danger")
        return redirect(url_for('admin_login'))

    try:
        inquiries = Inquiry.query.order_by(Inquiry.timestamp.desc()).all()
        rooms = Room.query.all()
    except OperationalError:
        db.session.rollback()
        inquiries = Inquiry.query.order_by(Inquiry.timestamp.desc()).all()
        rooms = Room.query.all()

    images = os.listdir(UPLOAD_FOLDER)

    return render_template('admin_panel.html', inquiries=inquiries, rooms=rooms, images=images)


@app.route('/admin/update_price', methods=['POST'])
def update_price():
    if 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    room_id = request.form.get('room_id')
    new_price = request.form.get('price')

    if not room_id or not new_price:
        return jsonify({'error': 'Missing room ID or price'}), 400

    room = Room.query.get(room_id)
    if not room:
        return jsonify({'error': 'Room not found'}), 404

    room.price = float(new_price)
    db.session.commit()
    return jsonify({'success': 'Price updated successfully'}), 200


# =======================
# File Upload Routes
# =======================
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    if 'image' not in request.files:
        return jsonify({'error': 'No file selected'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'success': 'Image uploaded successfully', 'filename': filename}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400


@app.route('/delete_image/<filename>', methods=['POST'])
def delete_image(filename):
    if 'admin' not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"success": True, "message": "Image deleted successfully"})
    else:
        return jsonify({"success": False, "error": "Image not found"}), 404


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# =======================
# Static Pages
# =======================
@app.route('/facilities')
def facilities():
    return render_template('facilities.html')


@app.route('/rooms')
def rooms():
    rooms = Room.query.all()
    return render_template('rooms.html', rooms=rooms)


@app.route('/events')
def events():
    return render_template('events.html')


@app.route('/travel')
def travel():
    return render_template('travel.html')


@app.route('/attraction')
def attraction():
    return render_template('attraction.html')


@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')


@app.route('/gallery')
def gallery():
    images = os.listdir(UPLOAD_FOLDER)
    return render_template('gallery.html', images=images)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/termsandcondition')
def termsandcondition():
    return render_template('termsandcondition.html')


@app.route('/package1')
def package1():
    return render_template('package1.html')


@app.route('/package2')
def package2():
    return render_template('package2.html')


@app.route('/package3')
def package3():
    return render_template('package3.html')


@app.route('/robots.txt')
def robots_txt():
    return app.send_static_file('robots.txt')


@app.route('/sitemap.xml')
def sitemap():
    return app.send_static_file('sitemap.xml')


# =======================
# Run the app
# =======================
if __name__ == '__main__':
    app.run(debug=True)
