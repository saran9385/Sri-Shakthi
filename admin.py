from app import app, db, Admin
from werkzeug.security import generate_password_hash

# Run inside Flask app context
with app.app_context():
    admin = Admin(username="admin", password=generate_password_hash("Srishakthi@123"))
    db.session.add(admin)
    db.session.commit()
    print("Admin user created successfully!")
