from invisibleroads_uploads.models import Upload
from pytest import fixture


@fixture
def upload(data_folder):
    return Upload.save(data_folder, USER_ID, ID_LENGTH, NAME, CONTENT)


USER_ID = 1000
ID_LENGTH = 10
NAME = 'x.txt'
CONTENT = 'whee'


pytest_plugins = [
    'invisibleroads_posts.tests',
    'invisibleroads_uploads.tests',
]
