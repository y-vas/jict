from os.path import join,dirname
from jict import yaml_to_note

def test_yaml():
    val = yaml_to_note(
        open(
            join(dirname(__file__),'notes.yaml')
        ,'r').read()
    )

    assert isinstance(val,list)
    assert len(val) == 2
