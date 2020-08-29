#!/usr/bin/env python
# Copyright 2016 VMware, Inc.
# All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

import abc
import contextlib
import importlib
import inspect
import os
from os import path
import re
import shutil
import sys
import tempfile

import argparse
import six

from oslo_serialization import jsonutils

__version__ = '0.0.2'

# NOTE(boden): This is a prototype and needs additional love

_MOCK_SRC = '''
class _PyIREmptyMock_(object):

    def __init__(self, *args, **kwargs):
        self._args_ = args
        self._kwargs_ = kwargs

    def __or__(self, o):
        return o

    def __ror__(self, o):
        return o

    def __xor__(self, o):
        return o

    def __rxor__(self, o):
        return o

    def __and__(self, o):
        return o

    def __rand__(self, o):
        return o

    def __rshift__(self, o):
        return o

    def __rrshift__(self, o):
        return o

    def __lshift__(self, o):
        return o

    def __rlshift__(self, o):
        return o

    def __pow__(self, o):
        return o

    def __rpow__(self, o):
        return o

    def __divmod__(self, o):
        return o

    def __rdivmod__(self, o):
        return o

    def __mod__(self, o):
        return o

    def __rmod__(self, o):
        return o

    def __floordiv__(self, o):
        return o

    def __rfloordiv__(self, o):
        return o

    def __truediv__(self, o):
        return o

    def __rtrudiv__(self, o):
        return o

    def __add__(self, o):
        return o

    def __radd__(self, o):
        return o

    def __sub__(self, o):
        return o

    def __rsub__(self, o):
        return o

    def __mul__(self, o):
        return o

    def __rmul__(self, o):
        return o

    def __matmul__(self, o):
        return o

    def __rmatmul__(self, o):
        return o

    def __getattribute__(self, name):
        return _PyIREmptyMock_()

    def __call__(self, *args, **kwargs):
        return _PyIREmptyMock_()

    def __iter__(self):
        return [].__iter__()

    def __getitem__(self, item):
        return _PyIREmptyMock_()

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

class _PyIREmptyImport_(_PyIREmptyMock_):
    pass

'''
_MOCK_CLASS_NAME = '_PyIREmptyMock_'
_MOCK_IMPORT_CLASS_NAME = '_PyIREmptyImport_'

UNKNOWN_VAL = 'PYIR UNKNOWN VALUE'
_BLACKLIST = [re.compile(".*\.%s" % _MOCK_CLASS_NAME),
              re.compile(".*\.%s" % _MOCK_IMPORT_CLASS_NAME)]


def blacklist_filter(value):
    for pattern in _BLACKLIST:
        if pattern.match(value):
            return False
    return True


def add_blacklist_from_csv_str(csv_str):
    global _BLACKLIST
    _BLACKLIST.extend([re.compile(p)
                       for p in split_on_token(csv_str, ',')])


def for_tokens(the_str, tokens, callback):
    in_str = []
    tokens = list(tokens)
    index = 0

    def _compare_tokens(idx):
        hits = []
        for token in tokens:
            if the_str[idx:].startswith(token):
                hits.append(token)
        return hits

    for c in the_str:
        if c == '\'' or c == '\"':
            if in_str and in_str[len(in_str) - 1] == c:
                in_str.pop()
            else:
                in_str.append(c)
        elif not in_str:
            matching_tokens = _compare_tokens(index)
            if matching_tokens:
                callback(matching_tokens, index, the_str[index:])
        index += 1


def token_indexes(the_str, tokens):
    indexes = []

    def _count(toks, idx, substring):
        indexes.append(idx)

    for_tokens(the_str, tokens, _count)
    return indexes


def split_on_token(the_str, token):
    indexes = token_indexes(the_str, [token])
    if not indexes:
        return [the_str]

    strs = []
    indexes.insert(0, None)
    for start, end in zip(indexes, indexes[1:] + [None]):
        start = 0 if start is None else start + 1
        if end is None:
            end = len(the_str)
        strs.append(the_str[start:end])
    return strs


def count_tokens(the_str, tokens):
    return len(token_indexes(the_str, tokens))


def remove_tokens(the_str, tokens):
    in_str = []
    tokens = list(tokens)
    index = 0
    new_str = ''

    def _token(idx):
        for token in tokens:
            if the_str[idx:].startswith(token):
                return token
        return None

    while index < len(the_str):
        c = the_str[index]
        if c == '\'' or c == '\"':
            if in_str and in_str[len(in_str) - 1] == c:
                in_str.pop()
            else:
                in_str.append(c)
        elif not in_str:
            tok = _token(index)
            if tok:
                index += len(tok)
                continue
        new_str += c
        index += 1

    return new_str


def remove_brackets(the_str):
    return remove_tokens(the_str, ['(', ')'])


def parent_path(file_path):
    if not file_path or file_path == '/':
        return None
    return path.abspath(path.join(file_path, '..'))


def is_py_file(file_path):
    file_path = file_path if filter(blacklist_filter, [file_path]) else None
    return (file_path and
            path.isfile(file_path) and
            file_path.endswith('.py'))


