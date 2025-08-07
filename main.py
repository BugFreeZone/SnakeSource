from os import system, chdir, listdir
from sys import argv,exit
from json import load

class PM:
    def __init__(self):
        try:
            with open('package.json') as f:
                self.db=load(f)
        except FileNotFoundError:
            print('[Error]: File packages.json not found')
            exit()
        except IsADirectoryError:
            print('[Error]: File packages.json is a directory')
            exit()
        except Exception as e:
            print(f'[Error]: Unknown error: {e}')
        try:
            with open('logo.txt') as f:
                print(f.read())
        except FileNotFoundError:
            print('[Error]: File logo.txt not found')
            exit()
        except IsADirectoryError:
            print('[Error]: File logo.txt is a directory')
            exit()
        except Exception as e:
            print(f'[Error]: Unknown error: {e}')
    def install(self, pkgname:str):
        if pkgname in self.db:
            print(f'[{pkgname}]: Downloading . . .')
            if system('git clone '+self.db[pkgname]['url']+' > /dev/null')!=0:
                print(f'[{pkgname}]: Dowloading failed')
                return
            print(f'[{pkgname}]: Resolvind dependencies . . .')
            for dep in self.db[pkgname]['deps']:
                if not self.is_installed(dep):
                    if dep in self.db:
                        print(f'[{pkgname}]: Installing dependencies({dep})')
                        self.install(dep)
                    else:
                        print(f'[{pkgname}]: {dep} is needed but not in packages.json')
                        exit()
            print(f'[{pkgname}]: Making . . .')
            try:
                chdir(pkgname)
            except FileNotFoundError:
                print(f'[{pkgname}]: Directory not found')
                return
            if system(self.db[pkgname]['build_command'])!=0:
                print(f'[{pkgname}]: Build failed')
                return
            print(f'[{pkgname}]: Done! ')
        else:
            print(f'[{pkgname}]: Package not found')
    def remove(self, pkgname:str):
        try:
            system(f'sudo rm -rf  $(which {pkgname}) > /dev/null')
        except:
            print(f'[{pkgname}]: Error')
    def search(self, pkgname:str):
        found=False
        for i in self.db:
            if pkgname in i:
                print(f'[{pkgname}]: Found in {i}')
                found=True
        if not found:
            print(f'[{pkgname}]: Not found')
    def is_installed(self, pkgname:str):
        return True if pkgname in listdir('/bin/') or pkgname in listdir('/sbin/') or pkgname in listdir('/usr/bin/') or pkgname in listdir('/usr/sbin/') else False
    def list(self):
        for i in self.db:
            if self.is_installed(i):
                print(f'[{i}]: Found')

if __name__=='__main__':
    pm=PM()
    pm.list()
    if len(argv) > 1:
        if argv[1]=='install':
            try:
                pm.install(argv[2])
            except KeyboardInterrupt:
                pass
        elif argv[1]=='remove':
            try:
                pm.remove(argv[2])
            except KeyboardInterrupt:
                pass
        elif argv[1]=='search':
            try:
                pm.search(argv[2])
            except KeyboardInterrupt:
                pass
        elif argv[1]=='list':
            try:
                pm.list()
            except KeyboardInterrupt:
                pass
        else:
            print('[Error]: Unknown arguments')
    else:
        print('[Error]: Unknown arguments')
