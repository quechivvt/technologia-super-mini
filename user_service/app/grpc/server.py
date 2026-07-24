import logging
import grpc

from app.grpc import user_pb2_grpc
from app.grpc.service import UserGrpcService

logger = logging.getLogger(__name__)


async def serve():
    server = grpc.aio.server()

    user_pb2_grpc.add_UserServiceServicer_to_server(
        UserGrpcService(),
        server,
    )

    server.add_insecure_port("[::]:50051")

    await server.start()

    logger.info("🚀 gRPC server started on port 50051")

    await server.wait_for_termination()