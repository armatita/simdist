# simdist
Small desktop App (made in python, numpy, scipy , pyqt4 and pyqtgraph) made to "correct" a statistical variable distribution into a target one. It was made as a support software for the statistical modeling in a mine exploration. We had drilled well logs and direct samples. The direct sampling methods used in the case study had more uncertain results and they were far less reliable than drilled cores. As such to be able to use them in spatial characterization this small desktop App was used. Nevertheless please consider that doing this without having reason to do it can be quite damaging to your study.

![alt tag](/ART/simdist.png?raw=true)

<h2>Information for developers</h2>
simdist.py is both the code for gui file and the main script for this software. There's also cerena_file_utils.py, a small module I've created for GEOMS2 to open several different kinds of file formats.

<h2>Run from source</h2>
To run this App you'll need Python 2.7 version and the following libs:
- numpy, scipy, pyqt4, pyqtgraph

<h2>Compile with py2exe</h2>
If you need to "compile" this software the following instruction in a setup.py file is quite enough when using py2exe:
```Python
from distutils.core import setup
import py2exe

setup(windows=[{
            "script": "simdist.pyw"
        }])
```

<h2>Developer and contact</h2>

This software was developed within research center CERENA (IST - University of Lisbon).
![alt tag](/ART/cerena.png?raw=true)

You can contact us at: cerena.cmrp@gmail.com
