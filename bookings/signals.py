from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Passenger
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_ticket(passenger):
    """Generate a PDF ticket for the passenger."""
    if not passenger.flight:
        print(f"Error: Passenger {passenger.id} has no associated flight.")
        return None

    filename = f"ticket_{passenger.id}.pdf"
    filepath = os.path.join("tickets", filename)

    os.makedirs("tickets", exist_ok=True)
    c = canvas.Canvas(filepath, pagesize=letter)
    c.drawString(100, 750, f"Ticket for {passenger.first_name} {passenger.last_name}")
    c.drawString(100, 730, f"Flight: {passenger.flight.flight_number}")
    c.drawString(100, 710, f"Seat: {passenger.seat_number} ({passenger.seat_class})")
    c.drawString(100, 690, f"Status: {passenger.seat_class}")
    c.drawString(100, 670, f"Departure: {passenger.flight.departure}")
    c.drawString(100, 650, f"Arrival: {passenger.flight.arrival}")
    c.save()

    return filepath

@receiver(post_save, sender=Passenger)
def issue_ticket(sender, instance, created, **kwargs):
    if created and instance.seat_class == "Confirmed":
        ticket_path = generate_ticket(instance)
        if ticket_path:
            print(f"Ticket generated at: {ticket_path}")
