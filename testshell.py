from frontloader import Repository
from frontloader import Pipeline
from frontloader.hduparsers import bok, decam
from frontloader.transforms.essential import Stitch, Mock

#repo= Repository('testdata/bok', 'testdata/bok.json')
repo= Repository('testdata/decam', 'testdata/decam.json')

pipe = Pipeline([
        Mock(),
        Stitch()])

PK = repo.get(repo.where("OBJECT") == "object")['PK']
expo = repo.open(PK)
decam.parse_hdus(expo)

#img = pipe.reduce(expo)

print expo

print img['CCD1'].invvar
print img['CCD1'].buffer
imshow(img['CCD1'].buffer)

