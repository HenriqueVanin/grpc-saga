import grpc
from concurrent import futures
import time
import random
import csv
from datetime import datetime

import hotel_pb2 as hotel_pb2
import hotel_pb2_grpc as hotel_pb2_grpc

database = "hotel_bookings.csv"

def random_boolean():
    return random.choice([True, False])

class HotelService(hotel_pb2_grpc.HotelServiceServicer):

    def BookHotel(self, request, context):
        print("HotelService: Booking hotel...")

        reservation_details = f"Hotel booked in {request.destination} on {request.date} for {request.number_of_people} people."
        
        if random_boolean():
            with open(database, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([request.id, request.destination, request.date, request.number_of_people, reservation_details, "Active"])

            return hotel_pb2.HotelReply(
                reservation_details=reservation_details,
                success=True
            )

        return hotel_pb2.HotelReply(
            reservation_details="Hotel booking failed.",
            success=False
        )

    def CancelBookHotel(self, request, context):
        print("HotelService: Canceling hotel booking...")

        data = []
        found = False

        with open(database, mode="r", newline="") as file:
            reader = csv.reader(file)
            header = next(reader)
            data.append(header)

            for row in reader:
                if row[0] == request.id and row[5] == "Active":
                    row[5] = "Canceled"
                    row[4] = "Hotel booking was canceled."
                    found = True
                data.append(row)

        with open(database, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)

        return hotel_pb2.HotelReply(
            reservation_details="Hotel booking was canceled." if found else "Booking not found or already canceled.",
            success=found
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hotel_pb2_grpc.add_HotelServiceServicer_to_server(HotelService(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("Hotel Service running on port 50053...")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    try:
        with open(database, mode="x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Destination", "Date", "People", "Details", "Status"])
    except FileExistsError:
        pass

    serve()
