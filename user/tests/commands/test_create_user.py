import pytest
import os
from unittest.mock import MagicMock
from src.commands.create_user import CreateUser
from src.errors.errors import InvalidParams, UserAlreadyExists
from src.models.model import User
from src.models.schemas import CreateUserInputSchema
from src.database import db_session
import base64
import hashlib




def test_create_user_success(mocker):
    # Mock schema validation to return no errors
    mock_schema = mocker.patch('src.commands.create_user.CreateUserInputSchema')
    mock_schema.return_value.validate.return_value = {}

    # Mock db_session to simulate no existing user
    mock_db_session = mocker.patch('src.commands.create_user.db_session')
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    # Mock db_session.add and db_session.commit methods
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()

    # Create the CreateUser instance
    command = CreateUser(
        username='test_user',
        password='password',
        email='test@example.com',
        dni='12345678A',
        fullName='Test User',
        phoneNumber='123456789'
    )
    result = command.execute()

    # Check the result
    assert 'createdAt' in result
    assert 'id' in result
    assert result['createdAt'] is None
    assert result['id'] is None

    # Optional: Check the User object passed to add
    added_user = mock_db_session.add.call_args[0][0]
    assert added_user.username == 'test_user'
    assert added_user.email == 'test@example.com'
    assert added_user.dni == '12345678A'
    assert added_user.fullName == 'Test User'
    assert added_user.phoneNumber == '123456789'

def test_create_user_invalid_params(mocker):
    # Mock schema validation to return errors
    mock_schema = mocker.patch('src.commands.create_user.CreateUserInputSchema')
    mock_schema.return_value.validate.return_value = {'username': 'required'}

    command = CreateUser(
        username='',
        password='password',
        email='test@example.com',
        dni='12345678A',
        fullName='Test User',
        phoneNumber='123456789'
    )

    with pytest.raises(InvalidParams):
        command.execute()

def test_create_user_already_exists(mocker):
    # Mock schema validation to return no errors
    mock_schema = mocker.patch('src.commands.create_user.CreateUserInputSchema')
    mock_schema.return_value.validate.return_value = {}

    # Mock db_session to simulate an existing user
    mock_user = MagicMock()
    mock_user.username = 'test_user'
    mock_user.email = 'test@example.com'

    mock_db_session = mocker.patch('src.commands.create_user.db_session')
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_user

    command = CreateUser(
        username='test_user',
        password='password',
        email='test@example.com',
        dni='12345678A',
        fullName='Test User',
        phoneNumber='123456789'
    )

    with pytest.raises(UserAlreadyExists):
        command.execute()

def test_generate_salt(mocker):
    # Test the generate_salt method directly
    salt = CreateUser.generate_salt()
    assert len(salt) == 16
    assert isinstance(salt, bytes)


def test_salt_base64_encoding():
    salt = os.urandom(16)
    salt_base64 = base64.b64encode(salt).decode('utf-8')
    
    decoded_salt = base64.b64decode(salt_base64)
    assert decoded_salt == salt

def test_commit_called(mocker):
    # Mock schema validation to return no errors
    mock_schema = mocker.patch('src.commands.create_user.CreateUserInputSchema')
    mock_schema.return_value.validate.return_value = {}

    # Mock db_session to simulate no existing user
    mock_db_session = mocker.patch('src.commands.create_user.db_session')
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    # Mock db_session.add and db_session.commit methods
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()

    # Create the CreateUser instance
    command = CreateUser(
        username='test_user',
        password='password',
        email='test@example.com',
        dni='12345678A',
        fullName='Test User',
        phoneNumber='123456789'
    )
    command.execute()

    # Check if commit is called
    mock_db_session.commit.assert_called_once()


def test_create_user_existing_user(mocker):
    # Mock schema validation to return no errors
    mock_schema = mocker.patch('src.commands.create_user.CreateUserInputSchema')
    mock_schema.return_value.validate.return_value = {}

    # Mock db_session to simulate existing user
    mock_db_session = mocker.patch('src.commands.create_user.db_session')
    existing_user = User(
        username='test_user',
        password='hashedpassword',
        email='test@example.com'
    )
    mock_db_session.query.return_value.filter.return_value.first.return_value = existing_user

    command = CreateUser(
        username='test_user',
        password='password',
        email='test@example.com',
        dni='12345678A',
        fullName='Test User',
        phoneNumber='123456789'
    )

    with pytest.raises(UserAlreadyExists):
        command.execute()
