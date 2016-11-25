"""
Fixer for spellchecking

This extracts all strings (including unicode
strings) and comments and passes them to the spellchecker.
"""

from lib2to3 import fixer_base
from lib2to3.pygram import token
from lib2to3.fixer_util import Leaf


class FixSpellcheck(fixer_base.BaseFix):

    def match(self, node):

        def check(node, name):
            intext = getattr(node, name)
            corrected = spellchecker.check(
                intext, lineno=node.lineno)
            if corrected != intext:
                setattr(node, name, corrected)
                node.changed()

        if isinstance(node, Leaf):
            if node.prefix.strip():
                check(node, 'prefix')
            if node.type in (token.STRING, token.COMMENT):
                check(node, 'value')
