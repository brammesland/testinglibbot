# The student class creates an object that contains the name, the log-in data and the preferred seat number
class Student:
    def __init__(self, name, user_name, password, seat):
        self.name = name
        self.user_name = user_name
        self.password = password
        self.seat = seat
        self.bookings = []

    def get_name(self):
        return self.name

    def get_user_name(self):
        return self.user_name

    def get_password(self):
        return self.password

    def get_seat(self):
        return self.seat

    def get_bookings(self):
        for booking in self.bookings:
            booking.display()

    def add_booking(self, booking):
        self.bookings.append(booking)


