# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
from io import BytesIO

import pytest

from translate.storage import yaml, test_monolingual, base


class TestYAMLResourceUnit(test_monolingual.TestMonolingualUnit):
    UnitClass = yaml.YAMLUnit

    def test_getlocations(self):
        unit = self.UnitClass("teststring")
        unit.setid('some-key')
        assert unit.getlocations() == ['some-key']


class TestYAMLResourceStore(test_monolingual.TestMonolingualStore):
    StoreClass = yaml.YAMLFile

    def test_serialize(self):
        store = yaml.YAMLFile()
        store.parse('key: value')
        out = BytesIO()
        store.serialize(out)

        assert out.getvalue() == b'key: value\n'

    def test_edit(self):
        store = yaml.YAMLFile()
        store.parse('key: value')

        store.units[0].settarget('second')

        out = BytesIO()
        store.serialize(out)

        assert out.getvalue() == b'key: second\n'

    def test_edit_unicode(self):
        store = yaml.YAMLFile()
        store.parse('key: value')

        store.units[0].settarget('zkouška')

        out = BytesIO()
        store.serialize(out)

        assert out.getvalue() == 'key: zkouška\n'.encode('utf-8')

    def test_parse_unicode_list(self):
        store = yaml.YAMLFile()
        store.parse('list:\n- zkouška')

        out = BytesIO()
        store.serialize(out)

        assert out.getvalue() == 'list:\n- zkouška\n'.encode('utf-8')

    def test_ordering(self):
        store = yaml.YAMLFile()
        store.parse('''
foo: foo
bar: bar
baz: baz
''')

        assert store.units[0].source == 'foo'
        assert store.units[2].source == 'baz'

    def test_initial_comments(self):
        store = yaml.YAMLFile()
        store.parse('''
# Hello world.

foo: bar
''')

        assert store.units[0].getid() == 'foo'
        assert store.units[0].source == 'bar'

        out = BytesIO()
        store.serialize(out)

        assert out.getvalue() == b'''foo: bar
'''

    def test_string_key(self):
        store = yaml.YAMLFile()
        store.parse('''
"yes": Oficina
''')

        assert store.units[0].getid() == 'yes'
        assert store.units[0].source == 'Oficina'

        out = BytesIO()
        store.serialize(out)

        assert out.getvalue() == b''''yes': Oficina
'''

    def test_nested(self):
        store = yaml.YAMLFile()
        store.parse('''
foo:
    bar: bar
    baz:
        boo: booo


eggs: spam
''')

        assert store.units[0].getid() == 'foo / bar'
        assert store.units[0].source == 'bar'
        assert store.units[1].getid() == 'foo / baz / boo'
        assert store.units[1].source == 'booo'
        assert store.units[2].getid() == 'eggs'
        assert store.units[2].source == 'spam'

        out = BytesIO()
        store.serialize(out)

        assert out.getvalue() == b'''foo:
  bar: bar
  baz:
    boo: booo
eggs: spam
'''

    @pytest.mark.xfail(reason="Not Implemented")
    def test_multiline(self):
        """These are used in Discourse and Diaspora* translation."""
        store = yaml.YAMLFile()
        store.parse('''
invite: |-
        Ola!
        Recibiches unha invitación para unirte!


eggs: spam
''')

        assert store.units[0].getid() == 'invite'
        assert store.units[0].source == """Ola!
        Recibiches unha invitación para unirte a!"""
        assert store.units[1].getid() == 'eggs'
        assert store.units[1].source == 'spam'

        out = BytesIO()
        store.serialize(out)

        assert out.getvalue() == '''invite: |-
        Ola!
        Recibiches unha invitación para unirte!
eggs: spam
'''

    @pytest.mark.xfail(reason="Not Implemented")
    def test_boolean(self):
        store = yaml.YAMLFile()
        store.parse('''
foo: True
''')

        assert store.units[0].getid() == 'foo'
        assert store.units[0].source == 'True'

        out = BytesIO()
        store.serialize(out)

        assert out.getvalue() == b'''foo: True
'''

    @pytest.mark.xfail(reason="Not Implemented")
    def test_strings(self):
        """These are used in OpenStreeMap translation."""
        store = yaml.YAMLFile()
        store.parse('''
foo: 'quote, single'
bar: "quote, double"
eggs: No quoting at all
spam: 'avoid escaping "quote"'
''')

        assert store.units[0].getid() == 'foo'
        assert store.units[0].source == 'quote, single'
        assert store.units[1].getid() == 'bar'
        assert store.units[1].source == 'quote, double'
        assert store.units[2].getid() == 'eggs'
        assert store.units[2].source == 'No quoting at all'
        assert store.units[3].getid() == 'spam'
        assert store.units[3].source == 'avoid escaping "quote"'

        out = BytesIO()
        store.serialize(out)

        assert out.getvalue() == b'''foo: 'quote, single'
bar: "quote, double"
eggs: No quoting at all
spam: 'avoid escaping "quote"'
'''

    @pytest.mark.xfail(reason="Not Implemented")
    def test_escaped_quotes(self):
        """These are used in OpenStreeMap translation."""
        store = yaml.YAMLFile()
        store.parse('''
foo: "Hello \"World\"."
''')

        assert store.units[0].getid() == 'foo'
        assert store.units[0].source == 'Hello "World"'

        out = BytesIO()
        store.serialize(out)

        assert out.getvalue() == b'''foo: "Hello \"World\"."
'''


class TestRubyYAMLResourceStore(test_monolingual.TestMonolingualStore):
    StoreClass = yaml.RubyYAMLFile

    def test_ruby_list(self):
        data = '''en-US:
  date:
    formats:
      default: '%Y-%m-%d'
      short: '%b %d'
      long: '%B %d, %Y'
    day_names:
    - Sunday
    - Monday
    - Tuesday
    - Wednesday
    - Thursday
    - Friday
    - Saturday
'''
        store = yaml.RubyYAMLFile()
        store.parse(data)
        out = BytesIO()
        store.serialize(out)

        assert out.getvalue() == data.encode('ascii')

    def test_ruby(self):
        data = '''en:
  language_name: English
  language_name_english: English
  message:
    unsubscribe: Unsubscribe from our emails
    from_app: from %{app_name}
'''
        store = yaml.RubyYAMLFile()
        store.parse(data)

        out = BytesIO()
        store.serialize(out)

        assert out.getvalue() == data.encode('ascii')

    def test_invalid_key(self):
        store = yaml.YAMLFile()
        with pytest.raises(base.ParseError):
            store.parse('yes: string')

    def test_invalid_value(self):
        store = yaml.YAMLFile()
        with pytest.raises(base.ParseError):
            store.parse('val: "\\u string"')