#! /bin/python3

from OSconnectorTest import integrationTest


base_url = 'http://localhost:9013/openspecimen/rest/ng'
auth = ('admin', 'Login@123')

integration = integrationTest(base_url = base_url, auth = auth)

out_ = integration.runIntegrationTest()

print('finito')
