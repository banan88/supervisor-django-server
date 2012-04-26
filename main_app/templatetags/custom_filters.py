# -*- coding: utf8


from django import template

register = template.Library()

STATES = {
        '3': 'Wykonane',
        '2': 'Aktywne',
        '1': 'Oczekujące',
        '0': 'Anulowane',
        }

def state_string(value):
    return STATES[value]

register.filter('state_string', state_string)