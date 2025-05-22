from dataclasses import asdict

from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='alice',
            email='alice@example.com',
            password='secret',
        )

        session.add(new_user)
        session.commit()

        user = session.scalar(select(User).where(User.username == 'alice'))

    assert asdict(user) == {
        'username': 'alice',
        'email': 'alice@example',
        'password': 'secret,',
        'created_at': time,
        'updated_at': time,
    }
