from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from restaurant.services.domain.table import Table

from typing import Optional
from restaurant.utils.result import Result

class Reservation:
    class Status:
        BOOKED = 'BOOKED'
        ATTENDED = 'ATTENDED'
        NOT_ATTENDED = 'NOT_ATTENDED'
        CANCELLED = 'CANCELLED'

        CHOICES = [
            (BOOKED, 'Booked'),
            (ATTENDED, 'Attended'),
            (NOT_ATTENDED, 'Not Attended'),
            (CANCELLED, 'Cancelled'),
        ]

    def __init__(
        self,
        name: str,
        email: str,
        phone_number: str,
        customer_number: int,
        reservation_date: datetime,
        status: str = Status.BOOKED,
        table: Table = None,
        created_at: Optional[datetime] = None,
        cancelled_at: Optional[datetime] = None,
    ):
        self.name = name
        self.email = email
        self.customer_number = customer_number
        self.phone_number = phone_number
        self.table = table
        self.reservation_date = reservation_date
        self.status = status
        self.created_at = created_at or datetime.now()
        self.cancelled_at = cancelled_at


    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.reservation_date}"


    def cancel(self):
        if self.status == self.Status.CANCELLED:
            raise ValueError("Reservation is already cancelled.")
        self.status = self.Status.CANCELLED
        self.cancelled_at = datetime.now()


    def attend(self):
        if self.status == self.Status.CANCELLED:
            raise ValueError("Cannot mark a cancelled reservation as attended.")
        self.status = self.Status.ATTENDED


    def mark_not_attended(self):
        if self.status == self.Status.CANCELLED:
            raise ValueError("Cannot mark a cancelled reservation as not attended.")
        self.status = self.Status.NOT_ATTENDED


    def assing_table(table : Table):
        self.table = table


    def validate_date(self) -> Result:
        reservation_date = self.reservation_date
        now = datetime.now()
        max_date_allowed = now.date() + relativedelta(months=1)  
        
        # Assert Future
        if reservation_date < now:
            return Result.error("Reservations must be made for a future date.")
        
        # Assert Not Booked At same Day
        if reservation_date.date() == now.date():
            return Result.error("Same-day reservations are not allowed.")

        # Assert 1 Month Range
        if reservation_date > max_date_allowed:
            return Result.error("Reservations can only be made up to one month in advance.")
        
        return Result.success()


    def validate_customer_limit(self) -> Result:
        if self.customer_number > 15:
            return Result.error("Reservation can't be above 15 customers")

        return Result.success()