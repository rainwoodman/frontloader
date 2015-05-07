from frontloader import Instrument
from frontloader import Pipeline
from frontloader import Operation
from frontloader import Stitch, Copy

instr = Instrument('testdata/bok', 'testdata/bok.json')
pipe = Pipeline(instr, [
        Copy(),
        Stitch()])

r = pipe.reduce(instr.metadata.keys()[0])
