from rest_framework import serializers
from .models import Flight, Passenger, Booking

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'

class PassengerSerializer(serializers.ModelSerializer):
    flight_details = FlightSerializer(source='flight', read_only=True)

    class Meta:
        model = Passenger
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    passenger_details = PassengerSerializer(source='passenger', read_only=True)
    flight_details = FlightSerializer(source='flights', many=True, read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'