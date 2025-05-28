from app import create_app, db
from app.models import Role

def init_db():
    app = create_app()
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create default roles if they don't exist
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin', description='Administrator with full access')
            db.session.add(admin_role)
        
        user_role = Role.query.filter_by(name='user').first()
        if not user_role:
            user_role = Role(name='user', description='Regular user with limited access')
            db.session.add(user_role)
        
        db.session.commit()
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db() 