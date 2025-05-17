import json
from datetime import datetime
import os

def load_flights():
    file_path = 'flight.json'
    print(f"Attempting to load flights from: {os.path.abspath(file_path)}") # Print absolute path for debugging
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: '{file_path}' not found in the current directory '{os.getcwd()}'.")
        print("Please make sure 'flights.json' exists in the same directory as the script.")
        return []
    except json.JSONDecodeError:
        print(f"Error reading '{file_path}'. Make sure it is valid JSON.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while loading flights: {e}")
        return []

def save_bookings(bookings):
    try:
        with open('bookings.json', 'w') as f:
            json.dump(bookings, f, indent=4)
    except Exception as e:
        print(f"Error saving bookings: {e}")

def search_flights():
    flights = load_flights()
    if not flights:
        print("Cannot search flights as flight data failed to load or is empty.")
        return [] # Return empty list to avoid issues in book_flight
    
    origin = input("Enter origin: ").strip()
    destination = input("Enter destination: ").strip()
    date_str = input("Enter date (YYYY-MM-DD): ").strip() # Removed non-English text
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return [] # Return empty list
    
    matching_flights = []
    for f in flights:
        try:
            # Ensure all required keys exist and departure is a valid datetime string
            if all(k in f for k in ('origin', 'destination', 'departure', 'flight_number', 'price')):
                flight_departure_date = datetime.strptime(f['departure'], '%Y-%m-%dT%H:%M:%S').date()
                if (f['origin'].lower() == origin.lower() and
                    f['destination'].lower() == destination.lower() and
                    flight_departure_date == date):
                    matching_flights.append(f)
            else:
                print(f"Warning: Skipping flight due to missing data: {f.get('flight_number', 'Unknown')}")
        except ValueError:
             print(f"Warning: Skipping flight due to invalid departure format: {f.get('flight_number', 'Unknown')}")
        except Exception as e:
             print(f"Warning: Skipping flight due to unexpected error: {f.get('flight_number', 'Unknown')} - {e}")

    if not matching_flights:
        print("No flights found for the given criteria.")
        return []
    else:
        print("\nAvailable Flights:")
        for idx, flight in enumerate(matching_flights, 1):
            print(f"{idx}. Flight {flight['flight_number']} from {flight['origin']} to {flight['destination']} on {flight['departure'][:10]} - Price: ${flight['price']}")
        return matching_flights

def book_flight():
    matching_flights = search_flights()
    # Check if search_flights returned a list (even if empty) or None (if loading failed)
    if matching_flights is None or not isinstance(matching_flights, list):
        print("Booking cannot proceed as flight search failed or returned invalid data.")
        return
    if not matching_flights: # Handles case where search returned empty list
        print("No flights available to book based on your search.")
        return

    choice = input("Enter the number of the flight you want to book (or '0' to cancel): ").strip()
    
    if choice == '0':
        print("Booking cancelled.")
        return
    
    try:
        flight_idx = int(choice) - 1
        if 0 <= flight_idx < len(matching_flights):
            selected_flight = matching_flights[flight_idx]
            user_name = input("Enter your name: ").strip()
            if not user_name:
                print("Name cannot be empty.")
                return
            
            booking = {
                "user_name": user_name,
                "flight_number": selected_flight['flight_number'],
                "origin": selected_flight['origin'],
                "destination": selected_flight['destination'],
                "departure": selected_flight['departure'],
                "price": selected_flight['price'],
                "booking_date": datetime.now().isoformat()
            }
            
            bookings = []
            # Load existing bookings safely
            if os.path.exists('bookings.json'):
                try:
                    with open('bookings.json', 'r') as f:
                        # Check if file is empty before loading
                        content = f.read()
                        if content:
                            bookings = json.loads(content)
                        if not isinstance(bookings, list):
                            print("Warning: 'bookings.json' does not contain a list. Starting with empty bookings.")
                            bookings = []
                except json.JSONDecodeError:
                    print("Error reading bookings.json. Starting with empty bookings.")
                    bookings = [] # Ensure bookings is a list
                except Exception as e:
                    print(f"Error loading bookings.json: {e}. Starting with empty bookings.")
                    bookings = []
            
            bookings.append(booking)
            save_bookings(bookings)
            print(f"Booking successful for {user_name} on flight {selected_flight['flight_number']}!")
        else:
            print("Invalid flight number.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    except Exception as e:
        print(f"An unexpected error occurred during booking: {e}")

def view_bookings():
    user_name = input("Enter your name: ").strip()
    if not user_name:
        print("Name cannot be empty.")
        return
    
    bookings = []
    # Load existing bookings safely
    if os.path.exists('bookings.json'):
        try:
            with open('bookings.json', 'r') as f:
                content = f.read()
                if content:
                    bookings = json.loads(content)
                if not isinstance(bookings, list):
                    print("Warning: 'bookings.json' does not contain a list. Cannot view bookings.")
                    return
        except json.JSONDecodeError:
            print("Error reading bookings.json. Cannot view bookings.")
            return
        except Exception as e:
            print(f"Error loading bookings.json: {e}. Cannot view bookings.")
            return
    
    user_bookings = [b for b in bookings if b.get('user_name', '').lower() == user_name.lower()]
    
    if not user_bookings:
        print("No bookings found for this user.")
    else:
        print(f"\nBookings for {user_name}:")
        for idx, booking in enumerate(user_bookings, 1):
            # Check for key existence before accessing
            flight_num = booking.get('flight_number', 'N/A')
            origin = booking.get('origin', 'N/A')
            dest = booking.get('destination', 'N/A')
            dep_date = booking.get('departure', 'N/A')[:10]
            price = booking.get('price', 'N/A')
            book_date = booking.get('booking_date', 'N/A')[:10]
            print(f"{idx}. Flight {flight_num} from {origin} to {dest} on {dep_date} - Price: ${price}, Booked on: {book_date}")

def main():
    # Create dummy files if they don't exist, to prevent initial errors
    if not os.path.exists('flights.json'):
        print("Creating empty 'flights.json'. Please populate it with flight data.")
        with open('flights.json', 'w') as f:
            json.dump([], f)
    if not os.path.exists('bookings.json'):
        print("Creating empty 'bookings.json'.")
        with open('bookings.json', 'w') as f:
            json.dump([], f)
            
    while True:
        print("\n--- Flight Booking System Menu ---")
        print("1. Search Flights")
        print("2. Book Flight")
        print("3. View My Bookings")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            search_flights()
        elif choice == '2':
            book_flight()
        elif choice == '3':
            view_bookings()
        elif choice == '4':
            print("Thank you for using the Flight Booking System!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

