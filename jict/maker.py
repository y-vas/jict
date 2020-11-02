import os

'''


'''

class Mold:
    bootstrap = False
    bfc = 'form-control'
    framework = 'django'

    def __init__(self , *args, **kwargs ):
        self.keys = kwargs


    def make(self):
        html = {}

        for x in self.keys:
            mode = self.keys[x]

            if x == 'id':
                continue

            name = mode['name'] if 'name' in mode else x

            value = f"value="
            if self.framework == 'django':
                value += "'{{obj." + name + "}}'"

            cls = self.bfc if self.bootstrap else ''
            ht = mode['ht'] if 'ht' in mode else 'text'
            name = name[0].upper() + name[1:]
            html[x] = f"<input class='{cls}' type='{ht}' name='{x}' {value} placeholder='{name}' >"



        print(html)
