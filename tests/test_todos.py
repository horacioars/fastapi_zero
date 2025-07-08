from http import HTTPStatus

import factory
import factory.fuzzy
import pytest

from fastapi_zero.models import Todo, TodoState


def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test Todo',
            'description': 'Test todo description.',
            'state': 'draft',
        },
    )

    assert response.json() == {
        'id': 1,
        'title': 'Test Todo',
        'description': 'Test todo description.',
        'state': 'draft',
    }


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1


@pytest.mark.asyncio
async def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_should_return_2_todos(session, client, user, token):
    expected_todos = 2
    session.add_all(TodoFactory.build_batch(5, user_id=user.id))
    await session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_title_return_5_todos(
    session, client, user, token
):
    expected_todos = 5
    session.add_all(
        TodoFactory.build_batch(5, user_id=user.id, title='Test todo 1')
    )
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    response = client.get(
        '/todos/?title=Test todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_description_return_5_todos(
    session, client, user, token
):
    expected_todos = 5
    session.add_all(
        TodoFactory.build_batch(5, user_id=user.id, description='description')
    )
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    response = client.get(
        '/todos/?description=desc',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_state_return_5_todos(
    session, client, user, token
):
    expected_todos = 5
    session.add_all(
        TodoFactory.build_batch(5, user_id=user.id, state=TodoState.draft)
    )
    await session.commit()

    response = client.get(
        '/todos/?state=draft',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    await session.commit()

    response = client.delete(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Task has been deleted successfully.'
    }


def test_delete_todo_not_found(client, token):
    response = client.delete(
        '/todos/10',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found!'}


@pytest.mark.asyncio
async def test_delete_other_user_todo(
    session,
    client,
    token,
    other_user,
):
    todo_other_user = TodoFactory(user_id=other_user.id)
    session.add(todo_other_user)
    await session.commit()

    response = client.delete(
        f'/todos/{todo_other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found!'}


@pytest.mark.asyncio
async def test_patch_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    await session.commit()

    response = client.patch(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Updated Title',
            'description': 'Updated description.',
            'state': 'done',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': todo.id,
        'title': 'Updated Title',
        'description': 'Updated description.',
        'state': 'done',
    }


@pytest.mark.asyncio
async def test_patch_todo_not_found(client, token):
    response = client.patch(
        '/todos/10',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Updated Title',
            'description': 'Updated description.',
            'state': 'done',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found!'}
