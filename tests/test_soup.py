from os.path import join, dirname
from jict import Soup

def load_file( name ):
    return open(join(dirname(__file__),name)).read()

def test_refs_detected():
    soup  = Soup(load_file('cv.yaml'))
    refs = soup.tags

    assert len(refs) == 7

def test_soup():
    soup  = Soup(load_file('no-changes.html'))
    final = soup.to_string()

    assert final == load_file('no-changes.html')
    assert 7 == len( soup.tags )

    ref = soup.tags[6]
    assert ref.is_ref()
    assert ref.raw == '<ref/>'

    soup = Soup(load_file('counter.html'))
    tags = soup.find_by( name = 'counter' )

    for tag in tags:
        tag.set_replace(15)

    assert tags[0].render() == '15'
    assert tags[1].render() == '3'
    assert load_file('counter-end.html') == soup.to_string()


    soup = Soup(load_file('starting-tag.yaml'))
    assert len(soup.tags) == 0

    # sub changes
    soup = Soup(load_file('sub-changes.html'))
    tags = soup.find_by(name='ref')
    assert len(tags) == 1

    for tag in tags:
        tag.set_replace('#fasd')
    assert soup.to_string() == load_file('sub-changes-expect.html')



    # templates
    soup = Soup(load_file('template.html'))
    tags = soup.find_by(name='ref')
    assert len(tags) == 1
    assert tags[0].attrs.get('link',None) == 'clean'
