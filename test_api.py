from app import app, Session, User
import jwt, uuid
from datetime import datetime, timedelta

def test_chat():
    db = Session()
    try:
        user = db.query(User).first()
        if not user:
            user = User(id="test_user", email="operator@sentinel.ai", name="Operator")
            db.add(user)
            db.commit()

        token = jwt.encode({'user_id': user.id, 'exp': datetime.utcnow() + timedelta(days=7)}, 'sentinel-indore-ultra-jwt-secret-deep-v2-enterprise', algorithm="HS256")
        
        client = app.test_client()
        response = client.post('/api/chat', 
                               json={'message': 'hello', 'session_id': ''},
                               headers={'Authorization': f'Bearer {token}'})
        print("Status Code:", response.status_code)
        print("Response JSON:", response.json)
    except Exception as e:
        import traceback
        traceback.print_exc()
    finally:
        Session.remove()

if __name__ == '__main__':
    test_chat()
