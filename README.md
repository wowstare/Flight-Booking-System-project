# Flight Booking System ✈️

A lightweight command-line interface (CLI) system for fast and simple flight reservations, designed for users who prioritize efficiency over visual complexity.



## 🚀 Features
- **3-Step Booking**: Search → Select → Confirm
- **Offline Functionality**: No internet required after setup
- **Bulk Booking Ready**: Edit JSON files directly for group reservations
- **Senior-Friendly**: Text-only interface with large font compatibility

## ⚙️ Installation

1. **Prerequisites**:  
   Ensure Python 3.10+ is installed:
   ```bash
   python --version
   
   Clone & Navigate:

   git clone https://github.com/narges/flight-booking-system.git
cd flight-booking-system

Sample Data Setup:
Create flights.json with airline data:

[
  {
    "flight_number": "AA101",
    "origin": "New York",
    "destination": "London",
    "departure": "2024-07-15T08:00:00",
    "price": 450.0
  }
]

 Usage
 Start System:
 python flight_booking.py

 Menu Options:

 1. Search Flights    : Find by origin/destination/date
2. Book Flight      : Reserve selected flight
3. View Bookings    : Check reservations by name
4. Exit             : Quit program

   Example Workflow:
   Enter origin > New York
Enter destination > London
Enter date (YYYY-MM-DD) > 2025-07-15

🛠️ Technologies :
Component     	     Technology	                   Purpose
Core Language       	Python 3.10             	 CLI logic and flow control
Data Storage	        JSON                     	Flight/booking persistence
Date Handling	        datetime	                  Flight scheduling/validation
File Management	       os	                         Safe file operations  

Project Structure
flight-booking-system/
├── flight_booking.py   # Main application logic
├── flights.json        # Flight database 
├── bookings.json       # Auto-generated booking records
├── README.md           # This documentation
            
 Future Improvements
Booking Modifications: Add cancellation/editing

Enhanced Search: Filter by price/time/airline

CSV Import/Export: For travel agency bulk operations

Voice Interface: For hands-free operation

Email Notifications: Booking confirmations
                                                   

   
