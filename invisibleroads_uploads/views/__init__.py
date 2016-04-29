from invisibleroads_macros.disk import make_folder
from os import environ, rename
from os.path import basename, join
from pyramid.httpexceptions import HTTPBadRequest
from shutil import copyfileobj
from tempfile import mkstemp


def add_routes(config):
    config.add_route('files.json', '/f.json')

    config.add_view(
        receive_file,
        permission='upload_file',
        renderer='json',
        request_method='POST',
        route_name='files.json')


def receive_file(request):
    try:
        source_file = request.POST['files[]'].file
    except KeyError:
        raise HTTPBadRequest
    settings = request.registry.settings
    data_folder = settings['data.folder']
    uploads_folder = make_folder(join(data_folder, 'uploads', 'links'))
    user_id = request.authenticated_userid or 0
    machine_id = environ.get('MACHINE_ID', 0)
    target_path = mkstemp(
        prefix='%s-%s-' % (user_id, machine_id),
        dir=uploads_folder)[1]
    temporary_path = target_path + '.tmp'
    with open(temporary_path, 'wb') as temporary_file:
        copyfileobj(source_file, temporary_file)
    rename(temporary_path, target_path)
    return {'id': basename(target_path).replace('%s-' % user_id, '', 1)}
