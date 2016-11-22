from invisibleroads_posts.models import DummyBase
from invisibleroads_users.models import UserFolderMixin


class Upload(UserFolderMixin, DummyBase):
    pass
