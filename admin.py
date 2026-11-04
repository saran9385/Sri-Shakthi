# from app import app, db, Admin
# from werkzeug.security import generate_password_hash

# # Run inside Flask app context
# with app.app_context():
#     admin = Admin(username="admin", password=generate_password_hash("Srishakthi@123"))
#     db.session.add(admin)
#     db.session.commit()
# #     print("Admin user created successfully!")
# from app import app, db, Admin
# from werkzeug.security import check_password_hash

# with app.app_context():
#     admin_users = Admin.query.all()  # Fetch all admin users
#     for admin in admin_users:
#         print(f"ID: {admin.id}, Username: {admin.username}, Password: {admin.password}")

#     # Check password for the first admin user (or any specific user)
#     admin = Admin.query.filter_by(username="admin").first()
#     if admin:
#         entered_password = "Srishakthi@123"
#         if check_password_hash(admin.password, entered_password):
#             print("Password is correct!")
#         else:
#             print("Wrong password!")
from app import app, db, Admin
from werkzeug.security import generate_password_hash

with app.app_context():
    # Remove existing admin if needed
    admin = Admin.query.filter_by(username="admin").first()
    if admin:
        db.session.delete(admin)
        db.session.commit()

    # Create new admin with pbkdf2 hash
    hashed_pw = generate_password_hash("Srishakthi@123", method="pbkdf2:sha256", salt_length=8)
    admin = Admin(username="admin", password=hashed_pw)
    db.session.add(admin)
    db.session.commit()
    print("Admin user created successfully!")
    print(f"Stored password hash: {hashed_pw}")
