import grpc
from concurrent import futures
import time

import car_pb2 as car_pb2
import car_pb2_grpc as car_pb2_grpc

class CarService(car_pb2_grpc.CarServiceServicer):
    def RentCar(self, request, context):
        print("CarService: Renting car...")
        reservation_details = f"Car rented at {request.pickup_location} on {request.date} for {request.number_of_people} people."
        
        return car_pb2.CarReply(
            reservation_details=reservation_details,
            success=True
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
    serve()
