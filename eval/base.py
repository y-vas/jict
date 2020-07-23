
def eval_base(jct):
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


    # test iad
    # default dict 


    print( jct )
