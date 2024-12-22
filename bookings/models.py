from django.db import models

# Create your models here.
class Flight(models.Model):

    # Let's Add Seat Classes
    ECONOMY = 'Economy'
    BUSINESS = 'Business'
    FIRST_CLASS = 'First Class'

    SEAT_CLASSES = [
        (ECONOMY, 'Economy'),
        (BUSINESS, 'Business'),
        (FIRST_CLASS, 'First Class'),
    ]

    # Basic Flight Features
    flight_number = models.CharField(max_length=10, unique=True)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    origin = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    capacity = models.IntegerField()

    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=100.00) # Base Price for a Ticket
    seat_classes = models.JSONField(default=dict) # JSON field to manage seat classes and 

    # Let's add dynamic pricing
    def calculate_dynamic_price(self, seat_class):
        """Calculate dynamic pricing based on seat demand."""
        total_seats = self.capacity
        booked_seats = sum(self.seat_classes.values())
        occupancy_rate = booked_seats / total_seats
        multiplier = 1.0

        if occupancy_rate > 0.7:
            multiplier = 1.2 # Increase price by 20% if occupancy is above 70%
        if seat_class == self.BUSINESS:
            multiplier *= 1.5 # Business class costs 50% more
        elif seat_class == self.FIRST_CLASS:
            multiplier *= 2.0 # First class costs twice as much
        
        return float(self.base_price) * multiplier
    
    def __str__(self):
        return f"{self.flight_number} ({self.origin} -> {self.destination})"
    
class Passenger(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    flight = models.ForeignKey(Flight, related_name='passengers', on_delete=models.CASCADE)

    # Seat Selection
    seat_number = models.CharField(max_length=5) # Seat number chosen by the passenger
    seat_class = models.CharField(max_length=20, default="Pending", choices=[
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled")
    ])

    def __str__(self):
        return f"{self.first_name} {self.last_name} - ({self.flight.flight_number})"

# Multi-leg flights can be handled by associating flights via a Many-to-Many relationship
class Booking(models.Model):
    flights = models.ManyToManyField(Flight, related_name="bookings")
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name="bookings")
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calculate_total_price(self):
        """Calculate total price for multi-leg flights."""
        self.total_price = sum(
            Flight.calculate_dynamic_price(self.passenger.seat_class) for flight in self.flights.all()
        )
        self.save()

#