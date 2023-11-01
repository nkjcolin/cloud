import grpc
import booking_pb2 as booking_pb2
import booking_pb2_grpc as booking_pb2_grpc

def make_booking_with_grpc(name, phone_number, email, timing, size):
    # Create a gRPC channel to the server
    channel = grpc.insecure_channel('localhost:50051')  # Replace with your server's address

    # Create a stub for the BookingService
    stub = booking_pb2_grpc.BookingServiceStub(channel)

    # Create a BookingRequest message
    booking_request = booking_pb2.BookingRequest(
        name=name,
        phone=phone_number,
        email=email,
        timing=timing,
        size=size
    )

    # Make a gRPC request to the server
    response = stub.Booking(booking_request)

    return response
