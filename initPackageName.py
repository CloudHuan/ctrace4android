import os
import re

import sys

import Config
from tools.Helper import UsefulHelper

with open(os.path.join(sys.path[0],'Config.py'),'r+',encoding = 'utf-8') as f:
    result = f.read()
    result02 = re.sub("packageName = '.*' ","packageName='"+UsefulHelper().getCurrentPackageName()+"'",result);
    print(result02)

with open(os.path.join(sys.path[0],'Config.py'),'w+',encoding = 'utf-8') as f:
    f.write(result02)