def is_py_dir(dir_path):
    if not filter(blacklist_filter, [dir_path]):
        return False

    if path.isdir(dir_path):
        for f in os.listdir(dir_path):
            f = path.join(dir_path, f)
            if is_py_file(f):
                return True
    return False


def is_py_package_dir(dir_path):
    if not filter(blacklist_filter, [dir_path]):
        return False

    if path.isdir(dir_path):
        return '__init__.py' in os.listdir(dir_path)
    return False


def parent_package_names(file_or_dir_path):
    pkg_names = []
    file_or_dir_path = parent_path(file_or_dir_path)
    while file_or_dir_path:
        if is_py_package_dir(file_or_dir_path):
            pkg_names.append(os.path.basename(file_or_dir_path))
        else:
            break
        file_or_dir_path = parent_path(file_or_dir_path)
    return None if not pkg_names else reversed(pkg_names)


def whitespace(line):
    if line.isspace():
        return line, ''

    char_index = 0
    for char_index in range(len(line)):
        if not line[char_index].isspace():
            break

    return line[:char_index], line[char_index:].strip()


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def json_primitive(val):
    if isinstance(val, (str, int, bool)):
        return str(val)
    elif str(val).startswith('<') or type(val) in [dict, list, set, tuple]:
        return str(type(val))
    elif (str(val).count(_MOCK_CLASS_NAME) or
            str(val).count(_MOCK_IMPORT_CLASS_NAME)):
        return UNKNOWN_VAL
    return val


def is_mock_import(obj):
    return _MOCK_IMPORT_CLASS_NAME in str(obj)


def _member_filter(obj):
    return not inspect.isbuiltin(obj) and not inspect.ismodule(obj)


class PyFiles(object):

    def __init__(self, files):
        self._files = set(PyFiles.check_py_paths(files))

    @staticmethod
    def check_py_paths(py_paths):
        checked = []
        for f in py_paths:
            f = path.abspath(f)
            assert path.exists(f)
            if path.isfile(f):
                if not is_py_file(f):
                    raise IOError("'%s' is not a .py file." % f)
            else:
                if not is_py_package_dir(f):
                    raise IOError("'%s' doesn't contain __init__.py." % f)
            checked.append(f)
        return checked

    @property
    def files(self):
        return set(self._files)

    @property
    def has_files(self):
        return len(self._files) > 0

    def _path_to_tmp_tree(self, tree_dir, src_path):
        tree_dest = path.join(tree_dir, path.basename(src_path))
        parent_dirs = list(parent_package_names(src_path) or [])

        if parent_dirs:
            tree_dest = path.join(tree_dir, *tuple(parent_dirs))
            os.makedirs(tree_dest)
            subpath = tree_dir
            for subdir in parent_dirs:
                subpath = path.join(subpath, subdir)
                open(path.join(subpath, '__init__.py'), 'a').close()
            tree_dest = path.join(tree_dest, path.basename(src_path))

        copy_fn = shutil.copytree if path.isdir(src_path) else shutil.copyfile
        copy_fn(src_path, tree_dest)

        return tree_dest

    def to_tmp_tree(self, tree_dir=None):
        tree_dir = tree_dir or tempfile.mkdtemp()
        assert path.isdir(tree_dir)

        subtrees = []
        for f in self._files:
            subtrees.append(self._path_to_tmp_tree(tree_dir, f))

        return tree_dir, subtrees

    @contextlib.contextmanager
    def tmp_tree(self, delete_on_exit=True):
        tree = None
        try:
            tree, subtress = self.to_tmp_tree()
            yield tree
        finally:
            if tree and delete_on_exit:
                shutil.rmtree(tree)

    @staticmethod
    def filter_all_py_files(root_dir, filters):
        for child in os.listdir(root_dir):
            child_path = path.join(root_dir, child)
            if is_py_file(child_path):
                PyFile.rewrite(child_path, filters)
            elif is_py_dir(child_path):
                PyFiles.filter_all_py_files(child_path, filters)


class PyLine(object):

    def __init__(self, ws, logical_line, py_file):
        self.ws = '' if ws is None else ws
        if ws == "\n":
            self.ws = ''
        self.logical = '' if logical_line is None else logical_line
        self._py_file = py_file

    @property
    def is_str_line(self):
        return ((self.logical.startswith('\'') and
                 self.logical.endswith('\'')) or
                (self.logical.startswith('\"') and
                 self.logical.endswith('\"')))

    @property
    def is_empty_line(self):
        return len(self.logical.strip()) == 0

    @property
    def indent(self):
        return self.ws.count(' ') + (self.ws.count("\t") * 4)

    @property
    def bracket_tics(self):
        return (count_tokens(self.logical, PyLineTokens.OPEN_B) -
                count_tokens(self.logical, PyLineTokens.CLOSED_B))

    @property
    def physical_line(self):
        return str(self)

    @property
    def is_comment(self):
        return self.logical.startswith(PyLineTokens.COMMENT)

    def comment_out(self):
        if not self.is_comment:
            self.logical = PyLineTokens.COMMENT + self.logical

    @property
    def has_unmatched_brackets(self):
        return self.bracket_tics != 0

    @property
    def is_continuation(self):
        return (self.logical.endswith(PyLineTokens.BACKSLASH) or
                self.has_unmatched_brackets)

    @property
    def is_space(self):
        if self.logical == '':
            return self.ws.isspace()
        return self.logical.isspace()

    @property
    def file_path(self):
        return self._py_file.name

    @staticmethod
    def from_string_lines(lines, py_file=None):
        py_lines = []
        for l in lines:
            ws, logical = whitespace(l)
            py_lines.append(PyLine(ws, logical, py_file))
        return py_lines

    def __str__(self):
        return self.ws + self.logical


