from invisibleroads_macros.database import DummyBase, UserFolderMixin


class Upload(UserFolderMixin, DummyBase):

    __tablename__ = 'upload'
