# Copyright (C) 2019 by Kevin L. Mitchell <klmitch@mit.edu>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License. You may
# obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.

from schema_res import helpers


class TestValidate(object):
    def test_base(self, mocker):
        mock_load_schema = mocker.patch.object(
            helpers.loader, 'load_schema',
        )

        helpers.validate('uri1', 'uri2', 'uri3')

        mock_load_schema.assert_has_calls([
            mocker.call('uri1', True),
            mocker.call('uri2', True),
            mocker.call('uri3', True),
        ])
