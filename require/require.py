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

from string import Template
from textwrap import dedent
from traitlets import Dict, HasTraits, observe, Unicode

from IPython.core.display import display, Javascript


_REQUIREJS_TEMPLATE = Template(dedent("""
    require.config({
        paths: {
            $libs
        }
    });
"""))


class RequireJS(HasTraits):

    _LIBS = Dict(Unicode(allow_none=False), default_value=dict(), help="""
        Linked JavaScript libraries.
    """)

    @observe('_LIBS')
    def update(self, *args):
        """Update requireJS config in Jupyter Notebook."""
        # required libraries
        libs = (
            f"'{key}': '{path}'" for key, path in self._LIBS.items()
        )
        require_js: str = _REQUIREJS_TEMPLATE.safe_substitute(
            libs=', '.join(libs))

        return display(Javascript(dedent(require_js)))

    def __call__(self, library: str, path: str, *args, **kwargs):
        """Links JavaScript library to Jupyter Notebook.

        The library is linked using requireJS such as:

        ```javascript
        require.config({ paths: {<key>: <path>} });
        ```

        Please note that <path> does __NOT__ contain `.js` suffix.

        :param library: str, key to the library
        :param path: str, path (url) to the library without .js suffix
        """
        self._LIBS['library'] = path

    def config(self, libs: dict):
        """Links JavaScript libraries to Jupyter Notebook.

        The libraries are linked using requireJS such as:

        ```javascript
        require.config({ paths: {<key>: <path>} });
        ```

        Please note that <path> does __NOT__ contain `.js` suffix.
        """
        self._LIBS = libs

    @property
    def loaded_libraries(self) -> dict:
        """Get loaded libraries."""
        return dict(self._LIBS)
