from src import create_app
from flask_jwt_extended import get_jwt, get_jwt_identity, create_access_token
from flask_jwt_extended import current_user
from src.extensions import db
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from src.models.models import User

app = create_app()


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(current_user)
            userId = get_jwt_identity()
            currentUser = User.query.filter_by(id=userId).first()
            if current_user:
                currentUser.access_token = access_token
                db.session.commit()
        return response
    except (RuntimeError, KeyError):
        return response


if __name__ == '__main__':
    app.run(port='5432',
            debug=True)
