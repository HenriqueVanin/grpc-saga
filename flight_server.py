import grpc
from concurrent import futures
import time

import flight_pb2 as flight_pb2
import flight_pb2_grpc as flight_pb2_grpc

class FlightService(flight_pb2_grpc.FlightServiceServicer):
    def BookFlight(self, request, context):
        print("FlightService: Booking flight...")
        ticket_details = f"Flight booked from {request.origin} to {request.destination} on {request.date} for {request.number_of_people} people."
        
        return flight_pb2.FlightReply(
            ticket_details=ticket_details,
            success=True
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
    serve()
