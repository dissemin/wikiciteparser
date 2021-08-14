wikiciteparser [![Build Status](https://travis-ci.com/dissemin/wikiciteparser.svg)](https://travis-ci.com/dissemin/wikiciteparser) [![PyPI](https://img.shields.io/pypi/v/wikiciteparser.svg)](https://pypi.python.org/pypi/wikiciteparser)
==============

This Python library wraps Wikipedia's citation processing code (written in Lua) to
parse citation templates. For instance, there are many different ways to specify the
authors of a citation: this codes maps all of them to the same representation.

This is the underlying code of our ["OAbot"](https://tools.wmflabs.org/oabot/) ([GitHub](https://github.com/dissemin/oabot)).

Distributed under the MIT license.

Dependencies: lupa, mwparserfromhell
To install lupa from pypi, you will need libpython and liblua (`libpython-dev` and `liblua5.2-dev` on debian-based systems).

Example
-------

Let's parse the reference section of [this article](https://en.wikipedia.org/wiki/Joachim_Lambek):

    import mwparserfromhell
    from wikiciteparser.parser import parse_citation_template
    
    mwtext = """
    ===Articles===
     * {{Citation | last1=Lambek | first1=Joachim | author1-link=Joachim Lambek | last2=Moser | first2=L. | title=Inverse and Complementary Sequences of Natural Numbers| doi=10.2307/2308078 | mr=0062777  | journal=[[American Mathematical Monthly|The American Mathematical Monthly]] | issn=0002-9890 | volume=61 | issue=7 | pages=454–458 | year=1954 | jstor=2308078 | publisher=The American Mathematical Monthly, Vol. 61, No. 7}}
     * {{Citation | last1=Lambek | first1=J. | author1-link=Joachim Lambek | title=The Mathematics of Sentence Structure | year=1958 | journal=[[American Mathematical Monthly|The American Mathematical Monthly]] | issn=0002-9890 | volume=65 | pages=154–170 | doi=10.2307/2310058 | issue=3 | publisher=The American Mathematical Monthly, Vol. 65, No. 3 | jstor=1480361}}
     *{{Citation | last1=Lambek | first1=Joachim | author1-link=Joachim Lambek | title=Bicommutators of nice injectives | doi=10.1016/0021-8693(72)90034-8 | mr=0301052  | year=1972 | journal=Journal of Algebra | issn=0021-8693 | volume=21 | pages=60–73}}
     *{{Citation | last1=Lambek | first1=Joachim | author1-link=Joachim Lambek | title=Localization and completion | doi=10.1016/0022-4049(72)90011-4 | mr=0320047  | year=1972 | journal=Journal of Pure and Applied Algebra | issn=0022-4049 | volume=2 | pages=343–370 | issue=4}}
     *{{Citation | last1=Lambek | first1=Joachim | author1-link=Joachim Lambek | title=A mathematician looks at Latin conjugation | mr=589163  | year=1979 | journal=Theoretical Linguistics | issn=0301-4428 | volume=6 | issue=2 | pages=221–234 | doi=10.1515/thli.1979.6.1-3.221}}
    """
    
    wikicode = mwparserfromhell.parse(mwtext)
    for tpl in wikicode.filter_templates():
       parsed = parse_citation_template(tpl)
       print(parsed)

Here is what you get:

    {'PublisherName': 'The American Mathematical Monthly, Vol. 61, No. 7', 'Title': 'Inverse and Complementary Sequences of Natural Numbers', 'ID_list': {'DOI': '10.2307/2308078', 'ISSN': '0002-9890', 'MR': '0062777', 'JSTOR': '2308078'}, 'Periodical': 'The American Mathematical Monthly', 'Authors': [{'link': 'Joachim Lambek', 'last': 'Lambek', 'first': 'Joachim'}, {'last': 'Moser', 'first': 'L.'}], 'Date': '1954', 'Pages': '454-458'}
    {'PublisherName': 'The American Mathematical Monthly, Vol. 65, No. 3', 'Title': 'The Mathematics of Sentence Structure', 'ID_list': {'DOI': '10.2307/2310058', 'ISSN': '0002-9890', 'JSTOR': '1480361'}, 'Periodical': 'The American Mathematical Monthly', 'Authors': [{'link': 'Joachim Lambek', 'last': 'Lambek', 'first': 'J.'}], 'Date': '1958', 'Pages': '154-170'}
    {'Title': 'Bicommutators of nice injectives', 'ID_list': {'DOI': '10.1016/0021-8693(72)90034-8', 'ISSN': '0021-8693', 'MR': '0301052'}, 'Periodical': 'Journal of Algebra', 'Authors': [{'link': 'Joachim Lambek', 'last': 'Lambek', 'first': 'Joachim'}], 'Date': '1972', 'Pages': '60-73'}
    {'Title': 'Localization and completion', 'ID_list': {'DOI': '10.1016/0022-4049(72)90011-4', 'ISSN': '0022-4049', 'MR': '0320047'}, 'Periodical': 'Journal of Pure and Applied Algebra', 'Authors': [{'link': 'Joachim Lambek', 'last': 'Lambek', 'first': 'Joachim'}], 'Date': '1972', 'Pages': '343-370'}
    {'Title': 'A mathematician looks at Latin conjugation', 'ID_list': {'DOI': '10.1515/thli.1979.6.1-3.221', 'ISSN': '0301-4428', 'MR': '589163'}, 'Periodical': 'Theoretical Linguistics', 'Authors': [{'link': 'Joachim Lambek', 'last': 'Lambek', 'first': 'Joachim'}], 'Date': '1979', 'Pages': '221-234'}



