from frontloader import Repository
from frontloader import Pipeline
from frontloader.transforms.essential import Stitch, Mock

repo= Repository('testdata/bok', 'testdata/bok.json')
pipe = Pipeline([
        Mock(),
        Stitch()])

PK = repo.search(repo.where("OBJECT") == "object")[0]['PK']
expo = repo.open(PK)
img = pipe.reduce(expo)

print img.ccds['CCD1'].invvar
print img.ccds['CCD1'].buffer
imshow(img.ccds['CCD1'].buffer)

