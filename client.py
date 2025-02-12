import grpc
import agency_pb2 as agency_pb2
import agency_pb2_grpc as agency_pb2_grpc

def run():
    # Create a gRPC channel to connect to the server (adjust the address if necessary)
    channel = grpc.insecure_channel('localhost:50051')
    stub = agency_pb2_grpc.AgencyServiceStub(channel)

    # Collect inputs from the user
    print("Enter the details for your trip:")

    date = input("Date (YYYY-MM-DD): ")
    origin = input("Origin: ")
    destination = input("Destination: ")
    number_of_people = int(input("Number of people: "))
    include_hotel = input("Include hotel? (yes/no): ").lower() == 'yes'
    include_car = input("Include car rental? (yes/no): ").lower() == 'yes'

    # Create a request message
    request = agency_pb2.AgencyRequest(
        date=date,
        origin=origin,
        destination=destination,
        number_of_people=number_of_people,
        include_hotel=include_hotel,
        include_car=include_car
    )

    try:
        # Call the BuyTicket RPC method with the request
        response = stub.BuyTicket(request)

        # Print the response from the server
        print("\nResponse from server:")
        print(f"Message: {response.message}")
        print(f"Success: {response.success}")
        if response.success:
            print(f"Hotel Details: {response.hotel_details}")
            print(f"Car Details: {response.car_details}")
            print(f"Flight Details: {response.flight_details}")

    except grpc.RpcError as e:
        print(f"RPC failed: {e.code()}: {e.details()}")

if __name__ == '__main__':
    run()
