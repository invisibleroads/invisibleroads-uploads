from invisibleroads_uploads.models import Upload
from invisibleroads_uploads.tests import prepare_field_storage
from invisibleroads_uploads.views import receive_file
from pyramid.exceptions import BadCSRFToken
from pytest import raises

from conftest import CONTENT, NAME, USER_ID


class TestReceiveFile(object):

    def assert_upload(self, request):
        request.POST['files[]'] = prepare_field_storage(NAME, CONTENT)
        d = receive_file(request)
        upload = Upload.get_from(request, d['upload_id'])
        assert upload.name == NAME
        assert open(upload.path, 'rt').read() == CONTENT

    def test_accept_anonymous(self, uploads_request):
        self.assert_upload(uploads_request)

    def test_accept_authenticated(self, config, uploads_request, mocker):
        config.testing_securitypolicy(userid=USER_ID, permissive=False)
        mocker.patch(CHECK_CSRF_TOKEN).return_value = True
        self.assert_upload(uploads_request)

    def test_reject_authenticated_bad_csrf(self, config, uploads_request):
        config.testing_securitypolicy(userid=USER_ID, permissive=False)
        with raises(BadCSRFToken):
            self.assert_upload(uploads_request)


MODULE_NAME = 'invisibleroads_uploads.views'
CHECK_CSRF_TOKEN = MODULE_NAME + '.check_csrf_token'
