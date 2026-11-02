"""Execute the notebook with this Python interpreter, using a temporary kernel spec."""
from pathlib import Path
import json, os, sys, tempfile
import nbformat
from nbclient import NotebookClient
ROOT=Path(__file__).resolve().parents[1]
path=next((ROOT/'notebooks').glob('*.ipynb'))
notebook=nbformat.read(path,as_version=4)
with tempfile.TemporaryDirectory(prefix='d2l-kernel-') as temp:
    spec=Path(temp)/'kernels'/'project-runtime';spec.mkdir(parents=True)
    (spec/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],
        'display_name':'Project runtime','language':'python'}),encoding='utf-8')
    previous=os.environ.get('JUPYTER_PATH')
    os.environ['JUPYTER_PATH']=temp+(os.pathsep+previous if previous else '')
    try:
        NotebookClient(notebook,timeout=1800,kernel_name='project-runtime',resources={'metadata':{'path':str(ROOT)}}).execute()
    finally:
        if previous is None: os.environ.pop('JUPYTER_PATH',None)
        else: os.environ['JUPYTER_PATH']=previous
nbformat.validate(notebook)
nbformat.write(notebook,path)
print('Executed:',path.name)
