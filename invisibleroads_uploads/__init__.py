from invisibleroads_posts import get_http_expiration_time

from .views import add_routes


def includeme(config):
    configure_assets(config)
    add_routes(config)


def configure_assets(config):
    settings = config.registry.settings
    settings['website.dependencies'].append(config.package_name)
    http_expiration_time = get_http_expiration_time(settings)
    config.add_static_view(
        '_/invisibleroads-uploads', 'invisibleroads-uploads:assets',
        cache_max_age=http_expiration_time)
