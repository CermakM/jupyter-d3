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

"""d3.js binding to execute d3 scripts in Jupyter notebooks."""


from string import Template
from textwrap import dedent

from IPython.core.display import display, Javascript

from . import config
from require import require


require.config({
    'd3': config.defaults.d3,
    'd3-hierarchy': config.defaults.d3_hierarchy
})


class D3Template(Template):
    """Custom d3 string template."""

    delimiter = "$$"

    def __init__(self, script: str):
        """Wrap the script in `require` function and instantiate template."""

        libraries = ', '.join(
            [f"'{lib}'" for lib in require.loaded_libraries.keys()]
        )
        wrapped_script = """
            'use strict';
            
            try {{
                    
                console.log("Checking required libraries: ", {libs});
                
                [{libs}].forEach( lib => {{
                
                    let is_defined = require.defined(lib);
                    console.log(`Checking library: ${{lib}}`, is_defined ? '✓' : 'x');
                    
                    if (!is_defined) {{
                        // throw
                        throw new Error(`RequireError: Requirement could not be satisfied: '${{lib}}'.`);
                    }}
                    
                }});
            
                require([{libs}], function ({args}) {{
                
                    // execute the script
                    {script}
                        
                }});
                
            }} catch(err) {{
            
                // append stack trace to the cell output element
                let div = document.createElement('div');
                
                div = $('<div/>')
                    .addClass('js-error')
                    .html(err.stack.replace(/\sat/g, '<br>\tat') + '<hr>');
                
                $(element).append(div);
                
                // re-throw
                throw err;
                    
            }}
            
        """.format(libs=libraries,
                   args=libraries.replace("'", '').replace('-', '_'),
                   script=script)

        super().__init__(dedent(wrapped_script))


def d3(script: str, **kwargs):
    """Execute d3 script."""

    parsed_script = parse_script(script, **kwargs)

    return display(Javascript(parsed_script))


def parse_script(script: str, **kwargs) -> str:
    """Parse the JS script and returns string template."""
    d3_template = D3Template(script)

    return substitute(d3_template, **kwargs)


def substitute(template: "D3Template", safe_substitute=True, **kwargs) -> str:
    """Substitute Python template variables."""
    if safe_substitute:
        script = template.safe_substitute(**kwargs)
    else:
        script = template.substitute(**kwargs)

    return script