class FilterMarker(object):

    def __init__(self, filt, markers=None):
        self._filter = filt
        self.markers = markers or []

    def mark(self, line):
        if self._filter.mark(line):
            self.markers.append(line)

    def filter(self, py_file):
        for marker in self.markers:
            self._filter.filter(marker, py_file)

    def reset(self):
        self.markers = []


class PyFile(object):

    def __init__(self, py_filters):
        self._markers = []
        self._add_filters(py_filters)

        self._lines = []

    def prepend_lines(self, lines):
        lines = list(lines)
        lines.extend(self._lines)
        self._lines = lines

    def reset(self):
        self._lines = []
        for m in self._markers:
            m.reset()

    def first_line(self):
        return self._lines[0] if self._lines else None

    def next_line(self, py_line):
        if py_line not in self._lines:
            return None
        index = self._lines.index(py_line) + 1
        if index >= len(self._lines):
            return None
        return self._lines[index]

    def prev_line(self, py_line):
        if py_line not in self._lines:
            return None
        index = self._lines.index(py_line) - 1
        if index <= 0:
            return None
        return self._lines[index]

    def del_line(self, py_line):
        self._lines.remove(py_line)

    def get_line(self, py_line):
        return (None if not self.contains_line(py_line)
                else self._lines[self._lines.index(py_line)])

    def contains_line(self, py_line):
        return py_line in self._lines

    def _add_filters(self, filters):
        self._markers.extend([FilterMarker(f) for f in filters])

    def _mark_line_filter(self, line):
        for marker in self._markers:
            marker.mark(line)

    def load_path(self, py_path):
        with open(py_path, 'r') as py_file:
            for line in py_file:
                ws, logical = whitespace(line)
                line = PyLine(ws, logical, py_file)
                self._lines.append(line)
                self._mark_line_filter(line)

    def filter(self):
        if not self._lines or not self._markers:
            return None

        for marker in self._markers:
            marker.filter(self)

    def insert_after(self, py_line, py_line_to_add):
        if py_line not in self._lines:
            return False
        self._lines.insert(self._lines.index(py_line) + 1, py_line_to_add)
        return True

    def to_file_str(self):
        buff = ''
        for line in self._lines:
            buff += str(line) + "\n"
        return buff

    def save(self, py_path):
        with open(py_path, 'w') as py_file:
            py_file.write(self.to_file_str())

    @staticmethod
    def filter_to_file_str(py_path, filters):
        py_file = PyFile(filters)
        py_file.load_path(py_path)
        py_file.filter()
        return py_file.to_file_str()

    @staticmethod
    def rewrite(py_path, filters):
        py_file = PyFile(filters)
        py_file.load_path(py_path)
        py_file.filter()
        py_file.save(py_path)


class ImportParser(object):

    def __init__(self):
        self.names = []
        self.modules = []

    def _segs(self, the_str, token=' '):
        return [s.strip() for s in the_str.split(token)
                if s and not s.isspace()]

    def _lstrip(self, the_str, to_strip):
        return the_str[len(to_strip):].strip()

    def _next_token(self, the_str, delim=' ', strip=True):
        try:
            idx = the_str.index(delim)
            content = the_str[:idx]
            remainder = the_str[idx:]
            if strip:
                content.strip()
                remainder.strip()
            return content, remainder

        except ValueError:
            return None, None

    def _parse_from(self, import_str):
        import_str = self._lstrip(import_str, 'from ')
        module_name, import_str = self._next_token(import_str)
        import_str = self._lstrip(import_str, 'import ')

        for name_def in self._segs(import_str, token=','):
            if name_def.count(' as '):
                segs = self._segs(name_def, token=' as ')
                self.names.append(segs[1])
                self.modules.append(module_name + '.' + segs[0])
            else:
                self.names.extend(self._segs(name_def, '.'))
                self.modules.append(module_name)

    def _parse_import(self, import_str):
        import_str = self._lstrip(import_str, 'import ')

        for name_def in self._segs(import_str, token=','):
            if name_def.count(' as '):
                segs = self._segs(name_def, token=' as ')
                self.names.append(segs[1])
                self.modules.append(segs[0])
            else:
                self.names.extend(self._segs(name_def, '.'))
                self.modules.append(name_def)

    def reset(self):
        self.names = []
        self.modules = []

    def is_statement(self, import_str):
        return import_str.startswith(('import ', 'from ', ))

    def parse(self, import_str):
        self.reset()

        import_str = import_str.replace('(', '').replace(')', '')

        if import_str.startswith('import '):
            self._parse_import(import_str)
        elif import_str.startswith('from '):
            self._parse_from(import_str)
        else:
            raise IOError("Invalid import string: %s" % import_str)
        return self


