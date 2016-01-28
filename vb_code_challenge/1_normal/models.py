from django.conf import settings
from django.db import models

## a very normal company address model.

## advantages:
## - less disk space used
## - can make some writes eaiser/faster
## - would make mr spock happy

## disadvantages:
## - harder for humans to read
## - can make reads slower due to many joins

class State(models.Model):
    name = models.CharField(max_length=63, help_text='State Name')

class City(models.Model):
    name = models.CharField(max_length=63, help_text='City Name')
    state = models.ForeignKey(State)

class Address(models.Model):
    street1 = models.CharField(max_length=63, help_text='Street Line 1')
    street2 = models.CharField(max_length=63, help_text='Street Line 2')
    city = models.ForeignKey(City)
    zipcode = models.CharField(max_length=10, help_text='Zip code')

class Company(models.Model):
    name = models.TextField(help_text='City Name')

class CompanyAddress(models.Model):
    company = models.ForeignKey(Company)
    address = models.ForeignKey(Address)
    
## legacy feilds are kept until migration from denormal model is complete...
##    company_name
##    street1
##    street2
##    city
##    state
##    zipcode