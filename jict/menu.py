import urwid
import os
from time import time,sleep

class ExampleTreeWidget( urwid.TreeWidget ):
    def get_display_text(self):
        return self.get_node().get_value()['name']

class ExampleNode(urwid.TreeNode):
    def load_widget(self):
        return ExampleTreeWidget(self)

class ExampleParentNode( urwid.ParentNode ):
    """ Data storage object for interior/parent nodes """
    def load_widget(self):
        return ExampleTreeWidget(self)

    def load_child_keys(self):
        data = self.get_value()
        return range(len(data['children']))

    def load_child_node(self, key):
        """Return either an ExampleNode or ExampleParentNode"""
        childdata = self.get_value()['children'][key]
        childdepth = self.get_depth() + 1
        if 'children' in childdata:
            childclass = ExampleParentNode
        else:
            childclass = ExampleNode

        return childclass(childdata, parent=self, key=key, depth=childdepth)


class ExampleTreeBrowser:
    palette = [
        ('body', 'black', 'white'),
        ('focus', 'light gray', 'dark blue', 'standout'),
        ('head', 'yellow', 'black', 'standout'),
        ('foot', 'light gray', 'black'),
        ('key', 'light cyan', 'black','underline'),
        ('title', 'white', 'black', 'bold'),
        ('flag', 'dark gray', 'light gray'),
        ('error', 'dark red', 'light gray'),
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

    def __init__(self, data = None ):
        self.topnode = ExampleParentNode( data )

        self.listbox = urwid.TreeListBox( urwid.TreeWalker(self.topnode) )
        self.listbox.offset_rows = 1

        self.columns = urwid.Columns([
            self.listbox, urwid.Filler( urwid.Text( str(time()) ), 'top')
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
            self.columns.contents[1] = (urwid.Filler(urwid.Text( str(time()) )), self.columns.options())
            self.loop.set_alarm_in(1, alarma )

        self.loop.set_alarm_in(1,alarma)

        self.loop.run()

def get_example_tree():

    retval = {"name":"parent","children":[]}
    for i in range(3):
        retval['children'].append({"name":"child " + str(i)})
        retval['children'][i]['children']=[]
        for j in range(5):
            retval['children'][i]['children'].append({"name":"grandchild " +
                                                      str(i) + "." + str(j)})

    return retval


def main():
    sample = get_example_tree()
    ExampleTreeBrowser(sample).main()


if __name__=="__main__":
    main()
