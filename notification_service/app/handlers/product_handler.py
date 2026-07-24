import logging

logger = logging.getLogger(__name__)


class ProductHandler:

    async def handle(
        self,
        event: dict,
    ):

        event_type = event["event"]

        if event_type == "created":
            logger.info(
                "📦 Product created: %s",
                event,
            )

        elif event_type == "updated":
            logger.info(
                "✏️ Product updated: %s",
                event,
            )

        elif event_type == "deleted":
            logger.info(
                "🗑️ Product deleted: %s",
                event,
            )

        else:
            logger.warning(
                "Unknown product event: %s",
                event,
            )