from frontloader import Instrument
from frontloader import Pipeline
from frontloader import Operation
from frontloader import Stitch, Mock

instr = Instrument('testdata/bok', 'testdata/bok.json')
pipe = Pipeline(instr, [
        Mock(),
        Stitch()])

r = pipe.reduce(instr.metadata.keys()[0])
