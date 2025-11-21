from app import db, app
from sqlalchemy import text

with app.app_context():
    # Add new columns to existing Job table
    try:
        db.session.execute(text('ALTER TABLE job ADD COLUMN requirements TEXT'))
        db.session.commit()
        print("Added requirements column")
    except Exception as e:
        print(f"Requirements column might already exist: {e}")
        db.session.rollback()

    try:
        db.session.execute(text('ALTER TABLE job ADD COLUMN benefits TEXT'))
        db.session.commit()
        print("Added benefits column")
    except Exception as e:
        print(f"Benefits column might already exist: {e}")
        db.session.rollback()

    try:
        db.session.execute(text('ALTER TABLE job ADD COLUMN is_active BOOLEAN DEFAULT 1'))
        db.session.commit()
        print("Added is_active column")
    except Exception as e:
        print(f"is_active column might already exist: {e}")
        db.session.rollback()

    try:
        db.session.execute(text('ALTER TABLE job ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP'))
        db.session.commit()
        print("Added updated_at column")
    except Exception as e:
        print(f"updated_at column might already exist: {e}")
        db.session.rollback()

    try:
        db.session.execute(text('ALTER TABLE user ADD COLUMN user_type VARCHAR(20) DEFAULT "job_seeker"'))
        db.session.commit()
        print("Added user_type column")
    except Exception as e:
        print(f"user_type column might already exist: {e}")
        db.session.rollback()

    # Create new tables
    db.create_all()
    print("Database migration completed!")
