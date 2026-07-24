from app.grpc import user_pb2
from app.grpc import user_pb2_grpc


class UserGrpcService(
    user_pb2_grpc.UserServiceServicer,
):

    async def GetUser(
        self,
        request,
        context,
    ):

        return user_pb2.UserResponse(
            user_id=request.user_id,
            username="Que Chi",
            email="test@gmail.com",
        )