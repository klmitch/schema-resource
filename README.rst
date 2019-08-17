================
Schema Resources
================

.. image:: https://travis-ci.org/klmitch/schema-resource.svg?branch=master
    :target: https://travis-ci.org/klmitch/schema-resource

The ``schema-resource`` package is a simple library for loading
``jsonschema`` schemas using ``pkg_resources``.  This means that
Python packages utilizing the ``schema-resource`` package can bundle
schemas for validating API or user configuration as separate files
with the package source.  Further, those schemas may then reference
other schema files within the package.

Simple Usage
============

The simplest way to use ``schema-resource`` begins by understanding
the resource URI.  A resource URI is a URI with the scheme "res".  The
"network location"--the part that appears after the "//" in a URI--is
the package name, as understood by ``pkg_resources``.  The path is
then interpreted relative to the root directory of the package.  For
instance, if the package "spam" has a schema named "schema.yaml", the
resource URI would be "res://spam/schema.yaml".  This schema can then
be loaded using ``schema_res.load_schema()``, which takes the resource
URI as its first argument; the result will be an object conforming to
the ``jsonschema.IValidator`` interface documented in the
``jsonschema`` documentation.

This schema could, of course, be loaded by using a combination of
``jsonschema`` and ``pkg_resources`` directly; however,
``schema-resource`` creates the schema with a special
``jsonschema.RefResolver`` that understands these resource URIs; this
enhancement allows one schema to refer to another, or part of another,
resource schema directly.

Class Attributes
================

Often, a class needs to use a particular schema in order to validate
input, often from an API or a configuration file.  This can be
simplified through the use of ``schema_res.SchemaDescriptor``.  This
class implements the Python "descriptor" protocol, meaning that, when
assigned to a class attribute, references to the value of the
attribute will cause a method of ``schema_res.SchemaDescriptor`` to be
called.  That method implements an on-demand loading of a schema
resource, constructing the resource URI if needed from the class's
``__module__`` attribute.  For instance, assume that the ``Spam``
class below needs to validate data fed to a class method::

    class Spam(object):
        schema = schema_res.SchemaDescriptor("spam.yaml")

        @classmethod
        def from_data(cls, data):
            cls.schema.validate(data)

            return cls(**data)

        ...

This class first validates the data against the schema loaded from the
"spam.yaml" file bundled with the package sources, loading the schema
the first time the method is called.  (The
``jsonschema.IValidator.validate()`` method raises a
``jsonschema.ValidationError`` exception if the ``data`` doesn't match
the requirements of the schema.)

Validating Schemas
==================

It is a good idea for the test suite for a package to verify that the
schemas it bundles are valid.  This could be done by simply using the
``schema_res.load_schema()`` function, calling it for each resource
URI and passing ``validate=True``, within the package's test suite.
However, there's also a simple helper: ``schema_res.validate()`` takes
one or more resource URIs and calls ``schema_res.load_schema()`` on
each, passing ``validate=True``.  This means that this entire test can
be written as a single function call, like so::

    class TestSchemas(object):
        def test_valid(self):
            schema_res.validate(
                "res://spam/schema1.yaml",
                "res://spam/schema2.yaml",
                "res://spam/schema3.yaml",
            )

Schema Format
=============

In all the examples so far, the schema filenames have had the ".yaml"
extension.  There is no specific need to use this extension, nor even
for the files to be in YAML format: JSON is a subset of YAML, so the
schema files can be written in regular JSON.  However, by using a YAML
parser to load the schema files, they may be expressed in YAML format,
which this programmer finds easier to write and to read than strict
JSON syntax.