class PyLineTokens(object):
    COMMENT = '#'
    BACKSLASH = '\\'
    DECORATOR = '@'
    OPEN_B = '('
    CLOSED_B = ')'


class AbstractFilter(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def mark(self, py_line):
        pass

    @abc.abstractmethod
    def filter(self, py_line, py_file):
        pass


class AbstractPerFileFilter(AbstractFilter, metaclass=abc.ABCMeta):

    def __init__(self):
        self._marked = []

    def mark(self, py_line):
        if py_line.file_path not in self._marked:
            self._marked.append(py_line.file_path)
            return True
        return False

    @abc.abstractmethod
    def _filter(self, py_line, py_file):
        pass

    def filter(self, py_line, py_file):
        if py_line.file_path not in self._marked:
            return
        self._marked.remove(py_line.file_path)
        return self._filter(py_line, py_file)


class CommentOutDecorators(AbstractFilter):

    def mark(self, py_line):
        if py_line.is_str_line:
            return False

        if py_line.logical.startswith(PyLineTokens.DECORATOR):
            return True
        return False

    def filter(self, py_line, py_file):
        if not py_file.get_line(py_line):
            return

        py_line.comment_out()


class StripTrailingComments(AbstractFilter):

    _RE = re.compile('^([^#]*)#(.*)$')

    def mark(self, py_line):
        if (py_line.is_str_line or
                not count_tokens(py_line.logical, PyLineTokens.COMMENT)):
            return False

        m = StripTrailingComments._RE.match(py_line.logical)
        return True if m else False

    def filter(self, py_line, py_file):
        if not py_file.get_line(py_line):
            return

        m = StripTrailingComments._RE.match(py_line.logical)
        py_line.logical = m.group(1).strip()


class AddMockDefinitions(AbstractPerFileFilter):

    _LINES = PyLine.from_string_lines(_MOCK_SRC.split("\n"))

    def _filter(self, py_line, py_file):
        py_file.prepend_lines(AddMockDefinitions._LINES)


class PassEmptyDef(AbstractPerFileFilter):

    def _has_body(self, def_py_line, py_file):
        indent = def_py_line.indent
        line = py_file.next_line(def_py_line)
        while line:
            if line.is_empty_line:
                line = py_file.next_line(line)
                continue
            elif line.indent > indent:
                return True
            elif line.indent <= indent:
                return False
            else:
                line = py_file.next_line(line)

        return False

    def _filter(self, py_line, py_file):
        line = py_file.first_line()
        while line:
            if (line.logical.startswith(('class ', 'def ',)) and
                    not self._has_body(line, py_file)):
                pass_line = PyLine(line.ws + "    ", 'pass', py_file)
                py_file.insert_after(line, pass_line)
                line = py_file.next_line(pass_line)
            else:
                line = py_file.next_line(line)


class RemoveDocStrings(AbstractPerFileFilter):

    _COMMENT = '"""'

    def _comment_count(self, py_line):
        return count_tokens(py_line.logical, RemoveDocStrings._COMMENT)

    def _safe_delete_line(self, py_line, py_file):
        if py_line.logical.endswith((',', ')',)):
            return
        py_file.del_line(py_line)

    def _filter(self, py_line, py_file):
        in_comment = False
        last_line = line = py_file.first_line()
        while line:
            comment_count = self._comment_count(line)
            if comment_count:
                if in_comment:
                    in_comment = False
                elif comment_count == 1:
                    in_comment = True
                py_file.del_line(line)
            elif in_comment:
                py_file.del_line(line)

            if not py_file.contains_line(line):
                if not py_file.contains_line(last_line):
                    last_line = line = py_file.first_line()
                else:
                    line = py_file.next_line(last_line)
            else:
                next_line = py_file.next_line(line)
                last_line = line
                line = next_line


class RemoveCommentLines(AbstractFilter):

    def mark(self, py_line):
        return py_line.logical.startswith(PyLineTokens.COMMENT)

    def filter(self, py_line, py_file):
        py_line = py_file.get_line(py_line)
        if py_line and self.mark(py_line):
            py_file.del_line(py_line)


class AbstractMultiLineCollector(AbstractFilter, metaclass=abc.ABCMeta):

    def __init__(self):
        self._comment_stripper = StripTrailingComments()

    def _strip_backslash(self, py_line):
        if py_line.logical.endswith(PyLineTokens.BACKSLASH):
            py_line.logical = py_line.logical[:-1].strip()
            return True
        return False

    def _collect(self, py_line, py_file, continue_fn):
        self._strip_backslash(py_line)
        next_line = py_file.next_line(py_line)

        while next_line:
            if not next_line.is_comment:
                if self._comment_stripper.mark(next_line):
                    self._comment_stripper.filter(next_line, py_file)
                if not next_line.is_space:
                    py_line.logical += ' ' + next_line.logical

            py_file.del_line(next_line)

            if continue_fn(py_line):
                next_line = py_file.next_line(py_line)
                continue
            else:
                break

    def _collect_backslash(self, py_line, py_file):
        self._strip_backslash(py_line)
        self._collect(py_line, py_file, self._strip_backslash)

    def _collect_brackets(self, py_line, py_file):
        self._collect(py_line, py_file, lambda l: l.has_unmatched_brackets)

    def filter(self, py_line, py_file):
        if py_line.logical.endswith(PyLineTokens.BACKSLASH):
            self._collect_backslash(py_line, py_file)
        else:
            self._collect_brackets(py_line, py_file)


class MergeMultiLineImports(AbstractMultiLineCollector):

    def mark(self, py_line):
        if py_line.is_str_line:
            return False

        logical = py_line.logical
        return (logical.startswith(('import ', 'from ',)) and
                py_line.is_continuation)

    def filter(self, py_line, py_file):
        super(MergeMultiLineImports, self).filter(py_line, py_file)
        py_line.logical = remove_brackets(py_line.logical)


class MergeMultiLineClass(AbstractMultiLineCollector):

    def mark(self, py_line):
        if py_line.is_str_line:
            return False
        return py_line.logical.startswith('class ') and py_line.is_continuation


class MergeMultiLineDef(AbstractMultiLineCollector):

    def mark(self, py_line):
        if py_line.is_str_line:
            return False
        return py_line.logical.startswith('def ') and py_line.is_continuation


class MergeMultiLineDecorator(AbstractMultiLineCollector):

    def mark(self, py_line):
        if py_line.is_str_line:
            return False
        return (py_line.logical.startswith(PyLineTokens.DECORATOR) and
                py_line.is_continuation)


class MockParentClass(AbstractFilter):

    _PARENT_RE = re.compile('class \w*\((.*)\)\:$')

    def mark(self, py_line):
        return (py_line.logical.startswith('class ') and
                not py_line.is_str_line)

    def filter(self, py_line, py_file):
        if not py_file.get_line(py_line):
            return

        m = MockParentClass._PARENT_RE.match(py_line.logical)
        if m:
            py_line.logical = py_line.logical.replace(
                "(%s):" % m.group(1), "(%s):" % _MOCK_CLASS_NAME)


class MockImports(AbstractFilter):

    def __init__(self):
        self._parser = ImportParser()

    def mark(self, py_line):
        return self._parser.is_statement(remove_brackets(py_line.logical))

    def filter(self, py_line, py_file):
        if not py_file.contains_line(py_line) or not self.mark(py_line):
            return

        py_line.logical = remove_brackets(py_line.logical)
        self._parser.parse(py_line.logical)

        if '*' in self._parser.names:
            inferred_names = []
            for module in self._parser.modules:
                if not module.startswith('.'):
                    inferred_names.extend(module.split('.'))
            self._parser.names = inferred_names

        if not self._parser.names:
            py_line.comment_out()
            return

        py_line.logical = ', '.join(self._parser.names) + ' = ' + ', '.join(
            [_MOCK_IMPORT_CLASS_NAME + '()' for n in self._parser.names])

        if '_' in self._parser.names:
            # TODO(boden): one off
            mock_translate = PyLine(py_line.ws, '_ = lambda s: str(s)',
                                    py_file)
            py_file.insert_after(py_line, mock_translate)


class APISignature(object):

    class SignatureType(object):
        CLASS = 'class'
        FUNCTION = 'function'
        METHOD = 'method'
        CLASS_ATTR = 'class_attribute'
        MODULE_ATTR = 'module_attribute'

    def __init__(self, signature_type, qualified_name, member, arg_spec):
        self.signature_type = signature_type
        self.qualified_name = qualified_name
        self.member = member
        self.arg_spec = arg_spec

    def to_dict(self):
        defaults = ([json_primitive(d) for d in self.arg_spec.defaults]
                    if self.arg_spec.defaults else None)
        return {
            'member_type': self.signature_type,
            'qualified_name': self.qualified_name,
            'member_value': json_primitive(self.member),
            'arg_spec': {
                'args': self.arg_spec.args,
                'varargs': self.arg_spec.varargs,
                'keywords': self.arg_spec.keywords,
                'defaults': defaults
            }
        }

    @staticmethod
    def arg_spec_from_dict(arg_spec_dict):
        defaults = arg_spec_dict['defaults']
        if defaults is not None:
            defaults = tuple(defaults)
        return inspect.ArgSpec(arg_spec_dict['args'],
                               arg_spec_dict['varargs'],
                               arg_spec_dict['keywords'],
                               defaults)

    @staticmethod
    def from_dict(api_dict):
        return APISignature(
            api_dict['member_type'],
            api_dict['qualified_name'],
            api_dict['member_value'],
            APISignature.arg_spec_from_dict(api_dict['arg_spec']))

    @property
    def signature(self):
        return self._build_signature(self.to_dict())

    @staticmethod
    def get_signature(signature):
        if isinstance(signature, dict):
            signature = APISignature.from_dict(signature)
        return signature.signature

    def _build_callable_signature(self, signature_dict):
        arg_spec = signature_dict['arg_spec']
        arg_str = ''
        defaults = arg_spec['defaults'] or []
        named_args = arg_spec['args'] or []
        named_kwargs = []

        if defaults:
            named_args = arg_spec['args'][:-len(defaults)]
            named_kwargs = arg_spec['args'][-len(defaults):]

        if named_args:
            arg_str += ", ".join(named_args)
        if named_kwargs:
            kw_args = []
            for kw_name, kw_default in zip(named_kwargs, defaults):
                kw_args.append("%s=%s" % (kw_name, kw_default))
            arg_str += ", %s" % ", ".join(kw_args)
        if arg_spec['varargs'] is not None:
            arg_str = "*%s%s" % (arg_spec['varargs'],
                                 '' if not arg_str else ', ' + arg_str)
        if arg_spec['keywords'] is not None:
            arg_str += "%s**%s" % (', ' if arg_str
                                   else '', arg_spec['keywords'])
        if arg_str.startswith(','):
            arg_str = arg_str[1:]
        return "%s(%s)" % (signature_dict['qualified_name'], arg_str.strip())

    def _build_variable_signature(self, signature_dict):
        return "%s = %s" % (signature_dict['qualified_name'],
                            signature_dict['member_value'])

    def _build_class_signature(self, signature_dict):
        return signature_dict['qualified_name']

    def _build_signature(self, signature_dict):
        if (signature_dict['member_type'] in
                [APISignature.SignatureType.FUNCTION,
                 APISignature.SignatureType.METHOD]):
            return self._build_callable_signature(signature_dict)
        elif signature_dict['member_type'] == APISignature.SignatureType.CLASS:
            return self._build_class_signature(signature_dict)
        else:
            return self._build_variable_signature(signature_dict)


class ModuleParser(object):

    def __init__(self, listeners, abort_on_load_failure=False):
        self.listeners = listeners
        self.abort_on_load_failure = abort_on_load_failure

    def _notify(self, signature_type, qualified_name, member, arg_spec=None):
        for listener in self.listeners:
            notify = getattr(listener, 'parse_' + signature_type)
            notify(APISignature(signature_type, qualified_name,
                                member, arg_spec or
                                inspect.ArgSpec(None, None, None, None)))

    def _collect_paths(self, paths, recurse=True):
        inits, mods = [], []

        if not paths:
            return inits, mods

        for py_path in paths:
            if is_py_file(py_path):
                if path.basename(py_path) == '__init__.py':
                    inits.append(py_path)
                else:
                    mods.append(py_path)
            elif is_py_dir(py_path) and recurse:
                c_inits, c_mods = self._collect_paths(
                    [path.join(py_path, c) for c in os.listdir(py_path)],
                    recurse=recurse)
                inits.extend(c_inits)
                mods.extend(c_mods)
        return inits, mods

    def _load_path(self, module_path):
        module_name = path.basename(path.splitext(module_path)[0])
        pkg_name = '.'.join(parent_package_names(module_path) or '')
        defined_name = ('%s.%s' % (pkg_name, module_name) if pkg_name
                        else module_name)
        if module_name == '__init__':
            defined_name = pkg_name

        search_paths = [parent_path(module_path)]
        f = None
        try:
            if defined_name in sys.modules:
                del sys.modules[defined_name]
            f, p, d = imp.find_module(module_name, search_paths)
            module = importlib.load_module(defined_name, f, p, d)
            if defined_name == '__init__':
                setattr(module, '__path__', search_paths)
            return module
        except Exception as e:
            sys.stderr.write("Failed to load module '%s' due to: %s" %
                             (module_path, e))
            if self.abort_on_load_failure:
                raise e
        finally:
            if f:
                f.close()

    def load_modules(self, init_paths, module_paths):
        init_mods, mods = [], []
        failed_to_load = []

        def _load(paths, store):
            for m_path in paths:
                module = self._load_path(m_path)
                if module:
                    store.append(module)
                else:
                    failed_to_load.append(m_path)

        _load(init_paths, init_mods)
        _load(module_paths, mods)
        return init_mods, mods, failed_to_load

    def _fully_qualified_name(self, parent, name):
        if inspect.isclass(parent):
            prefix = parent.__module__ + '.' + parent.__name__
        else:
            prefix = parent.__name__
        return prefix + '.' + name

    def parse_modules(self, modules):
        for module in modules:
            for member_name, member in inspect.getmembers(
                    module, _member_filter):

                if member_name.startswith('__') and member_name.endswith('__'):
                    continue

                fqn = self._fully_qualified_name(module, member_name)

                if inspect.isclass(member):
                    self._notify(APISignature.SignatureType.CLASS,
                                 fqn, member)
                    self.parse_modules([member])
                elif inspect.isfunction(member):
                    self._notify(APISignature.SignatureType.FUNCTION,
                                 fqn, member,
                                 arg_spec=inspect.getargspec(member))
                elif inspect.ismethod(member):
                    self._notify(APISignature.SignatureType.METHOD,
                                 fqn, member,
                                 arg_spec=inspect.getargspec(member))
                else:
                    event = (APISignature.SignatureType.MODULE_ATTR
                             if inspect.ismodule(module)
                             else APISignature.SignatureType.CLASS_ATTR)
                    self._notify(event, fqn, member)

    def parse_paths(self, py_paths, recurse=True):
        init_paths, mod_paths = self._collect_paths(
            py_paths, recurse=recurse)
        init_mods, pkg_mods, failed_mods = self.load_modules(
            init_paths, mod_paths)
        self.parse_modules(init_mods)
        self.parse_modules(pkg_mods)


class APIReport(object):

    def __init__(self, abort_on_load_failure=False):
        self._api = {}
        self._parser = ModuleParser(
            [self], abort_on_load_failure=abort_on_load_failure)

    def _add(self, event):

        if is_mock_import(event.member):
            return
        uuid = str(event.qualified_name)
        if uuid in self._api:
            # TODO(boden): configurable bail on duplicate flag
            sys.stderr.write("Duplicate API signature: %s" % uuid)
            return

        if not filter(blacklist_filter, [uuid]):
            return

        self._api[uuid] = event.to_dict()

    def parse_method(self, event):
        self._add(event)

    def parse_function(self, event):
        self._add(event)

    def parse_class(self, event):
        self._add(event)

    def parse_class_attribute(self, event):
        self._add(event)

    def parse_module_attribute(self, event):
        self._add(event)

    def parse_api_paths(self, api_paths, recurse=True):
        self._parser.parse_paths(api_paths, recurse=recurse)

    def parse_api_path(self, api_path, recurse=True):
        self.parse_api_paths([api_path], recurse=recurse)

    @property
    def api(self):
        return dict(self._api)

    def to_json(self):
        return jsonutils.dumps(self._api)

    @staticmethod
    def from_json(json_str):
        api = APIReport()
        api._api = jsonutils.loads(json_str)
        return api

    @staticmethod
    def from_json_file(file_path):
        with open(file_path, 'r') as json_file:
            data = json_file.read()
        return APIReport.from_json(data)

    @staticmethod
    def api_diff_files(new_api, old_api):
        new_api = APIReport.from_json_file(new_api)
        old_api = APIReport.from_json_file(old_api)
        return new_api.api_diff(old_api)

    def get_filtered_signatures(self):
        return filter(blacklist_filter, self.get_signatures())

    def get_signatures(self):
        return sorted([APISignature.get_signature(s)
                       for s in self._api.values()])

    def api_diff(self, other_api):
        our_keys = sorted(self.api.keys())
        other_keys = sorted(other_api.api.keys())

        new_keys = set(our_keys) - set(other_keys)
        removed_keys = set(other_keys) - set(our_keys)
        common_keys = set(our_keys) & set(other_keys)

        common_key_changes = [k for k in common_keys
                              if ordered(self.api[k]) !=
                              ordered(other_api.api[k])]

        for k in common_key_changes:
            if (not blacklist_filter(self.api[k]['member_value']) and not
                    blacklist_filter(other_api.api[k]['member_value'])):
                common_key_changes.remove(k)

        def _build_report(new_api):
            apis = APIReport()
            apis._api = new_api
            return apis

        return {
            'new': _build_report({k: self.api[k] for k in new_keys}),
            'removed': _build_report({k: other_api.api[k]
                                      for k in removed_keys}),
            'unchanged': _build_report({k: self.api[k]
                                        for k in
                                        set(common_keys) -
                                        set(common_key_changes)}),
            'new_changed': _build_report({k: self.api[k]
                                          for k in common_key_changes}),
            'old_changed': _build_report({k: other_api.api[k]
                                          for k in common_key_changes})
        }


class AbstractCommand(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_parser(self):
        pass

    @abc.abstractmethod
    def run(self, args):
        pass


def _add_blacklist_opt(parser):
    parser.add_argument(
        '--blacklist',
        help='One or more regular expressions used to filter out '
             'API paths from the report. File path segments, module '
             'names, class names, etc. are all subject to filtering. '
             'Multiple regexes can be specified using a comma in the '
             '--blacklist argument.')


class GenerateReportCommand(AbstractCommand):

    PY_LINE_FILTERS = [RemoveDocStrings(),
                       RemoveCommentLines(),
                       StripTrailingComments(),
                       MergeMultiLineImports(),
                       MergeMultiLineClass(),
                       MergeMultiLineDef(),
                       MergeMultiLineDecorator(),
                       CommentOutDecorators(),
                       PassEmptyDef(),
                       MockParentClass(),
                       AddMockDefinitions(),
                       MockImports()]

    def __init__(self):
        self._parser = argparse.ArgumentParser(
            prog='generate',
            description='Generate an interface report for python '
                        'source. The paths given can be a python '
                        'package or project directory, or a single '
                        'python source file. The program replaces '
                        'your imports with mocks, so no dependencies '
                        'are needed in the python env.')
        _add_blacklist_opt(self._parser)
        self._parser.add_argument(
            '--debug',
            help='Exit parsing on failure to load a module and '
                 'leave temp staging dir intact..',
            action='store_const',
            const=True)
        self._parser.add_argument('PATH', nargs='+', metavar='PATH')

    def get_parser(self):
        return self._parser

    def run(self, args):
        if args.blacklist:
            add_blacklist_from_csv_str(args.blacklist)

        files = PyFiles(args.PATH)
        with files.tmp_tree(delete_on_exit=(
                not args.debug)) as tmp_root:
            PyFiles.filter_all_py_files(
                tmp_root, GenerateReportCommand.PY_LINE_FILTERS)
            report = APIReport(abort_on_load_failure=args.debug)
            for child in os.listdir(tmp_root):
                child_path = path.join(tmp_root, child)
                report.parse_api_paths([child_path])

        print("%s" % report.to_json())


class PrintReportCommand(AbstractCommand):

    def __init__(self):
        self._parser = argparse.ArgumentParser(
            prog='print',
            description='Given a JSON API file, print the API signatures '
                        'to STDOUT.')
        _add_blacklist_opt(self._parser)
        self._parser.add_argument('REPORT_FILE',
                                  help='Path to JSON report file.')

    def get_parser(self):
        return self._parser

    def run(self, args):
        if args.blacklist:
            add_blacklist_from_csv_str(args.blacklist)
        report = APIReport.from_json_file(args.REPORT_FILE)
        for signature in report.get_filtered_signatures():
            print(signature)


class DiffReportCommand(AbstractCommand):

    def __init__(self):
        self._parser = argparse.ArgumentParser(
            prog='diff',
            description='Given a new and old JSON interface report '
                        'files, calculate the changes between new '
                        'and old and echo them to STDOUT.')
        _add_blacklist_opt(self._parser)
        self._parser.add_argument(
            '--unchanged',
            help='Used with --diff to specify that unchanged '
                 'public APIs should be reported in addition to '
                 'new and removed.',
            action='store_const',
            const=True)
        self._parser.add_argument('NEW_REPORT_FILE',
                                  help='Path to new report file.')
        self._parser.add_argument('OLD_REPORT_FILE',
                                  help='Path to old report file.')

    def get_parser(self):
        return self._parser

    def _print_row(self, heading, content_list):
        print(heading)
        print("-----------------------------------------------------")
        for content in content_list:
            print(str(content))
        print("-----------------------------------------------------\n")

    def run(self, args):
        if args.blacklist:
            add_blacklist_from_csv_str(args.blacklist)

        api_diff = APIReport.api_diff_files(
            args.NEW_REPORT_FILE, args.OLD_REPORT_FILE)

        self._print_row("New API Signatures",
                        api_diff['new'].get_filtered_signatures())
        self._print_row("Removed API Signatures",
                        api_diff['removed'].get_filtered_signatures())

        new_sigs = api_diff['new_changed'].get_filtered_signatures()
        old_sigs = api_diff['old_changed'].get_filtered_signatures()
        if len(new_sigs) != len(old_sigs):
            new_sigs = []
            old_sigs = []
            new_changed = api_diff['new_changed'].api
            old_changed = api_diff['old_changed'].api
            for n, new_spec in new_changed.items():
                display_old = blacklist_filter(old_changed[n]['member_value'])
                display_new = blacklist_filter(new_spec['member_value'])
                if display_old and display_new:
                    new_sigs.append(APISignature.get_signature(new_spec))
                    old_sigs.append(APISignature.get_signature(old_changed[n]))
                elif not display_old:
                    new_sigs.append(APISignature.get_signature(new_spec))
                    old_sigs.append(n)
                else:
                    new_sigs.append('UNKNOWN')
                    old_sigs.append(n)
        self._print_row("Changed API Signatures",
                        ["%s [is now] %s" %
                         (old_sigs[i], new_sigs[i])
                         for i in range(len(new_sigs))])

        if args.unchanged:
            self._print_row("Unchanged API Signatures",
                            api_diff['unchanged'].get_filtered_signatures())


class CLI(object):

    def __init__(self, commands):
        self._commands = {c.get_parser().prog: c for c in commands}
        self.parser = argparse.ArgumentParser(
            prog='pyir',
            description='Python API report tooling.',
            usage="pyir <%s> [args]" % "|".join(self._commands.keys()),
            add_help=True)
        self.parser.add_argument(
            'command',
            help='The command to run. Known commands: '
                 '%s . Try \'pyir <command> --help\' for more info '
                 'on a specific command. ' % ", ".join(self._commands.keys()))

        args = self.parser.parse_args(sys.argv[1:2])
        if args.command not in self._commands.keys():
            print("Unknown command: %s" % args.command)
            self.parser.print_help()
            exit(1)

        cmd = self._commands[args.command]
        cmd.get_parser().prog = self.parser.prog + ' ' + cmd.get_parser().prog
        cmd.run(cmd.get_parser().parse_args(sys.argv[2:]))


def main():
    CLI([DiffReportCommand(), GenerateReportCommand(), PrintReportCommand()])

if __name__ == '__main__':
    main()
    exit(0)
