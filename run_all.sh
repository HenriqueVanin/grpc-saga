#!/bin/bash

echo "Starting Flight Service..."
gnome-terminal -- bash -c "python3 flight_server.py; exec bash"

echo "Starting Hotel Service..."
gnome-terminal -- bash -c "python3 hotel_server.py; exec bash"

echo "Starting Car Service..."
gnome-terminal -- bash -c "python3 car_server.py; exec bash"

echo "Starting Agency Service..."
gnome-terminal -- bash -c "python3 agency_server.py; exec bash"

echo "Starting Client Interface..."
gnome-terminal -- bash -c "python3 agency_client_gui.py; exec bash"

echo "All services are running."
