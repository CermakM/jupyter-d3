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

"""Jupyter magic for managing linked JavaScript Libraries."""


__name__ = "require"
__version__ = "0.1.0"


from IPython.core.magic import line_magic
from IPython.core.magic import magics_class
from IPython.core.magic import Magics
from IPython.core.magic import needs_local_scope

from .require import RequireJS

require = RequireJS()
require.__doc__ = RequireJS.config.__doc__


@magics_class
class RequireJSMagic(Magics):
    """Ipython magic for RequireJS class.

    Links JavaScript libraries to Jupyter Notebook.
    """

    @needs_local_scope
    @line_magic
    def require(self, line: str, local_ns=None):
        """Link required JS library.

        :param line: string in form '<key> <path>'
        :param local_ns: current cell namespace [optional]
        """
        user_ns = self.shell.user_ns
        user_ns.update(local_ns or dict())

        lib, path = line \
            .strip() \
            .split(sep=' ')

        return require(lib, path)


def load_ipython_extension(ipython):
    """Load the IPython extension."""
    # magic: %require
    ipython.register_magics(RequireJSMagic)