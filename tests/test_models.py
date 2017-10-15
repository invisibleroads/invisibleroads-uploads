from invisibleroads_uploads.models import Upload
from invisibleroads_uploads.tests import prepare_field_storage
from os import remove
from os.path import basename, dirname, join
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from pytest import fixture, raises

from conftest import CONTENT, ID_LENGTH, NAME, USER_ID


class TestUpload(object):

    def test_save(self, data_folder):
        x = Upload.save(data_folder, USER_ID, ID_LENGTH, NAME, CONTENT)
        assert x.name == NAME
        assert open(x.path, 'rt').read() == CONTENT

    def test_save_from(self, uploads_request):
        param_name = 'files[]'
        with raises(HTTPBadRequest):
            Upload.save_from(uploads_request, param_name)
        uploads_request.POST[param_name] = 'x'
        with raises(HTTPBadRequest):
            Upload.save_from(uploads_request, param_name)
        uploads_request.POST[param_name] = prepare_field_storage(NAME, CONTENT)
        x = Upload.save_from(uploads_request, param_name)
        assert x.name == NAME
        assert open(x.path, 'rt').read() == CONTENT

    def test_load_exceptions(self, data_folder, upload):
        remove(upload.path)
        with raises(IOError):
            Upload.load(data_folder, USER_ID, upload.id)
        remove(join(upload.folder, 'name.txt'))
        with raises(IOError):
            Upload.load(data_folder, USER_ID, upload.id)

    def test_load_from_with_param_name(self, uploads_request):
        param_name = 'x'
        uploads_request.POST[param_name] = prepare_field_storage(NAME, CONTENT)
        x = Upload.load_from(uploads_request, param_name)
        assert x.name == NAME
        assert open(x.path, 'rt').read() == CONTENT

    def test_load_from_with_upload_id(self, config, uploads_request, upload):
        config.testing_securitypolicy(userid=USER_ID, permissive=False)
        uploads_request.POST['upload_id'] = upload.id
        x = Upload.load_from(uploads_request)
        assert x.name == upload.name
        assert x.path == upload.path

    def test_get_from(self, config, uploads_request, upload):
        config.testing_securitypolicy(userid=USER_ID, permissive=False)
        with raises(HTTPBadRequest):
            Upload.get_from(uploads_request)
        uploads_request.params['upload_id'] = 'x'
        with raises(HTTPNotFound):
            Upload.get_from(uploads_request)
        uploads_request.params['upload_id'] = upload.id
        x = Upload.get_from(uploads_request)
        assert x.name == upload.name
        assert x.path == upload.path

    def test_spawn(self, data_folder):
        x = Upload.spawn(data_folder, owner_id=USER_ID)
        assert basename(x.folder) == '1'
        assert basename(dirname(x.folder)) == str(USER_ID)
        assert x.owner_id == USER_ID

    def test_spawn_enumerated_folder(self, data_folder):
        with raises(IOError):
            Upload.spawn_folder(data_folder, owner_id='../1')
        folder = Upload.spawn_folder(data_folder, owner_id=USER_ID)
        assert basename(folder) == '1'
        assert basename(dirname(folder)) == str(USER_ID)
        folder = Upload.spawn_folder(data_folder)
        assert basename(folder) == '1'
        assert basename(dirname(folder)) == 'anonymous'

    def test_spawn_random_folder(self, data_folder):
        with raises(IOError):
            Upload.spawn_folder(data_folder, ID_LENGTH, owner_id='../1')
        folder = Upload.spawn_folder(data_folder, ID_LENGTH, USER_ID)
        assert len(basename(folder)) == ID_LENGTH
        assert basename(dirname(folder)) == str(USER_ID)
        folder = Upload.spawn_folder(data_folder, ID_LENGTH)
        assert len(basename(folder)) == ID_LENGTH
        assert basename(dirname(folder)) == 'anonymous'

    def test_get_user_folder(self, data_folder):
        with raises(IOError):
            Upload.get_user_folder(data_folder, owner_id='../1')
        user_folder = Upload.get_user_folder(data_folder, USER_ID)
        assert basename(user_folder) == str(USER_ID)

    def test_get_folder(self, data_folder):
        record_id = 100
        with raises(IOError):
            Upload(id=record_id, owner_id='../1').get_folder(data_folder)
        folder = Upload(id=record_id, owner_id=USER_ID).get_folder(data_folder)
        assert basename(folder) == str(record_id)


@fixture
def data_folder(tmpdir):
    return str(tmpdir)
