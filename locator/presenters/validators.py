from clientlocator.exceptions import ClientLocatorException
from locator.infra.interfaces import IValidator


class LocatorValidator(IValidator):
    @staticmethod
    def validate(value: bool) -> bool:
        return value

    def is_empty_payload(self, payload) -> (bool, Exception):
        """
          Checks if is a empty payload
        """
        if isinstance(payload, (dict, list, bytes)):
            return True
        else:
            raise ClientLocatorException(
                source="validator",
                code="empty_payload",
                message="Payload in request is empty",
            )

    def validate_coordinates(self, coordinates: dict) -> (bool, Exception):
        """
            Checks if the coordinates has latitude and longitude params
        """
        if "lat" not in coordinates:
            raise ClientLocatorException(
                source="validator",
                code="field_not_exists",
                message="Field required in coordinates: lat",
            )

        if "lon" not in coordinates:
            raise ClientLocatorException(
                source="validator",
                code="field_not_exists",
                message="Field required in coordinates: lon",
            )

        return True

    def validate_payload(self, payload: dict) -> list:
        """
            Checks all payload
        """

        self.is_empty_payload(payload)

        if "pageNumber" not in payload:
            raise ClientLocatorException(
                source="validator",
                code="field_not_exists",
                message="Field required: pageNumber",
            )

        if "pageSize" not in payload:
            raise ClientLocatorException(
                source="validator",
                code="field_not_exists",
                message="Field required: pageSize",
            )

        if "coordinates" not in payload:
            raise ClientLocatorException(
                source="validator",
                code="field_not_exists",
                message="Field required: coordinates",
            )

        self.validate_coordinates(payload["coordinates"])

        return self.validate(True)
