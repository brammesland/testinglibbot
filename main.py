from Student import *
from AutoBooker import *
from AutoLogger import *
from Booking import *
import datetime as dt

Konstantin = Student("Konstantin Asam", "576634ka@eur.nl", "password", "https://eur-nl.libcal.com/seat/123114")

#auto_booker = AutoBooker(Konstantin)
#auto_booker.book()

auto_logger = AutoLogger(Konstantin)
auto_logger.get_code()





