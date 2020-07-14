from jict import jict, jictmt
#
#
# def get_example_tree():
#
#     retval = {"name":"parent","children":[]}
#     for i in range(3):
#         retval['children'].append({"name":"child " + str(i)})
#         retval['children'][i]['children']=[]
#         for j in range(5):
#             retval['children'][i]['children'].append({"name":"grandchild " +
#                                                       str(i) + "." + str(j)})
#
#     return [retval]

#
#
# tr = get_example_tree()
# # print(jict(tr))
#
jct = jict('get://mymemory.yaml')

jct['asdfasd'] = '1'
jct['151'] = 'dsfasd'
jct['153'] = 'aaaaaa'
jct['asdfasd'] = 'afsdf'

# def mkdic():
#
#
# retval = {"name":"main","children":[]}
# for i, x in enumerate( jct.keys() ):
#     retval['children'].append({"name": x })
#
# print(retval)

jictmt( jct ).main()

#
# import urwid
#
# class SelectableText(urwid.Text):
#     def selectable( self ):
#         return True
#
#     def keypress( self, size, key ):
#         return key
#
# content = urwid.SimpleListWalker([
#     urwid.AttrMap(SelectableText('foo'), '',  'reveal focus' ),
#     urwid.AttrMap(SelectableText('bar'), '',  'reveal focus' ),
#     urwid.AttrMap(SelectableText('baz'), '',  'reveal focus' ),
# ])
#
# listbox = urwid.ListBox(content)
# wrapped = listbox
#
# palette = [
#     ('reveal focus', 'black', 'dark cyan', 'standout')
# ]
#
# loop = urwid.MainLoop(wrapped, palette=palette)
# loop.run()
