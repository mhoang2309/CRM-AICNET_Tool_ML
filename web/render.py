from flask import render_template as rt
from typing import Union, Optional
import html

def render_template(link:Optional[list]=None, script:Optional[list]=None, title:str="", body:str=""):
    _head = rt("base/_head.html", link=link, title=title)
    _script = rt("base/_script.html", script=link)
    _template = rt("base/_index.html", head=_head, body=body, script=_script)
    return html.unescape(_template)