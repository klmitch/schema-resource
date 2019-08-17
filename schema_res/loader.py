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

import jsonschema
import pkg_resources
from six.moves.urllib import parse as urlparse
import yaml


def _res_handler(uri):
    """
    Handler for "res:" URIs.  A "res:" URI resolves a resource using
    ``pkg_resources.resource_stream``; the "netloc" part of the URI
    (the part after the "res://") should be the package or
    requirement, and the "path" part of the URI will be interpreted
    relative to the top level of that package or requirement.

    :param str uri: The resource URI.

    :returns: The result of loading the URI as a YAML file (of which
              JSON is a subset).
    :rtype: ``dict`` or ``bool``
    """

    # Split the URI and extract the parts we're interested in
    urisplit = urlparse.urlparse(uri)
    if (urisplit.scheme != 'res' or not urisplit.netloc or
            urisplit.path in {'', '/'}):
        raise ValueError('invalid URI "%s"' % uri)
    pkg = urisplit.netloc
    path = urisplit.path[1:]

    # Return the result of loading the URI
    with pkg_resources.resource_stream(pkg, path) as f:
        return yaml.safe_load(f)


def load_schema(uri, validate=False):
    """
    Loads a schema from a specified resource URI.  A resource URI has
    the scheme "res:"; the "netloc" part of the URI (the part after
    the "res://") should be the package or requirement, and the "path"
    part of the URI will be interpreted relative to the top level of
    that package or requirement.  The schema is loaded as a YAML file
    (of which JSON is a subset), and an appropriate ``jsonschema``
    validator is returned.

    :param str uri: The resource URI.
    :param bool validate: If ``True``, the schema will be validated.
                          Defaults to ``False``.

    :returns: A suitable schema validator.
    :rtype: ``jsonschema.IValidator``
    """

    # Begin by loading the root schema
    sch = _res_handler(uri)

    # Construct a RefResolver
    resolver = jsonschema.RefResolver(
        uri, sch,
        handlers={'res': _res_handler},
    )

    # Pick the correct validator matching the schema
    val = jsonschema.validators.validator_for(sch)

    # Perform the schema validation
    if validate:
        val.check_schema(sch)

    # Return the constructed schema
    return val(sch, resolver=resolver)
