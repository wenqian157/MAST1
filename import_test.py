import sys
import os 

#region importing for vs code
path = os.path.dirname(os.path.dirname(__file__))
if path not in sys.path:
    sys.path.append(path)

import mola
#endregion


#region importing for gh python

# import os

# ghComp = ghenv.Component
# ghDoc = ghComp.OnPingDocument()
# gh_file_location = ghDoc.FilePath
# parent = os.path.dirname(os.path.realpath(gh_file_location))

# file_name = "filename.py"
# file_path = os.path.join(parent, file_name)
# print(file_path)

# execfile(file_path)
#endregion
