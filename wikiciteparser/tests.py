# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import unittest
from .parser import *

class ParsingTests(unittest.TestCase):
    def test_multiple_authors(self):
        p = parse_citation_template({"doi": "10.1111/j.1365-2486.2008.01559.x", "title": "Climate change, plant migration, and range collapse in a global biodiversity hotspot: the ''Banksia'' (Proteaceae) of Western Australia", "issue": "6", "journal": "Global Change Biology", "year": "2008", "volume": "14", "last4": "Dunn", "last1": "Fitzpatrick", "last3": "Sanders", "last2": "Gove", "first1": "Matthew C.", "first2": "Aaron D.", "first3": "Nathan J.", "first4": "Robert R.", "pages": "1\u201316", "_tpl": "cite journal"})
        self.assertEqual(p['Authors'],[{'last': 'Fitzpatrick', 'first': 'Matthew C.'}, {'last': 'Gove', 'first': 'Aaron D.'}, {'last': 'Sanders', 'first': 'Nathan J.'}, {'last': 'Dunn', 'first': 'Robert R.'}])

    def test_vauthors(self):
        p = parse_citation_template({"doi": "10.1016/s1097-2765(00)80111-2", "title": "SAP30, a component of the mSin3 corepressor complex involved in N-CoR-mediated repression by specific transcription factors", "_tpl": "cite journal", "journal": "Mol. Cell", "volume": "2", "date": "July 1998", "pmid": "9702189", "issue": "1", "pages": "33\u201342", "vauthors": "Laherty CD, Billin AN, Lavinsky RM, Yochum GS, Bush AC, Sun JM, Mullen TM, Davie JR, Rose DW, Glass CK, Rosenfeld MG, Ayer DE, Eisenman RN"})
        self.assertEqual(p['Authors'],[{'last': 'Laherty', 'first': 'CD'}, {'last': 'Billin', 'first': 'AN'}, {'last': 'Lavinsky', 'first': 'RM'}, {'last': 'Yochum', 'first': 'GS'}, {'last': 'Bush', 'first': 'AC'}, {'last': 'Sun', 'first': 'JM'}, {'last': 'Mullen', 'first': 'TM'}, {'last': 'Davie', 'first': 'JR'}, {'last': 'Rose', 'first': 'DW'}, {'last': 'Glass', 'first': 'CK'}, {'last': 'Rosenfeld', 'first': 'MG'}, {'last': 'Ayer', 'first': 'DE'}, {'last': 'Eisenman', 'first': 'RN'}])

    def test_remove_links(self):
        p = parse_citation_template({"title": "Mobile, Alabama", "url": "http://archive.org/stream/ballouspictorial1112ball#page/408/mode/2up", "_tpl": "cite journal", "journal": "[[Ballou's Pictorial Drawing-Room Companion]]", "volume": "12", "location": "Boston", "date": "June 27, 1857"})
        self.assertEqual(p['Periodical'], "Ballou's Pictorial Drawing-Room Companion")

    def test_authorlink(self):
        p = parse_citation_template({"publisher": "[[World Bank]]", "isbn": "978-0821369418", "title": "Performance Accountability and Combating Corruption", "url": "http://siteresources.worldbank.org/INTWBIGOVANTCOR/Resources/DisruptingCorruption.pdf", "_tpl": "citation", "page": "309", "last1": "Shah", "location": "[[Washington, D.C.]], [[United States|U.S.]]", "year": "2007", "first1": "Anwar", "authorlink1": "Anwar Shah", "oclc": "77116846"})
        self.assertEqual(p['Authors'], [{'link': 'Anwar Shah', 'last': 'Shah', 'first': 'Anwar'}])


