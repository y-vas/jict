#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sample program demonstrating how to implement widgets for a master-detail UI
for a list of records using the urwid library (http://urwid.org)
"""

from __future__ import print_function, absolute_import, division
from functools import partial
import urwid


PALETTE = [
    ('bold', 'bold', ''),
    ('reveal focus', 'black', 'dark cyan', 'standout'),
]


def show_or_exit(key):
    if key in ('q', 'Q', 'esc'):
        raise urwid.ExitMainLoop()


HEADERS = ["Field 1", "Field 2", "Field 3", "Field 4"]
ENTRIES = [
    ["a1", "a2", "a3", "a4"],
    ["b1", "b2", "b3", "b4"],
    ["c1", "c2", "c3", "c4"],
    ["d1", "d2", "d3", "d4"],
    ["e1", "e2", "e3", "e4"],
    ["e1", "e2", "e3", "e4"],
    ["f1", "f2", "f3", "f4"],
    ["g1", "g2", "g3", "g4"],
    ["h1", "h2", "h3", "h4"],
]


class SelectableRow(urwid.WidgetWrap):
    def __init__(self, contents, on_select=None):
        self.on_select = on_select
        self.contents = contents
        self._columns = urwid.Columns([urwid.Text(c) for c in contents])
        self._focusable_columns = urwid.AttrMap(self._columns, '', 'reveal focus')
        super(SelectableRow, self).__init__(self._focusable_columns)

    def selectable(self):
        return True

    def update_contents(self, contents):
        # update the list record inplace...
        self.contents[:] = contents

        # ... and update the displayed items
        for t, (w, _) in zip(contents, self._columns.contents):
            w.set_text(t)

    def keypress(self, size, key):
        if self.on_select and key in ('enter',):
            self.on_select(self)
        return key

    def __repr__(self):
        return '%s(contents=%r)' % (self.__class__.__name__, self.contents)


class CancelableEdit(urwid.Edit):
    def __init__(self, *args, **kwargs):
        self.on_cancel = kwargs.pop('on_cancel', None)
        super(CancelableEdit, self).__init__(*args, **kwargs)

    def keypress(self, size, key):
        if key == 'esc':
            self.on_cancel(self)
        else:
            return super(CancelableEdit, self).keypress(size, key)


def build_dialog(title, contents, background, on_save=None, on_cancel=None):
    buttons = urwid.Columns([
        urwid.Button('Save', on_press=on_save),
        urwid.Button('Cancel', on_press=on_cancel),
    ])
    pile = urwid.Pile(
        [urwid.Text(title), urwid.Divider('-')]
        + contents
        + [urwid.Divider(' '), buttons]
    )
    return urwid.Overlay(
        urwid.Filler(urwid.LineBox(pile)),
        urwid.Filler(background),
        'center',
        ('relative', 80),
        'middle',
        ('relative', 80),
    )


class App(object):
    def __init__(self, entries):
        self.entries = entries
        self.header = urwid.Text('Welcome to the Master Detail Urwid Sample!')
        self.footer = urwid.Text('Status: ready')

        contents = [
            SelectableRow(row, on_select=self.show_detail_view)
            for row in entries
        ]
        listbox = urwid.ListBox(urwid.SimpleFocusListWalker(contents))

        # TODO: cap to screen size
        size = len(entries)

        self.master_pile = urwid.Pile([
            self.header,
            urwid.Divider(u'─'),
            urwid.BoxAdapter(listbox, size),
            urwid.Divider(u'─'),
            self.footer,
        ])
        
        self.widget = urwid.Filler(self.master_pile, 'top')
        self.loop = urwid.MainLoop(self.widget, PALETTE, unhandled_input=show_or_exit)

    def show_detail_view(self, row):
        self._edits = [
            CancelableEdit('%s: ' % key, value, on_cancel=self.close_dialog)
            for key, value in zip(HEADERS, row.contents)
        ]
        self.loop.widget = build_dialog(
            title='Editing',
            contents=self._edits,
            background=self.master_pile,
            on_save=partial(self.save_and_close_dialog, row),
            on_cancel=self.close_dialog,
        )
        self.show_status('Detail: %r' % row)

    def save_and_close_dialog(self, row, btn):
        new_content = [e.edit_text for e in self._edits]

        row.update_contents(new_content)

        self.show_status('Updated')
        self.loop.widget = self.widget

    def close_dialog(self, btn):
        self.loop.widget = self.widget

    def show_status(self, mesg):
        self.footer.set_text(str(mesg))

    def start(self):
        self.loop.run()


if __name__ == '__main__':
    app = App(ENTRIES)
    app.start()
