from concurrent import futures
import grpc
import booking_pb2 as pb2
import booking_pb2_grpc as pb2_grpc

class BookingService(pb2_grpc.BookingServiceServicer):
    def Booking(self, request, context):
        # Implement your reservation logic here
        response = pb2.BookingReply(
            name=request.name,
            phone=request.phone,
            email=request.email,
            timing = request.timing,
            size = request.size
        )
        return response

def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_BookingServiceServicer_to_server(BookingService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    run_server()
