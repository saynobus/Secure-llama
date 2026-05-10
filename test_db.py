from app import db_factory, SystemConfig, User, ChatMessage, ChatSession
try:
    db = db_factory()
    print("Configs:", db.query(SystemConfig).all())
    print("Users:", db.query(User).all())
    print("Success")
except Exception as e:
    import traceback
    traceback.print_exc()
