# jupyter-d3
# Copyright 2019 Marek Cermak <macermak@redhat.com>
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""d3.js Jupyter notebook magic to execute d3 scripts in Jupyter notebooks."""

from IPython.core.magic import cell_magic
from IPython.core.magic import line_magic
from IPython.core.magic import line_cell_magic
from IPython.core.magic import magics_class
from IPython.core.magic import Magics


@magics_class
class JupyterD3(Magics):
    """d3.js Jupyter notebook magic.

    This magic class provides convenient execution of JavaScript
    lines or cells containing d3.js source. It allows to pass
    python variables directly to the cell and does not require
    user to set up d3 manually.

    Example:

    Read data in python

    ```python
    import pandas as pd

    raw_data = pd.read_csv("raw_data.csv")
    ```

    And now for the d3 JavaScript part

    ```javascript
    %%d3

    const parsed_data = d3.parseCSV($$raw_data);  // use double $ sign to denote python variable
    const x = 300,
          y = 300;
    var svg = d3.select(element.get(0)).append('svg')

    svg
        .append('g')
        .transform(`translate (${x}, ${y})`);  // single $ sign as usual

    svg.select('g')
        .data(parsed_data) //
        ...
    ```
    """

    @line_magic
    def lmagic(self):
        """Execute line as d3 command and displays output."""

    @cell_magic
    def cmagic(self):
        """Execute current cell as d3 script and displays output."""

    @line_cell_magic
    def lcmagic(self):
        """Syntactic sugar which can be used as both cell and line magic."""
