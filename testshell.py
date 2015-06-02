from frontloader import Repository
from frontloader import Pipeline
from frontloader.hduparsers import bok, decam
from frontloader.transforms.essential import Stitch, Initialize, ElectronicBias

#Xtalk

#repo= Repository('testdata/bok', 'testdata/bok.json')
repo= Repository('testdata/decam', 'testdata/decam.json')

pipe = Pipeline([
        Initialize(),
        ElectronicBias(),
        Stitch()])

PK = repo.get(repo.where("FLAVOR") == "object")['PK']
expo = repo.open(PK)
decam.parse_hdus(expo)

for ccdname in expo:
    r = pipe.reduce(expo[ccdname])
    print r.buffer

#print expo
#print expo['CCD00'].buffer

#print img['CCD1'].invvar
#print img['CCD1'].buffer
#imshow(img['CCD1'].buffer)

