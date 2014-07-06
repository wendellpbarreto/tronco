from admin_tools.dashboard.modules import *
from fluent_dashboard.modules import *

# Icones ordenados.

class ListaAplicacoes(AppIconList):

    def init_with_context(self, context):
        if self._initialized:
            return
        items = self._visible_models(context['request'])
        apps = {}
        for model, perms in items:
            app_label = model._meta.app_label
            if app_label not in apps:
                apps[app_label] = {
                    'title': capfirst(app_label.title()),
                    'url': self._get_admin_app_list_url(model, context),
                    'models': []
                }
            model_dict = {}
            model_dict['title'] = capfirst(model._meta.verbose_name_plural)
            if perms['change']:
                model_dict['change_url'] = self._get_admin_change_url(model, context)
            if perms['add']:
                model_dict['add_url'] = self._get_admin_add_url(model, context)
            apps[app_label]['models'].append(model_dict)

        apps_sorted = apps.keys()
        #apps_sorted.sort()
        for app in apps_sorted:
            # sort model list alphabetically
            #apps[app]['models'].sort(lambda x, y: cmp(x['title'], y['title']))
            self.children.append(apps[app])

        apps = self.children

        for app in apps:
            app_name = self._get_app_name(app)
            app['name'] = app_name

            for model in app['models']:
                try:
                    model_name = self._get_model_name(model)
                    model['name'] = model_name
                    model['icon'] = self.get_icon_for_model(app_name, model_name) or appsettings.FLUENT_DASHBOARD_DEFAULT_ICON
                except ValueError:
                    model['icon'] = appsettings.FLUENT_DASHBOARD_DEFAULT_ICON

                # Automatically add STATIC_URL before relative icon paths.
                model['icon'] = self.get_icon_url(model['icon'])
                model['app_name'] = app_name

        self._initialized = True

