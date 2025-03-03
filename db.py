# from app import app, db
# from models import Room

# # Create the database tables (only needed once)
# with app.app_context():
#     db.create_all()  # Ensure tables are created

#     # Add room details
#     room1 = Room(name="Classic Rooms", description="Enjoy a luxurious and relaxing stay in our classic rooms with premium amenities in the heart of Kanyakumari", price=150.0, image_url="https://img.freepik.com/free-photo/3d-rendering-beautiful-luxury-dark-wood-european-classic-bedroom-suite-hotel_105762-2164.jpg?ga=GA1.1.654617352.1727958446&semt=ais_hybrid")
#     room2 = Room(name="Double BedRooms", description="Experience urban elegance and modern comfort in our spacious double bedrooms.", price=100.0, image_url="https://github.com/WebDesignMastery/RayalPark_25-12-23/blob/main/assets/room-1.jpg?raw=true")
#     room3 = Room(name="Budget Rooms", description="Comfortable and affordable, our budget rooms are perfect for a cozy stay with loved ones.", price=100.0, image_url="https://img.freepik.com/free-photo/interior-modern-comfortable-hotel-room_1232-1822.jpg?ga=GA1.1.654617352.1727958446&semt=ais_hybrid")
#     room4 = Room(name="Family Rooms", description="Experience urban elegance and modern comfort in our spacious family rooms.", price=100.0, image_url="https://img.freepik.com/premium-photo/traditional-thai-style-wooden-bedroom_251764-581.jpg?ga=GA1.1.654617352.1727958446&semt=ais_hybrid")
#     room5 = Room(name="Simple Rooms", description="Cozy and comfortable, our simple rooms are perfect for a relaxing stay", price=100.0, image_url="https://img.freepik.com/free-photo/bedroom-interior_53876-32151.jpg?ga=GA1.1.654617352.1727958446&semt=ais_hybrid")
    

#     # Add to the session and commit
#     # db.session.add(room1)
#     db.session.add(room5)
#     db.session.commit()

#     print("Rooms added successfully!")


# from app import app, db
# from models import Inquiry  # Ensure 'Inquiry' is the correct model name for your 'inquiry' table

# with app.app_context():
#     # Delete all records from the inquiry table
#     db.session.query(Inquiry).delete()
#     db.session.commit()

#     print("All data from the 'inquiry' table has been deleted successfully!")
