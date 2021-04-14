#!/usr/bin/python3
# Exceptions
# CodeWriter21

class APIConfigNotFoundException(Exception):
	pass

class APIConfigDamagedException(Exception):
	pass

class NoBotConfigFoundException(Exception):
	pass

class NoBotEnabledConfigFoundException(Exception):
	pass

class ButtonsNotSetException(Exception):
	pass