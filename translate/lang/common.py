#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2007 Zuza Software Foundation
# 
# This file is part of translate.
#
# translate is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# translate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with translate; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""This module contains all the common features for languages.

Supported features:
language code (km, af)
language name (Khmer, Afrikaans)
Plurals
  Number of plurals (nplurals)
  Plural equation

TODO:
Ideas for possible features:

Language-Team information

Segmentation
  words
  phrases
  sentences
Punctuation
  End of sentence
  Start of sentence
  Middle of sentence
  Quotes
    single
    double

Valid characters
Accelerator characters
Special characters
Direction (rtl or ltr)
"""
class Common:
    """This class is the common parent class for all language classes."""
    
    code = ""
    fullname = ""
    # 0 is not a valid value - it must be overridden
    nplurals = 0
    pluralequation = "0"

    punctuation = u".,;:!?-@#$%^*_()[]{}/\\'\"<>‘’‚‛“”„‟′″‴‵‶‷‹›«»±³¹²°¿©®×£¥。។៕៖៘"

    def character_iter(cls, text):
        """Returns an iterator over the characters in text."""
        #We don't return more than one consecutive whitespace character
        prev = 'A'
        for c in text:
            if c.isspace() and prev.isspace():
                continue
            prev = c
            if not (c in cls.punctuation):
                yield c
    character_iter = classmethod(character_iter)

    def characters(cls, text):
        """Returns a list of characters in text."""
        return [c for c in cls.character_iter(text)]
    characters = classmethod(characters)

    def word_iter(cls, text):
        """Returns an iterator over the words in text."""
        #TODO: Consider replacing puctuation with space before split()
        for w in text.split():
            word = w.strip(cls.punctuation)
            if word:
                yield word
    word_iter = classmethod(word_iter)

    def words(cls, text):
        """Returns a list of words in text."""
        return [w for w in cls.word_iter(text)]
    words = classmethod(words)

    def sentence_iter(cls, text):
        """Returns an iterator over the senteces in text."""
        #TODO: This is very naïve. We really should consider all punctuation,
        #and return the punctuation with the sentence.
        #TODO: Search for capital letter start with next sentence to avoid
        #confusion with abbreviations. And remember Afrikaans "'n" :-)
        for s in text.split(". "):
            yield s.strip()
    sentence_iter = classmethod(sentence_iter)
            
    def sentences(cls, text):
        """Returns a list of senteces in text."""
        return [s for s in cls.sentence_iter(text)]
    sentences = classmethod(sentences)

