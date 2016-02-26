# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import re
import os
import lupa
import json
import mwparserfromhell
from time import sleep
lua = lupa.LuaRuntime()

luacode = ''
luafilepath = os.path.join(os.path.dirname(__file__), 'cs1.lua')
with open(luafilepath, 'r') as f:
    luacode = f.read()

# MediaWiki utilities simulated by Python wrappers
def lua_to_python_re(regex):
    rx = re.sub('%a', '[a-zA-Z]', regex) # letters
    rx = re.sub('%c', '[\x7f\x80]', regex) # control chars
    rx = re.sub('%d', '[0-9]', rx) # digits
    rx = re.sub('%l', '[a-z]', rx) # lowercase letters
    rx = re.sub('%p', '\\p{P}', rx) # punctuation chars
    rx = re.sub('%s', '\\s', rx) # space chars
    rx = re.sub('%u', '[A-Z]', rx) # uppercase chars
    rx = re.sub('%w', '\\w', rx) # alphanumeric chars
    rx = re.sub('%x', '[0-9A-F]', rx) # hexa chars
    return rx

def ustring_match(string, regex):
    return re.match(lua_to_python_re(regex), string) is not None

def ustring_len(string):
    return len(string)

def uri_encode(string):
    return string

def text_split(string, pattern):
    return lua.table_from(re.split(lua_to_python_re(pattern), string))

def nowiki(string):
    try:
        wikicode = mwparserfromhell.parse(string)
        return wikicode.strip_code()
    except (ValueError, mwparserfromhell.parser.ParserError):
        return string

# Conversion utilities, from lua objects to python objects

def is_int(val):
    """
    Is this lua object an integer?
    """
    try:
        x = int(val)
        return True
    except (ValueError, TypeError):
        return False


wrapped_type = lua.globals().type

def toPyDict(lua_val):
    """
    Converts a lua dict to a Python one
    """
    wt = wrapped_type(lua_val)
    if wt == 'string':
        return nowiki(lua_val)
    elif wt == 'table':
        dct = {}
        lst = []
        for k, v in sorted(lua_val.items(), key=(lambda x: x[0])):
            vp = toPyDict(v)
            if not vp:
                continue
            if is_int(k):
                lst.append(vp)
            dct[k] = vp
        if lst:
            return lst
        return dct
    else:
        return lua_val

def parse_citation_template(arguments):
    """
    Parses the citation represented by the arguments provided.
    """
    lua_table = lua.table_from(arguments)
    lua_result = lua.eval(luacode)(lua_table,
            ustring_match,
            ustring_len,
            uri_encode,
            text_split,
            nowiki)
    return toPyDict(lua_result)


def parse_citation(arguments, template_name='citation'):
    """
    Parses the Wikipedia citation into a python dict.

    :param arguments: a dictionary with the arguments of the citation template
    :param template_name: the name of the template used (e.g. 'cite journal', 'citation', and so on)
    :returns: a dictionary used as internal representation in wikipedia for rendering and export to other formats
    """
    args = arguments.copy()
    args['_tpl'] = template_name
    return parse_citation_template


