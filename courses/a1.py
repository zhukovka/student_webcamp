'''
Created on Jun 3, 2014

@author: lenka
'''
from .models import *


def main():
    h = Course.objects.createCourse('javascript')
    h.save()
if __name__ == '__main__':
    pass