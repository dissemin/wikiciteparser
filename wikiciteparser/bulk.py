"""
Helper script for extracting references from bulk mediawiki XML dumps (eg,
those from https://dumps.wikimedia.org/)

With wikiciteparser installed, run this script like::

    python3 -m wikiciteparser.bulk enwiki-20210801-pages-meta-current.xml.bz2 | pv -l | gzip > enwiki-20210801-pages-meta-current.refs.json.gz

Depending on the size of the dump, it can take a long time to process all
articles (eg, 10 revisions/second, days of processing for millions of
articles).

Output is JSON lines on stdout, with one line per page revision. JSON keys:

    site_name (eg, 'enwiki')
    page_title
    revsion_id
    refs (array of parsed references)
"""

import json
import argparse
from typing import Iterator

import mwxml
import mwtypes
import mwtypes.files
import mwparserfromhell

from .parser import parse_citation_template


def extract_revision(revision):
    # type: (mwtypes.Revision) -> dict
    meta = {}
    meta["revision_id"] = revision.id
    refs = []
    wikicode = mwparserfromhell.parse(revision.text)
    for tmpl in wikicode.filter_templates():
        parsed = parse_citation_template(tmpl)
        if parsed:
            refs.append(parsed)
    meta["refs"] = refs
    return meta


def extract_file(xml_file_path):
    # type: (str) -> Iterator[dict]
    """
    Iterate over all revisions of all pages not in a namespace from the dump.
    Yields dicts.

    If we are processing one of the 'current' dumps, there will be only one
    Revision per Page.
    """

    dump = mwxml.Dump.from_file(mwtypes.files.reader(xml_file_path))
    site_name = dump.site_info.dbname

    for page in dump.pages:
        if (page.namespace not in [0, "0"]) or page.redirect:
            # print(f"SKIPPED: [{page.namespace}] {page.title} redirect={page.redirect}", file=sys.stderr)
            continue
        for revision in page:
            if revision.deleted.text or not revision.text:
                continue
            meta = extract_revision(revision)
            meta["site_name"] = site_name
            meta["page_title"] = page.title
            yield meta


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "xml_files",
        help="input XML files to extract from. may be compessed (eg, .bz2)",
        nargs="+",
        type=str,
    )
    args = parser.parse_args()

    for xml_path in args.xml_files:
        for obj in extract_file(xml_path):
            print(json.dumps(obj))


if __name__ == "__main__":
    main()
