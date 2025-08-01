from http import HTTPStatus

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.models import User


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession):
    new_user = User(username='alice', password='secret', email='teste@test')
    session.add(new_user)  # (1)!
    await session.commit()  # (2)!

    user = await session.scalar(
        select(User).where(User.username == 'alice')
    )  # (3)!

    assert user.username == 'alice'
    # assert asdict(user) == {
    #     'id': 1,
    #     'username': 'alice',
    #     'email': 'teste@test',
    #     'password':'secret',
    #     'created_at': time,
    #     'updated_at': time,
    #     'todos': [],
    # }


def test_get_user_should_return_not_found(client):
    response = client.get('/users/666')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


def test_get_user(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }
