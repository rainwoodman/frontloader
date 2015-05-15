from frontloader import Repository
from frontloader import Pipeline
from frontloader.transforms.essential import Stitch, Mock

repo= Repository('testdata/bok', 'testdata/bok.json')
pipe = Pipeline([
        Mock(),
        Stitch()])

PK = repo.get(repo.where("OBJECT") == "object")['PK']
expo = repo.open(PK)
img = pipe.reduce(expo)

print img['CCD1'].invvar
print img['CCD1'].buffer
imshow(img['CCD1'].buffer)

