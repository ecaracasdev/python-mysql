from app import app
from utils.db import db, User

with app.app_context():
    db.create_all()
    # create a new user
    existing_user = User.query.filter_by(username='admin').first()

    # add the user only if it doesn't exist
    if not existing_user:
        user = User(username='admin', password='pbkdf2:sha256:260000$EGWshHJk$0a5e6cd3836e7e036f664fb92afca8f84623d4d2cb71bc9524f804178398ce69', fullname='Admin')
        db.session.add(user)
        db.session.commit()

if __name__ == "__main__":
   app.run(debug=True,host='0.0.0.0', port=5000)
