import uuid
import grpc
import agency_pb2 as agency_pb2
import agency_pb2_grpc as agency_pb2_grpc
import tkinter as tk
from tkinter import messagebox

def submit_request():
    # Get the values from the input fields
    date = entry_date.get()
    origin = entry_origin.get()
    destination = entry_destination.get()
    number_of_people = int(entry_people.get())
    include_hotel = var_hotel.get()
    include_car = var_car.get()

    # Create a request message
    request = agency_pb2.AgencyRequest(
        id=str(uuid.uuid4()),
        date=date,
        origin=origin,
        destination=destination,
        number_of_people=number_of_people,
        include_hotel=include_hotel,
        include_car=include_car
    )

    try:
        # Create a gRPC channel and stub
        channel = grpc.insecure_channel('localhost:50051')
        stub = agency_pb2_grpc.AgencyServiceStub(channel)

        # Call the BuyTicket RPC method
        response = stub.BuyTicket(request)

        # Show the result in a message box
        messagebox.showinfo("Response from server", 
                            f"Message: {'successful' if response.success else 'aborted'}\n\n"
                            f"Airline ticket purchase was {response.message}\n\n"
                            f"Services Responses\n\n"
                            f"Flight Details: {response.flight_details}\n"
                            f"Hotel Details: {response.hotel_details}\n"
                            f"Car Details: {response.car_details}\n")

    except grpc.RpcError as e:
        print("RPC Error", f"RPC failed: {e.code()}: {e.details()}")

# Create the main window
root = tk.Tk()
root.title("Travel Agency Client")

# Create input fields
tk.Label(root, text="Date (YYYY-MM-DD)").pack()
entry_date = tk.Entry(root)
entry_date.pack()

tk.Label(root, text="Origin").pack()
entry_origin = tk.Entry(root)
entry_origin.pack()

tk.Label(root, text="Destination").pack()
entry_destination = tk.Entry(root)
entry_destination.pack()

tk.Label(root, text="Number of People").pack()
entry_people = tk.Entry(root)
entry_people.pack()

var_hotel = tk.BooleanVar()
tk.Checkbutton(root, text="Include hotel?", variable=var_hotel).pack()

var_car = tk.BooleanVar()
tk.Checkbutton(root, text="Include car rental?", variable=var_car).pack()

# Submit button
submit_btn = tk.Button(root, text="Submit", command=submit_request)
submit_btn.pack()

# Run the application
root.mainloop()
