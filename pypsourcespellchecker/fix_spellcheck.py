"""
Fixer for spellchecking

This extracts all strings (including unicode
strings) and comments and passes them to the spellchecker.
"""

from lib2to3 import fixer_base
from lib2to3.pygram import token
from lib2to3.fixer_util import Leaf

__author__ = "Hartmut Goebel <h.goebel@crazy-compilers.com>"
__copyright__ = "Copyright 2012 by Hartmut Goebel <h.goebel@crazy-compilers.com>"
__licence__ = "GNU Public Licence v3 (GPLv3)"


class FixSpellcheck(fixer_base.BaseFix):

    def match(self, node):
        if isinstance(node, Leaf):
            if node.prefix.strip():
                corrected = spellchecker.check(node.prefix)
                if corrected != node.prefix:
                    node.prefix = corrected
                    node.changed()
            elif node.type in (token.STRING, token.COMMENT):
                corrected = spellchecker.check(node.value)
                if corrected != node.value:
                    node.value = corrected
                    node.changed()
