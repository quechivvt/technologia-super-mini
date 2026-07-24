import logging

logger = logging.getLogger(__name__)


class UserHandler:

    async def handle(
        self,
        event: dict,
    ):

        event_type = event["event"]

        if event_type == "register":
            logger.info(
                "👤 User registered: %s",
                event,
            )

        elif event_type == "login":
            logger.info(
                "🔑 User login: %s",
                event,
            )

        elif event_type == "logout":
            logger.info(
                "🚪 User logout: %s",
                event,
            )

        else:
            logger.warning(
                "Unknown user event: %s",
                event,
            )