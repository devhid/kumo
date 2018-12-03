# utils imports
from utils.constants import HTTP_HEADERS, HTTP_BODY
from utils.namedtuples import StatusCode

class HttpResponse:

    """ A simple class representing an HTTP reponse message. """

    def __init__(self, http_response):
        """ Initializes a new HttpResponse.

        An HttpResponse object contains:
            1) the HTTP headers as a string,
            2) the StatusCode namedtuple obtained from the HTTP headers,
            3) the HTTP body of the response,
            4) the raw HTTP response as a string
        
        The first three attributes may be None if the http_response passed during
        construction was invalid.

        For the StatusCode, refer to get_status_code for more information.

        Parameters
        ----------
        http_response : string
            the HTTP response as a string
        """
        self.headers = HttpResponse.__get_headers(http_response)
        self.status_code = HttpResponse.get_status_code(http_response)
        self.body = HttpResponse.__get_body(http_response)
        self.response = http_response

    @staticmethod
    def get_status_code(http_response):
        """ Gets the HTTP status code from an HTTP response. 
            Does basic validity checking on http_response.

        Parameters
        ----------
        http_response : string
            string representing an HTTP response

        Returns
        -------
        (status_code, interesting_info) or None : (int, depends) or None
            status_code is the HTTP status code, and interesting_info is
            not None only if status_code == '3xx' and a preferred redirect
            link is in the http_response
        """
        # Initialize needed variables.
        lines = http_response.split("\n")
        status_code = 0
        interesting_info = None
        find_interesting_info = False

        # Invalid HTTP response.
        if len(lines) == 0:
            return None

        # Analyze the first line in the response.
        words = lines[0].split(" ")

        # Invalid HTTP response.
        if len(words) < 3:
            return None

        # Extract the status code.
        status_code = words[1]

        # Invalid HTTP response.
        if len(status_code) != 3:
            return None
        
        # Check if the status code is a redirect status code (3xx).
        if status_code[:1] == "3":
            # Extract the preferred redirect URL if there is one.
            find_interesting_info = True

        # Status code is a redirect status code, try to find a preferred redirect URL.
        if find_interesting_info:
            for line in lines:
                words = line.split(" ")
                if len(words) > 1 and words[0] == "Location:":
                    interesting_info = words[1]

        # Return the tuple.
        return StatusCode(status_code=status_code,interesting_info=interesting_info)

    @staticmethod
    def get_data(http_response,headers_body):
        """ Gets either the HTTP headers or HTTP body from an HTTP response.

        Parameters
        ----------
        http_response : string
            string representing an HTTP response
        headers_body : string
            "headers" (constants.HTTP_HEADERS) or "body" (constants.HTTP_BODY)

        Returns
        -------
        data : string or None
            specified data of the HTTP response, or None if http_response is not valid
        """
        if headers_body is not HTTP_HEADERS and \
            headers_body is not HTTP_BODY:
            return None
        if headers_body is HTTP_HEADERS:
            return HttpResponse.__get_headers(http_response)
        else:
            return HttpResponse.__get_body(http_response)

    @classmethod
    def __get_headers(cls,http_response):
        """ Gets the HTTP headers from an HTTP response.

        Parameters
        ----------
        http_response : string
            string representing an HTTP response

        Returns
        -------
        headers : string or None
            HTTP headers of the HTTP response, or None if http_response is not valid
        """
        # Initialize return value.
        headers = http_response

        # HTTP headers end after 2 consecutive newlines (\r\n\r\n)
        newlines = "\r\n\r\n"

        # Invalid HTTP response
        if headers.find(newlines) == -1:
            return None
            
        # Set index to be the start of the body, and return everything after.
        index = headers.find(newlines) + len(newlines)
        headers = headers[:index]
        return headers

    @classmethod
    def __get_body(cls, http_response):
        """ Gets the body from an HTTP response.

        Parameters
        ----------
        http_response : string
            string representing an HTTP response

        Returns
        -------
        body : string or None
            HTML body of the HTTP response, or None if http_response is not valid
        """
        # Initialize return value.
        body = http_response

        # HTTP body must begin after 2 consecutive newlines (\r\n\r\n)
        newlines = "\r\n\r\n"

        # Invalid HTTP response
        if body.find(newlines) == -1:
            return None
            
        # Set index to be the start of the body, and return everything after.
        index = body.find(newlines) + len(newlines)
        body = body[index:]
        return body