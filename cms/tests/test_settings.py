from cms.settings import *
import os
from django.test.runner import DiscoverRunner


class CMSTestRunner(DiscoverRunner):

    def setup_test_environment(self, *args, **kwargs):
        # insert cms_dsitrict, cms_singapore,

        super(CMSTestRunner, self).setup_test_environment(
            *args, **kwargs)

    def teardown_test_environment(self, *args, **kwargs):
        super(CMSTestRunner, self).teardown_test_environment(
            *args, **kwargs)
        # reset unmanaged models

TEST_RUNNER = 'tests.test_settings.CMSTestRunner'
