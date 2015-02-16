from fabric.api import local

def _execute(cmd, capture=False):
    ret = local(cmd, capture=capture)
    return ret
