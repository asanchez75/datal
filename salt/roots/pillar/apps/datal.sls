application:
  path: /home/vagrant/app
  statics_dir: /home/vagrant/static
  cdn: ''
  api_key: ''
  public_key: ''

  settings:
    # Base Django Settings
    secret_key: '1'
    root_urlconf: 'workspace.urls'

    pagination_results_per_page: 10

    domains:
      engine: 'http://workspace'

virtualenv:
  path: /home/vagrant/env
  requirements: /home/vagrant/app/requirements.txt

searchers:
  searchify:
    api_url: ''
    index: ''

email:
    host: ''
    port: ''
    user: ''
    password: ''
    tls: True

sentry_dns: ''

bigdata:
  port: ''
  endpoint: ''
  hosts:
    - { name: ''}