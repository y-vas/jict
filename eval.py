from eval.base import eval

from jict import jict

jct = jict({"1":{"name":"bob","age":"20","work":"Assistant"}})
jct2 = jict({"2":{"name":"James","age":"36","work":"Dev"}})

jct['1'].replace({"name":"bob","age":"25","work":"Dev"})
jct2['2'].replace({"name": "James", "age": "40", "work": "Assistant"})

print(jct)
print(jct2)

jct = jict()
# base( jct )
