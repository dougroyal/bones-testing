from paver.easy import task, needs, sh, path
import re
import os

VERSION = '0.1.0'


@task
def bump_version():
    version_line = "VERSION = '%s'" % _build_new_version(VERSION)
    version_pattern = "VERSION = '\d\.\d\.\d'"

    pavement_file = os.path.realpath(__file__)

    new_pavement_lines = []
    with open(path(pavement_file), 'r') as f:
        for line in f.readlines():
            new_line = re.sub(version_pattern, version_line, line)
            new_pavement_lines.append(new_line)

    import pprint; pprint.pprint(new_pavement_lines)

    with open(path(pavement_file), 'w') as f:
        f.writelines(new_pavement_lines)

@task
def clean():
    """ remove __pycache__ directories """
    sh('find . -type d -name __pycache__ -exec rm -rf {} \;')


@task
def freeze():
    """ pip freeze > requirements.txt, excluding development installs"""
    dependencies = sh('pip freeze', capture=True).split(os.linesep)

    with open('requirements.txt', 'w') as file:
        for dep in dependencies:
            if not dep.startswith('bones-testing'):
                file.write(dep+'\n')

def _build_new_version(old_version):
    new_version = old_version.split('.')
    new_version[1] = str(int(new_version[1])+1)
    return '.'.join(new_version)
