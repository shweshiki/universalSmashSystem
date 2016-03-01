#!/usr/bin/env python
from __future__ import print_function
import pygame
import engine.stage
import stages.true_arena as stage
import settingsManager
import imp
import os
from pygame.locals import *

from engine import *
from builder import *
from fighters import *
from menu import *
from stages import *

def main(debug = False):
    menu = importFromURI("__file__",'menu/menu.py')
    menu.Menu()
    
def importFromURI(filePath, uri, absl=False, suffix=""):
    if not absl:
        uri = os.path.normpath(os.path.join(os.path.dirname(filePath).replace('main.exe',''), uri))
    path, fname = os.path.split(uri)
    mname, ext = os.path.splitext(fname)
    
    no_ext = os.path.join(path, mname)
         
    if os.path.exists(no_ext + '.py'):
        try:
            return imp.load_source((mname + suffix), no_ext + '.py')
        except Exception as e:
            print(mname, e)
        
    
if __name__  == '__main__': main(True)

