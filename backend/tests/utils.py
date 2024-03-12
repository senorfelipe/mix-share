from user_api.models import User


def create_two_users(username_one='user_one', username_two='user_two') -> tuple[User, User]:
    user_one = User.objects.create(username=username_one, email=f'{username_one}@example.org')
    user_two = User.objects.create(username=username_two, email=f'{username_two}@example.org')
    return user_one, user_two
