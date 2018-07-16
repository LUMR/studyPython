#!/usr/bin/env python3
from lumr.orm import *


class User(Model):
    id = StringField('id')
    name = StringField('name')
    age = IntegerField('age')


if __name__ == '__main__':
    a = User(id='abc', name='wum', age=19)
    a.save()
