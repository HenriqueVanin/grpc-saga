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

# Função para salvar reserva no CSV
def save_booking(request, flight_details, hotel_details, car_details, success):
    booking_id = request.id if request.id else str(uuid.uuid4())  # Usa ID existente ou gera um novo
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "Active" if success else "Failed"

    data = {
        "id": booking_id,
        "origin": request.origin,
        "destination": request.destination,
        "date": request.date,
        "number_of_people": request.number_of_people,
        "include_hotel": request.include_hotel,
        "include_car": request.include_car,
        "status": status,
        "flight_details": flight_details,
        "hotel_details": hotel_details,
        "car_details": car_details,
        "created_at": created_at
    }

    file_exists = False
    try:
        with open(database, "r") as f:
            file_exists = True
    except FileNotFoundError:
        pass

    with open(database, mode="a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(data.keys())  # Cabeçalho

        writer.writerow(data.values())  # Dados

    return booking_id

# Função para atualizar reserva cancelada no CSV
def update_booking_status(booking_id):
    rows = []
    
    with open(database, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["id"] == booking_id:
                row["status"] = "Cancelled"
            rows.append(row)

    with open(database, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

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
            update_booking_status(request.id)
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
            update_booking_status(request.id)
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
            update_booking_status(request.id)
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

        save_booking(request, flight_details, hotel_details, car_details, True)

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
