import urwid
import os
from time import time,sleep

class SelectableText( urwid.Text ):
    def selectable( self ):
        return True

    def keypress( self, size, key ):
        return key

class jictmt:
    palette = [
        ('body', 'black', 'white'),
        ('focus', 'light gray', 'dark blue', 'standout' ),
        ('head', 'yellow', 'white', 'standout' ),
        ('foot', 'light gray', 'black' ),
        ('key', 'light cyan', 'black','underline' ),
        ('title', 'white', 'black', 'bold' ),
        ('flag', 'dark gray', 'light gray' ),
        ('error', 'dark red', 'light gray' ),
        ('reveal focus', 'black', 'dark cyan', 'standout')
    ]

    footer_text = [
        ('title', "Example Data Browser"), "    ",
        ('key', "UP"), ",", ('key', "DOWN"), ",",
        ('key', "PAGE UP"), ",", ('key', "PAGE DOWN"),
        "  ",
        ('key', "+"), ",",
        ('key', "-"), "  ",
        ('key', "LEFT"), "  ",
        ('key', "HOME"), "  ",
        ('key', "END"), "  ",
        ('key', "Q"),
        ]

    def __init__(self, data ):

        self.data = data
        self.datak = list( data.keys() )

        self.list = urwid.SimpleListWalker([
            urwid.AttrWrap( SelectableText(x) , '',  'reveal focus' ) for x in data.keys()
        ])

        self.listbox = urwid.ListBox( self.list )
        self.listbox.offset_rows = 1

        self.columns = urwid.Columns([
            self.listbox,
            urwid.Filler( urwid.Text( str(time()) ), 'top')
        ])

        self.header = urwid.Text( "" )
        self.footer = urwid.AttrWrap( urwid.Text( self.footer_text ) , 'foot' )

        self.view = urwid.Frame(
            urwid.AttrWrap( self.columns, 'body' ),
            header = urwid.AttrWrap( self.header , 'head' ),
            footer= self.footer
        )

    def main(self):
        self.loop = urwid.MainLoop(
            self.view,
            self.palette,
        )

        def alarma(x,y):
            f = self.list.get_focus()

            data = self.data[ self.datak[ int(f[1]) ] ]

            if isinstance(data,list):
                ls = ''

                for x in data:
                    ls += str( x ) + '\n'

                data = ls

            self.columns.contents[1] = (urwid.Filler(urwid.Text(
                str( data )
            ),'top'), self.columns.options())

            self.loop.set_alarm_in( 0.5 , alarma )

        self.loop.set_alarm_in( 0.5,alarma)

        self.loop.run()
