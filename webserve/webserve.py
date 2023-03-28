from threading import RLock
from game.update import Update
from concurrent import futures

import grpc
from . import webserve_pb2_grpc, webserve_pb2

PORT = 8160

class WebserveServicer(webserve_pb2_grpc.WebserveServicer):
    def __init__(self, updates: list, updates_lock: RLock):
        self.updates = updates
        self.updates_lock = updates_lock

    def MoveBall(self, request: webserve_pb2.MoveBallRequest, context) -> webserve_pb2.MoveBallResponse:
        self.updates_lock.acquire()
        self.updates.append(Update(dx = request.x, dy = request.y))
        self.updates_lock.release()

        return webserve_pb2.MoveBallResponse()

def start_grpc(updates: list, updates_lock: RLock):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    webserve_pb2_grpc.add_WebserveServicer_to_server(WebserveServicer(updates, updates_lock), server)

    server.add_insecure_port(f"[::]:{PORT}")
    server.start()

    print(f"Started webserve gRPC server on port {PORT}")
    server.wait_for_termination()

if __name__ == '__main__':
    updates = []
    updates_lock = RLock()

    start_grpc(updates, updates_lock)