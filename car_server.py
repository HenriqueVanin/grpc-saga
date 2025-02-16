import grpc
from concurrent import futures
import time
import random
import csv
from datetime import datetime

import car_pb2 as car_pb2
import car_pb2_grpc as car_pb2_grpc

database = "car_rentals.csv"

def random_boolean():
    return random.choice([True, False])

class CarService(car_pb2_grpc.CarServiceServicer):
    def RentCar(self, request, context):
        print("CarService: Renting car...")

        reservation_details = f"Car rented at {request.pickup_location} on {request.date} for {request.number_of_people} people."

        if random_boolean():
            with open(database, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([request.id, request.pickup_location, request.date, request.number_of_people, reservation_details, "Active"])

            return car_pb2.CarReply(
                reservation_details=reservation_details,
                success=True
            )

        return car_pb2.CarReply(
            reservation_details="Car rental failed.",
            success=False
        )

    def CancelRentCar(self, request, context):
        print("CarService: Canceling car rental...")

        data = []
        found = False

        with open(database, mode="r", newline="") as file:
            reader = csv.reader(file)
            header = next(reader)
            data.append(header)

            for row in reader:
                if row[0] == request.id and row[5] == "Active":
                    row[5] = "Canceled"
                    row[4] = "Car rental was canceled."
                    found = True
                data.append(row)

        with open(database, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)

        return car_pb2.CarReply(
            reservation_details="Car rental was canceled." if found else "Booking not found or already canceled.",
            success=found
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    car_pb2_grpc.add_CarServiceServicer_to_server(CarService(), server)
    server.add_insecure_port('[::]:50054')
    server.start()
    print("Car Service running on port 50054...")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    try:
        with open(database, mode="x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Pickup Location", "Date", "People", "Details", "Status"])
    except FileExistsError:
        pass

    serve()
