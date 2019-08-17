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

from six.moves.urllib import parse as urlparse

from schema_res import loader


class SchemaDescriptor(object):
    """
    A class implementing the descriptor protocol to automatically load
    schemas from package resources.  Values are always
    ``jsonschema.IValidator`` instances, regardless of how the
    descriptor is accessed.
    """

    def __init__(self, uri_or_fname):
        """
        Initialize a ``SchemaDescriptor`` instance.

        :param str uri_or_fname: The URI or filename of the schema to
                                 load.  Only "res:"-style URIs are
                                 recognized; this cannot be used to
                                 load a schema over the network, in
                                 order to discourage that non-portable
                                 practice.  If a bare filename is
                                 provided, it will be interpreted
                                 relative to the ``__module__``
                                 attribute of the owning class.
        """

        # Save the URI
        self.uri = urlparse.urlparse(uri_or_fname)

        # Cache of the loaded schema
        self.schema = None

    def __get__(self, inst, owner):
        """
        Retrieve the specified schema object.

        :param inst: An instance of the class.  Ignored by this
                     implementation of the descriptor protocol.
        :param owner: The class containing the descriptor.

        :returns: The desired schema, loading it as necessary.
        :rtype: ``jsonschema.IValidator``
        """

        # Do we need to load the schema?
        if self.schema is None:
            # Is it a fully qualified URL?
            if self.uri.scheme:
                uri = urlparse.urlunparse(self.uri)
            else:
                uri = urlparse.urlunparse((
                    'res', owner.__module__,
                    self.uri.path, self.uri.params, self.uri.query,
                    self.uri.fragment,
                ))

            # Load the schema
            self.schema = loader.load_schema(uri)

        return self.schema
