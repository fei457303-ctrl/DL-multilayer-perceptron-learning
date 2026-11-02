"""Download and validate the official Fashion-MNIST IDX files."""
from pathlib import Path
import gzip, hashlib, struct, urllib.request
import numpy as np
FILES = {
 'train-images-idx3-ubyte.gz':'8d4fb7e6c68d591d4c3dfef9ec88bf0d',
 'train-labels-idx1-ubyte.gz':'25c81989df183df01b3e8a0aad5dffbe',
 't10k-images-idx3-ubyte.gz':'bef4ecab320f06d8554ea6380940ec79',
 't10k-labels-idx1-ubyte.gz':'bb300cfdad3c16e7a12a480ee83cd310',
}
BASE='https://raw.githubusercontent.com/zalandoresearch/fashion-mnist/master/data/fashion/'
CLASSES=['T-shirt/top','Trouser','Pullover','Dress','Coat','Sandal','Shirt','Sneaker','Bag','Ankle boot']
def load_fashion(cache):
    cache=Path(cache);cache.mkdir(parents=True,exist_ok=True)
    arrays={}
    for name,checksum in FILES.items():
        path=cache/name
        if not path.exists():
            print('Downloading',name,flush=True)
            with urllib.request.urlopen(BASE+name,timeout=120) as r: content=r.read()
            if hashlib.md5(content).hexdigest()!=checksum: raise ValueError('Download checksum mismatch: '+name)
            path.write_bytes(content)
        content=path.read_bytes()
        if hashlib.md5(content).hexdigest()!=checksum: raise ValueError('Cached checksum mismatch: '+str(path))
        raw=gzip.decompress(content)
        magic,n=struct.unpack('>II',raw[:8])
        if magic==2051:
            rows,cols=struct.unpack('>II',raw[8:16]);assert (rows,cols)==(28,28)
            assert len(raw)==16+n*rows*cols
            arrays[name]=np.frombuffer(raw,dtype=np.uint8,offset=16).reshape(n,1,28,28).copy()
        elif magic==2049:
            assert len(raw)==8+n
            arrays[name]=np.frombuffer(raw,dtype=np.uint8,offset=8).copy()
        else: raise ValueError('Invalid IDX header')
    return (arrays['train-images-idx3-ubyte.gz'],arrays['train-labels-idx1-ubyte.gz'],
            arrays['t10k-images-idx3-ubyte.gz'],arrays['t10k-labels-idx1-ubyte.gz'])
