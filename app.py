import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, Inquiry, Admin,Room


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'postgresql://sridb_user:0WErCNp83H1fzkSSSyHwKcB9VRCzKDVV@dpg-d35u189r0fns73bfiq10-a.oregon-postgres.render.com/sridb?sslmode=require'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
# Initialize database
# with app.app_context():
#     db.create_all()
app.config['SECRET_KEY'] = 'your_secret_key'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 
db.init_app(app)


# Helper function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        print('Deleted:', filename)
        return jsonify({"success": True, "message": "Image deleted successfully"})
    else:
        return jsonify({"success": False, "error": "Image not found"}), 404

# @app.route('/gallery')
# def gallery():
#     images = os.listdir(UPLOAD_FOLDER)
#     return render_template('gallery.html', images=images)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST']) 
def home():
    if request.method == 'POST':
        name = request.form['name']
        phone=request.form['phone']
        email = request.form['email']
        message = request.form['message']
        new_inquiry = Inquiry(name=name,phone=phone, email=email, message=message)
        db.session.add(new_inquiry)
        db.session.commit()

        flash("We will reach out to you shortly for further steps")
        return redirect(url_for('home'))
        # return render_template('home.html')
    rooms = Room.query.limit(3).all() 
    return render_template('home.html', rooms=rooms)

    # return render_template('home.html')

@app.route('/contactform', methods=['POST']) 
def contactform():
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    email = request.form.get('email', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not phone or not email or not message:
        return jsonify({'error': 'Please fill all the fields!'}), 400  # Return JSON error

    new_inquiry = Inquiry(name=name, phone=phone, email=email, message=message)
    db.session.add(new_inquiry)
    db.session.commit()

    return jsonify({'success': 'We will reach out to you shortly for further steps!'}), 200  # Return JSON success

@app.route('/enquiry_form', methods=['GET', 'POST'])
def enquiry_form():
    if request.method == 'POST':
        name = request.form['name']
        phone=request.form['phone']
        email = request.form['email']
        message = request.form['message']
        if not name or not phone or not email or not message:
            return jsonify({'error': 'Please fill all the fields!'}), 400
        new_inquiry = Inquiry(name=name,phone=phone, email=email, message=message)
        db.session.add(new_inquiry)
        db.session.commit()
        return jsonify({'message': 'We will reach out to you shortly for further steps'})
        # flash("Inquiry submitted successfully!", "success")
        # return redirect(url_for('enquiry_form'))
    # return render_template('inquiry_form.html')
@app.route('/admin', methods=['GET'])
def admin_dashboard():
    if 'admin' not in session:
        flash("You must be logged in to access the admin panel.", "danger")
        return redirect(url_for('admin_login'))
    
    session.pop('_flashes', None)  # Clears flash messages after successful login

    # Fetch inquiries and rooms from the database
    inquiries = Inquiry.query.order_by(Inquiry.timestamp.desc()).all()
    rooms = Room.query.all()  # ✅ Fetch rooms

    # Ensure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    images = os.listdir(UPLOAD_FOLDER)

    return render_template('admin_panel.html', inquiries=inquiries, rooms=rooms, images=images)


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

@app.route('/home')
def home1():
    rooms = Room.query.limit(3).all()  # Fetch only the first 3 rooms
    return render_template('home.html', rooms=rooms)
@app.route('/facilities')
def facilities():
    return render_template('facilities.html')
@app.route('/rooms')
def rooms():
    rooms = Room.query.all()  # Fetch all rooms from the database
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
