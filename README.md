
---

# Airline System API

Welcome to the **Airline System API**! This Django-based API allows users to manage flight bookings, passengers, and flight details. It integrates various features, including dynamic pricing, seat selection, and ticket issuance, with RESTful endpoints to interact with flight-related data.

## Project Setup

This section explains how to set up and run the project.

### Prerequisites

Ensure you have the following installed:

- Python 3.12 or above
- Django 5.x
- Django REST Framework
- SQLite (default database) or another database if you prefer

### Installation Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/airline-system-116533.git
    cd airline-system-116533
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations to set up the database:**

    ```bash
    python manage.py migrate
    ```

5. **Run the server:**

    ```bash
    python manage.py runserver
    ```

Your API should now be accessible at `http://127.0.0.1:8000/api/`.

## API Endpoints

The following are the available endpoints for interacting with the API:

### **/api/flights/**
- **GET**: Retrieve a list of all flights.
- **POST**: Create a new flight.

### **/api/flights/{id}/**
- **GET**: Retrieve details for a specific flight.
- **PUT**: Update a flight's details.
- **DELETE**: Delete a flight.

### **/api/passengers/**
- **GET**: Retrieve a list of all passengers.
- **POST**: Add a new passenger.

### **/api/passengers/{id}/**
- **GET**: Retrieve a specific passenger’s details.
- **PUT**: Update passenger details.
- **DELETE**: Remove a passenger.

### **/api/bookings/**
- **GET**: Retrieve a list of all bookings.
- **POST**: Create a new booking.

### **/api/bookings/{id}/**
- **GET**: Retrieve booking details for a specific booking.
- **PUT**: Update a booking.
- **DELETE**: Cancel a booking.

## Models

The system is designed with three key models:

### **Flight**
The `Flight` model contains the details of each flight, such as flight number, departure/arrival times, origin/destination, capacity, base price, and seat classes.

- **seat_classes (JSONField)**: Allows dynamic seat class management, supporting Economy, Business, and First-Class seat options.
- **calculate_dynamic_price()**: A method that calculates the dynamic price based on seat demand and class.

### **Passenger**
The `Passenger` model holds details about the passengers such as their first and last names, email, phone number, and their flight selection.

- **seat_class**: The seat class assigned to the passenger (e.g., Pending, Confirmed, Cancelled).

### **Booking**
The `Booking` model tracks a booking with multiple flights and one passenger. It calculates the total price of the booking based on the selected flights and seat classes.

- **calculate_total_price()**: A method to calculate the total price for a booking, considering dynamic pricing of flights.

## Serializers

Serializers convert complex data types like Django models into JSON format that can be easily rendered into a response or sent as input for API requests.

- **FlightSerializer**: Serializes the `Flight` model.
- **PassengerSerializer**: Serializes the `Passenger` model and includes flight details.
- **BookingSerializer**: Serializes the `Booking` model, including passenger and flight details.

## Views and Viewsets

Django REST Framework's `viewsets.ModelViewSet` is used to handle the CRUD operations for each model. These viewsets automatically provide actions like list, create, update, and delete.

- **FlightViewSet**: Handles operations related to flights.
- **PassengerViewSet**: Handles operations related to passengers.
- **BookingViewSet**: Manages bookings and calculates total booking prices.

## Signals

The system includes a signal to generate PDF tickets when a new `Passenger` is created with a confirmed seat class.

- **issue_ticket()**: A signal that generates a PDF ticket for the passenger and stores it in a designated directory.

## Notable Design Decisions

- **Seat Classes & Dynamic Pricing**: A JSON field is used in the `Flight` model to manage seat classes, which makes it easy to adjust pricing dynamically. The method `calculate_dynamic_price()` calculates ticket prices based on the occupancy rate and seat class.
- **PDF Ticket Generation**: The use of Django signals allows for automatic PDF ticket generation when a passenger is confirmed. The `ReportLab` library is used for generating these tickets.
- **Many-to-Many Relationships**: The `Booking` model uses a many-to-many relationship with the `Flight` model, supporting multi-leg flights.

## Testing

1. **Create test data** by using the Django Admin panel or creating test cases in the Django shell.
2. **Test API** by using tools like Postman, or directly through the browser for GET requests. Make sure you test both `GET`, `POST`, `PUT`, and `DELETE` actions.

## Contributing

If you would like to contribute to this project, please feel free to fork the repository and submit a pull request. Contributions are welcome!

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---