import grpc
from concurrent import futures
import time

import hotel_pb2 as hotel_pb2
import hotel_pb2_grpc as hotel_pb2_grpc

class HotelService(hotel_pb2_grpc.HotelServiceServicer):
    def BookHotel(self, request, context):
        print("HotelService: Booking hotel...")
        reservation_details = f"Hotel booked in {request.destination} on {request.date} for {request.number_of_people} people."
        
        return hotel_pb2.HotelReply(
            reservation_details=reservation_details,
            success=True
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
    serve()
