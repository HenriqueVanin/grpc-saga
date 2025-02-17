# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import hotel_pb2 as hotel__pb2

GRPC_GENERATED_VERSION = '1.70.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in hotel_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class HotelServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.BookHotel = channel.unary_unary(
                '/hotel.HotelService/BookHotel',
                request_serializer=hotel__pb2.HotelRequest.SerializeToString,
                response_deserializer=hotel__pb2.HotelReply.FromString,
                _registered_method=True)
        self.CancelBookHotel = channel.unary_unary(
                '/hotel.HotelService/CancelBookHotel',
                request_serializer=hotel__pb2.HotelRequest.SerializeToString,
                response_deserializer=hotel__pb2.HotelReply.FromString,
                _registered_method=True)


class HotelServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def BookHotel(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CancelBookHotel(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_HotelServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'BookHotel': grpc.unary_unary_rpc_method_handler(
                    servicer.BookHotel,
                    request_deserializer=hotel__pb2.HotelRequest.FromString,
                    response_serializer=hotel__pb2.HotelReply.SerializeToString,
            ),
            'CancelBookHotel': grpc.unary_unary_rpc_method_handler(
                    servicer.CancelBookHotel,
                    request_deserializer=hotel__pb2.HotelRequest.FromString,
                    response_serializer=hotel__pb2.HotelReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'hotel.HotelService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('hotel.HotelService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class HotelService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def BookHotel(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/hotel.HotelService/BookHotel',
            hotel__pb2.HotelRequest.SerializeToString,
            hotel__pb2.HotelReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def CancelBookHotel(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/hotel.HotelService/CancelBookHotel',
            hotel__pb2.HotelRequest.SerializeToString,
            hotel__pb2.HotelReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
