import settings.initial_settings as init
from mongoengine import *
import datetime as dt

log = init.LogDefaultConfig("mongo_engine.log").logger
