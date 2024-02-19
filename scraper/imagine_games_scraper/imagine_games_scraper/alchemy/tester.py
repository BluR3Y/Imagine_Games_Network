from config import create_session
from models.user import User, UserConfiguration, Author, SocialMediaEntry
from models.misc import Image

session = create_session()

new_user = User(
    legacy_id = 'f0cfae0d-11c8-4e83-9db7-08be1f93560f',
    name = 'rey',
    nickname = 'blu_rey'
)
session.add(new_user)
session.commit()

user_configuration = UserConfiguration(
    user_id = new_user.id,
    privacy = 'private'
)
session.add(user_configuration)
session.commit()

author_info = Author(
    user_id = new_user.id,
    url = 'https://www.reyhector.com',
    position = 'lead software engineer',
    bio = 'big data',
    location = 'near your area',
    socials = [
        {'platform':'twitter','username':'blu_rey'},
        {'platform':'instagram','username':'blu'}
    ]
)
session.add(author_info)
session.commit()

session.close()