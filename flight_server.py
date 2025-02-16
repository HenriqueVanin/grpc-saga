import grpc
from concurrent import futures
import time
import random
import csv
from datetime import datetime

import flight_pb2 as flight_pb2
import flight_pb2_grpc as flight_pb2_grpc

database = "flight_bookings.csv"

def random_boolean():
    return random.choice([True, False])

class FlightService(flight_pb2_grpc.FlightServiceServicer):

    def BookFlight(self, request, context):
        print("FlightService: Booking flight...")

        ticket_details = f"Flight booked from {request.origin} to {request.destination} on {request.date} for {request.number_of_people} people."

        if random_boolean():
            with open(database, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([request.id, request.origin, request.destination, request.date, request.number_of_people, ticket_details, "Active"])

            return flight_pb2.FlightReply(
                ticket_details=ticket_details,
                success=True
            )

        return flight_pb2.FlightReply(
            ticket_details="Flight booking failed.",
            success=False
        )

    def CancelBookFlight(self, request, context):
        print("FlightService: Canceling flight booking...")

        data = []
        found = False

        with open(database, mode="r", newline="") as file:
            reader = csv.reader(file)
            header = next(reader)
            data.append(header)

            for row in reader:
                if row[0] == request.id and row[6] == "Active":
                    row[6] = "Canceled"
                    row[5] = "Flight booking was canceled."
                    found = True
                data.append(row)

        with open(database, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)

        return flight_pb2.FlightReply(
            ticket_details="Flight booking was canceled." if found else "Booking not found or already canceled.",
            success=found
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    flight_pb2_grpc.add_FlightServiceServicer_to_server(FlightService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Flight Service running on port 50052...")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    try:
        with open(database, mode="x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Origin", "Destination", "Date", "People", "Details", "Status"])
    except FileExistsError:
        pass

    serve()
