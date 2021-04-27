#! /bin/python3
from OSconnectorTest import integrationTest


base_url = 'http://os8-0-x.silicolab.bibbox.org/openspecimen/rest/ng'
auth = ('admin', 'Login@123')

integration = integrationTest(base_url = base_url, auth = auth)

integration.runIntegrationTest()
print('finito')
