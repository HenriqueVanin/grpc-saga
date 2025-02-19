import grpc
from concurrent import futures
import time
import csv
import uuid
from datetime import datetime

import agency_pb2 as agency_pb2
import agency_pb2_grpc as agency_pb2_grpc
import hotel_pb2 as hotel_pb2
import hotel_pb2_grpc as hotel_pb2_grpc
import car_pb2 as car_pb2
import car_pb2_grpc as car_pb2_grpc
import flight_pb2 as flight_pb2
import flight_pb2_grpc as flight_pb2_grpc

database = "agency_bookings.csv"

class AgencyService(agency_pb2_grpc.AgencyServiceServicer):
    def BookFlightCompensation(self, request, context):
        with grpc.insecure_channel('localhost:50052') as flight_channel:
            flight_stub = flight_pb2_grpc.FlightServiceStub(flight_channel)
            flight_response = flight_stub.CancelBookFlight(flight_pb2.FlightRequest(
                id=request.id,
                origin=request.origin,
                destination=request.destination,
                date=request.date,
                number_of_people=request.number_of_people
            ))
            return flight_response.ticket_details

    def BookHotelCompensation(self, request, context):
        with grpc.insecure_channel('localhost:50053') as hotel_channel:
            hotel_stub = hotel_pb2_grpc.HotelServiceStub(hotel_channel)
            hotel_response = hotel_stub.CancelBookHotel(hotel_pb2.HotelRequest(
                id=request.id,
                destination=request.destination,
                date=request.date,
                number_of_people=request.number_of_people
            ))
            return hotel_response.reservation_details

    def BookCarCompensation(self, request, context):
        with grpc.insecure_channel('localhost:50054') as car_channel:
            car_stub = car_pb2_grpc.CarServiceStub(car_channel)
            car_response = car_stub.CancelRentCar(car_pb2.CarRequest(
                id=request.id,
                pickup_location=request.destination,
                date=request.date,
                number_of_people=request.number_of_people
            ))
            return car_response.reservation_details

    def BuyTicket(self, request, context):
        hotel_details = "Not included"
        car_details = "Not included"
        flight_details = "Agency failed"

        with grpc.insecure_channel('localhost:50052') as flight_channel:
            flight_stub = flight_pb2_grpc.FlightServiceStub(flight_channel)
            flight_response = flight_stub.BookFlight(flight_pb2.FlightRequest(
                origin=request.origin,
                destination=request.destination,
                date=request.date,
                number_of_people=request.number_of_people,
                id=request.id
            ))
            if flight_response.success:
                flight_details = flight_response.ticket_details
            else:
                flight_details = self.BookFlightCompensation(request, context)
                return agency_pb2.AgencyReply(
                    message="Your ticket could not be booked. Book flight failed.",
                    flight_details=flight_details,
                    success=False,
                    id=request.id
                )

        if request.include_hotel:
            with grpc.insecure_channel('localhost:50053') as hotel_channel:
                hotel_stub = hotel_pb2_grpc.HotelServiceStub(hotel_channel)
                hotel_response = hotel_stub.BookHotel(hotel_pb2.HotelRequest(
                    destination=request.destination,
                    date=request.date,
                    number_of_people=request.number_of_people,
                    id=request.id
                ))
                if hotel_response.success:
                    hotel_details = hotel_response.reservation_details
                else:
                    flight_details = self.BookFlightCompensation(request, context)
                    hotel_details = self.BookHotelCompensation(request, context)
                    return agency_pb2.AgencyReply(
                        message="Your ticket could not be booked. Book hotel failed.",
                        flight_details=flight_details, 
                        hotel_details=hotel_details,
                        success=False,
                        id=request.id
                    )

        if request.include_car:
            with grpc.insecure_channel('localhost:50054') as car_channel:
                car_stub = car_pb2_grpc.CarServiceStub(car_channel)
                car_response = car_stub.RentCar(car_pb2.CarRequest(
                    pickup_location=request.destination,
                    date=request.date,
                    number_of_people=request.number_of_people,
                    id=request.id
                ))
                if car_response.success:
                    car_details = car_response.reservation_details
                else:
                    flight_details = self.BookFlightCompensation(request, context)
                    hotel_details = self.BookHotelCompensation(request, context)
                    car_details = self.BookCarCompensation(request, context)
                    return agency_pb2.AgencyReply(
                        message="Your ticket could not be booked. Book car failed.",
                        flight_details=flight_details, 
                        hotel_details=hotel_details,
                        car_details=car_details,
                        success=False,
                        id=request.id
                    )

        return agency_pb2.AgencyReply(
            id=request.id,
            message="Agency completed!",
            success=True,
            hotel_details=hotel_details,
            car_details=car_details,
            flight_details=flight_details
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    agency_pb2_grpc.add_AgencyServiceServicer_to_server(AgencyService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Agency Service running on port 50051...")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
