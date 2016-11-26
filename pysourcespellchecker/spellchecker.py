"""
Spellcheck texts using `enchant`.
"""

import sys
import re

import enchant
from enchant.checker import SpellChecker as _SpellChecker
from enchant.checker.CmdLineChecker import CmdLineChecker
from enchant.tokenize import get_tokenizer
from enchant.tokenize import Filter, EmailFilter, URLFilter


class SheBangFilter(Filter):
    """Filter skipping over shebang lines for the python interpreter.
    This filter skips any words matching the following regular expression:

           ^#!/.+python.*$
    """
    _pattern = re.compile(r"^#!/.+$")

    def _skip(self, word):
        if self._pattern.match(word):
            return True
        return False


class URLFilter(URLFilter):
    _pattern = re.compile(r"^([a-zA-z]+:\/\/[^\s].*"
                          "|"
                          r"<[a-zA-z]+:\/\/[^\s].*>)")


filters_to_use = [EmailFilter, URLFilter, SheBangFilter]

RED = '\033[01;31m'
GREEN = '\033[01;32m'
COLOR_RESET = '\033[0m'


class SpellChecker(object):

    def __init__(self, language, files, pwl=None):
        self.files = files
        if pwl:
            language = enchant.DictWithPWL(language, pwl)
        self._checker = _SpellChecker(lang=language,
                                      filters=filters_to_use)

    def check(self, text, **kwargs):
        ctext = re.sub("\"|'|#|`", " ", text)

        self._checker.set_text(ctext)
        string = ''
        for err in self._checker:
            self.print_to_console(
                err.word, err.suggest(), **kwargs)
        return text

    def print_to_console(self, word, suggestions, **kwargs):
        if 'lineno' in kwargs:  # HACK
            lineno = kwargs.pop('lineno')
            string = self.files[0] + ':' + str(lineno) + ' - '
        else:
            string = ''

        for key, value in kwargs.iteritems():
            string += '%s:%s - ' % (key, value)

        # build and print colorized string
        string += RED + word
        string += COLOR_RESET + ' ==> '
        string += GREEN + str(suggestions)
        string += COLOR_RESET
        string = string.encode('utf-8')
        print string


class CmdLineSpellChecker(object):

    def __init__(self, language, pwl=None):
        if pwl:
            language = enchant.DictWithPWL(language, pwl)
        self._checker = _SpellChecker(lang=language,
                                      filters=filters_to_use)
        self.cmdln = CmdLineChecker()
        self.cmdln.set_checker(self._checker)

    def check(self, text):
        self._checker.set_text(text)
        self.cmdln.run()
        return self._checker.get_text()
