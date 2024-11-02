from rest_framework.exceptions import APIException


class InactiveTagException(APIException):
    status_code = 400  # Bad Request or use an appropriate status code
    default_detail = "The specified tag is not active."

    def __init__(self, tag):
        detail = f"The {tag.name} tag is not active."
        super().__init__(detail=detail)
