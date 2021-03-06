from django.core.management.base import BaseCommand

from optparse import make_option

from core.models import (User, Grant, VisualizationRevision, Preference, DataStreamRevision, DatasetRevision, Role,
                         VisualizationI18n, DatastreamI18n, Account)
from core.choices import StatusChoices
import json
from django.db.models import Q


class Command(BaseCommand):

    role_migration_dict = {
        'ao-editor': 'ao-editor',
        'ao-user': '',
        'ao-viewer': '',
        'ao-member': '',
        'ao-ops': '',
        'ao-publisher-premier': 'ao-publisher',
        'ao-publisher-plus': 'ao-publisher',
        'ao-enhancer-premier': 'ao-editor',
        'ao-enhancer-plus': 'ao-editor',
        'ao-collector-premier': 'ao-editor',
        'ao-collector-plus': 'ao-editor',
        'ao-free-user': '',
        'ao-publisher': 'ao-publisher',
        'ao-enhancer': 'ao-editor',
        'ao-collector': 'ao-editor',
        'ao-account-admin': 'ao-account-admin',
    }

    option_list = BaseCommand.option_list + (
        make_option('-a', '--account',
            dest='account',
            type="string",
            help='Reindex resources'),
        )


    def chanageResourcesStatus(self, resources):
        for res in resources:
            if res.status == 2:
                res.status = StatusChoices.PENDING_REVIEW # 1
            elif res.status == 4:
                res.status = StatusChoices.DRAFT # 0
            elif res.status == 5:
                res.status = StatusChoices.DRAFT # 0
            res.save()

    def changeStatus(self):
        self.chanageResourcesStatus(self.dataset_revision_all)
        self.chanageResourcesStatus(self.datasstream_revision_all)
        self.chanageResourcesStatus(self.visualization_revision_all)

    def migrateRoles(self):
        for key, value in self.role_migration_dict.items():
            if key != value:
                try:
                    key_role = Role.objects.get(code=key)
                    value_role = Role.objects.get(code=key)
                except Role.DoesNotExist:
                    pass
                else:
                    for grant in key_role.grant_set.all():
                            Grant.objects.get_or_create(
                                user=grant.user, 
                                role=value_role, 
                                privilege=grant.privilege, 
                                guest=grant.guest)

    def migrateUserRoles(self):
        role_dict = {}
        for key, value in self.role_migration_dict.items():
            try: 
                role_dict[key]=Role.objects.get(code=key)
            except Role.DoesNotExist:
                pass

        for user in User.objects.all():
            user_codes=user.roles.all().values_list('code', flat=True)
            for code in user_codes:
                if self.role_migration_dict[code] and code != self.role_migration_dict[code]:
                    user.roles.add(role_dict[self.role_migration_dict[code]])
                    user.roles.remove(role_dict[code])

    def dataset_preferences(self):
        Preference.objects.get_or_create(account=self.account, key="account.dataset.download", value="on")
        Preference.objects.get_or_create(account=self.account, key="account.dataset.show", value="True")

    def handle(self, *args, **options):
        self.account = None

        if options['account']:
            self.account = Account.objects.get(pk=int(options['account']))

            self.visualization_revision_all = VisualizationRevision.objects.filter(user__account=self.account)
            self.dataset_revision_all = DatasetRevision.objects.filter(user__account=self.account)
            self.datasstream_revision_all = DataStreamRevision.objects.filter(user__account=self.account)
            self.users_all = User.objects.filter(account=self.account)

            self.dataset_preferences()
        else:
            self.visualization_revision_all = VisualizationRevision.objects.all()
            self.dataset_revision_all = DatasetRevision.objects.all()
            self.datasstream_revision_all = DataStreamRevision.objects.all()
            self.users_all = User.objects.all()

        for rev in self.visualization_revision_all:
            imp = json.loads(rev.impl_details)

            if 'traceSelection' in imp['chart'] and imp['chart']['traceSelection']:
                imp['chart']['geoType'] = 'traces'

            if 'latitudSelection' in imp['chart'] and 'longitudSelection' in imp['chart'] and imp['chart']['latitudSelection'] and imp['chart']['longitudSelection']:
                imp['chart']['geoType'] = 'points'

            if 'headerSelection' in imp['chart'] and imp['chart']['headerSelection'] == ",":
                imp['chart']['headerSelection'] = ''

            if 'labelSelection' in imp['chart'] and imp['chart']['labelSelection'] == ",":
                imp['chart']['labelSelection'] = ''

            if 'labelSelection' in imp['chart'] and imp['chart']['labelSelection']:
                header = imp['chart']['labelSelection'].replace(' ', '')
                answer = []
                for mh in header.split(','):
                    if ':' not in mh:
                        answer.append("%s:%s" % (mh, mh))
                    else:
                        answer.append(mh)
                imp['chart']['labelSelection'] = ','.join(answer)

            if 'headerSelection' in imp['chart'] and imp['chart']['headerSelection']:
                header = imp['chart']['headerSelection'].replace(' ', '')
                answer = []
                for mh in header.split(','):
                    if ':' not in mh:
                        answer.append("%s:%s" % (mh, mh))
                    else:
                        answer.append(mh)
                imp['chart']['headerSelection'] = ','.join(answer)

            spaces = ('latitudSelection', 'longitudSelection', 'traceSelection', 'data')

            for s in spaces:
                if s in imp['chart'] and not isinstance(imp['chart'][s], list):
                    imp['chart'][s] = imp['chart'][s].replace(' ', '')
                elif s in imp and not isinstance(imp[s], list):
                    imp[s] = imp[s].replace(' ', '')

            renames=( ("zoomLevel", "zoom"),
                ("mapCenter","center"),
            )

            for rename in renames:
                if rename[0] in imp['chart']:
                    imp['chart'][rename[1]]=imp['chart'][rename[0]]
                    imp['chart'].pop(rename[0])

            if 'headerSelection' in imp['chart'] and imp['chart']['headerSelection'] == ":":
                imp['chart']['headerSelection'] = ''

            if 'labelSelection' in imp['chart'] and imp['chart']['labelSelection'] == ":":
                imp['chart']['labelSelection'] = ''

            rev.impl_details = json.dumps(imp)

            rev.save()

            if 'invertedAxis' in imp['format']:
                if imp['format']['invertedAxis'] == 'checked':
                    if 'headerSelection' in imp['chart'].keys():
                        print "[InvertedAxis True] Account ID: %s; Revision ID: %s; headerSelection: %s; labelSelection: %s" %(self.account.id, rev.id, imp['chart']['headerSelection'], imp['chart']['labelSelection'])
                    else:
                        print "[InvertedAxis True] Account ID: %s; Revision ID: %s; headerSelection: Empty; labelSelection: %s" %(self.account.id, rev.id, imp['chart']['labelSelection'])

        # Preferencias del account.home.config.sliderSection cambiamos los type:chart a type:vz
        for home in Preference.objects.filter(Q(key="account.home")| Q(key="account.preview")):
            config = json.loads(home.value)

            try:
                if 'config' in config and 'sliderSection' in config['config'] and config['config']['sliderSection']:
                    sliderSection=[]
                    for slider in config['config']['sliderSection']:
                        sliderSection.append({u'type': slider['type'].replace("chart","vz"), u'id': slider['id']})

                    config['config']['sliderSection']=sliderSection
                home.value=json.dumps(config)
                home.save()
            except TypeError:
                pass
                
            # actualizo estados
            self.changeStatus() 
            self.migrateRoles()
            self.migrateUserRoles()

        # Creamos I18N que no existian en Junar 1
        visualization_revisions = self.visualization_revision_all.exclude(user__account__id__in=[5990, 5991])
        for visualization_revision in visualization_revisions:
            if not VisualizationI18n.objects.filter(visualization_revision=visualization_revision):
                try:
                    datastreami18n = DatastreamI18n.objects.filter(datastream_revision__datastream=visualization_revision.visualization.datastream.pk).latest('id')
                    title = datastreami18n.title
                    description = datastreami18n.description
                    notes = datastreami18n.notes
                except:
                    if visualization_revision.user.language == 'es':
                        title = 'Nombre'
                        description = 'Descripcion'
                        notes = ''
                    else:
                        title = 'Name'
                        description = 'Description'
                        notes = ''

                obj, created = VisualizationI18n.objects.get_or_create(
                    language=visualization_revision.user.language,
                    visualization_revision=visualization_revision,
                    created_at=visualization_revision.created_at,
                    title=title,
                    description=description,
                    notes=notes
                )

        # Fix de las vistas publicadas de datastreams no publicados
        visualization_revisions = self.visualization_revision_all.exclude(user__account__id__in=[5990, 5991]).filter(
                status=StatusChoices.PUBLISHED
        )

        for rev in visualization_revisions:
            if not rev.visualization.datastream.last_published_revision:
                rev.status = StatusChoices.PENDING_REVIEW
                rev.save()

                rev.visualization.last_published_revision = None
                rev.visualization.save()

        # Fix de usuarios sin Name
        for user in self.users_all:
            if not user.name:
                user.name = user.nick
                user.save()
