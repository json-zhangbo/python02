#!/usr/bin/python3
class Person:
    def __init__(self,firstname,lastname):
        self.firstname=firstname
        self.lastname=lastname

p1=Person("zhang","bo")
print(p1.firstname)
print(p1.lastname)