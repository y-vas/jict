
def eval_base( jct ):
    jct['base'] = 1
    if jct['base'] != 1:
        raise Exception(' base is not == 1 :', jct['base'])

    jct['base2']['sub'] = 1
    if jct['base2']['sub'] != 1:
        raise Exception(' base2.sub is not == 1 :', jct['base2']['sub'])

    jct.init('base', 5 )
    if jct['base'] != 1:
        raise Exception(' init not set properly :', jct['base'])

    jct.init('base3', 5 )
    if jct['base3'] != 5:
        raise Exception(' init not set properly :', jct['base3'])

    # ---- test iad
    # default dict
    jct['RELES'] = [
        {'id':33,'status':False },
        {'id':37,'status':False }
    ]

    jct['RELES'] += [
        { 'id':33,'status': False },
        { 'id':37,'status': False }
    ]

    if len(jct['RELES']) != 4:
        raise Exception('add not done correctly :', jct['RELES'])


    jct.init('to_follow',[])

    now = len(jct['to_follow'])
    jct['to_follow'] += ['test']
    add = len(jct['to_follow'])

    if (add - 1) != now:
        raise Exception('add not done correctly :', jct['to_follow'])

    # jct = jict({"1":{"name":"bob","age":"20","work":"Assistant"}})
    # jct2 = jict({"2":{"name":"James","age":"36","work":"Dev"}})
    # jct.replace({"name":"bob","age":"25","work":"Dev"})
    # jct2.replace({"name": "James", "age": "40", "work": "Assistant"})
