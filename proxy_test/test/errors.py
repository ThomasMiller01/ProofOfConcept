"""Exception Hierarchy

- :class:`GermanCollectorsException`
    - :class:`ClientLoopError`
    - :class:`HealthCheckError`
        - :class:`SerializationError`
        - :class:`GeneralError`
    - :class:`RequestsError`
        - :class:`InvalidStatusCode`
    - :class:`ProxyError`
        - :class:`ProxyRequestError`
        - :class:`InvalidProxy`
    - :class:`TwitterError`
    - :class:`ShopmonitorError`
        - :class:`ShopmonitorLoopError`
"""

from datetime import datetime
import pytz
import traceback
import json

from time_util import getCurrentDatetime


class GermanCollectorsException(Exception):
    """GermanCollectors Exception
    
    Base exception for the GermanCollectors bot.

    This class can be used to handle any exception thrown by this bot.

    :param e: exception
    :type e: Exception, optional

    :param traceback: traceback of the exception
    :type traceback: str, got from ``e``
    """
    def __init__(self, e=None):        
        if e != None:
            self.e = e
            self.traceback = exception_traceback = '\n'.join(traceback.format_exception(type(e), e, e.__traceback__))
        self.when = getCurrentDatetime()

    def __str__(self):
        data = {
            "GermanCollectorsException": {
                "when": self.when.strftime('%Y-%m-%d %H:%M:%S'),                
            }
        }
        if hasattr(self, "e"):
            data["GermanCollectorsException"]["e"] = str(self.e)
            data["GermanCollectorsException"]["traceback"] = str(self.traceback)            
        
        json_string = json.dumps(data)

        return json_string


class HealthCheckError(GermanCollectorsException):
    """HealthCheck Error

    Error that are logged to :class:`~features.healthCheck_feature.healthCheck_feature`.        
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        data = {
            "base": json.loads(super().__str__()),
            "HealthCheckError": ""
        }

        json_string = json.dumps(data)

        return json_string        


class SerializationError(HealthCheckError):
    """Serialization Error

    This error occurrs when an exception is raised during the serialization of the health-check data.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        data = {
            "base": json.loads(super().__str__()),
            "SerializationError": ""
        }

        json_string = json.dumps(data)

        return json_string


class GeneralError(HealthCheckError):
    """General Error

    An error that will be logged to :class:`~features.healthCheck_feature.healthCheck_feature`.

    :param message: `message` contains more specific information about the exception
    :type message: str
    """
    def __init__(self, message, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.message = message  

    def __str__(self):
        data = {
            "base": json.loads(super().__str__()),
            "GeneralError": {
                "message": self.message
            }
        }

        json_string = json.dumps(data)

        return json_string        


class RequestsError(GermanCollectorsException):
    """Requests Errors

    Errors that occurred while fetching data with the `requests` library.

    :param url: url of the request, that failed
    :type url: str
    """
    def __init__(self, url, *args, **kwargs):
        super().__init__(*args, **kwargs)    

        self.url = url       

    def __str__(self):
        data = {
            "base": json.loads(super().__str__()),
            "RequestsError": {
                "url": self.url
            }
        }

        json_string = json.dumps(data)

        return json_string


class InvalidStatusCode(RequestsError):
    """InvalidStatusCode Error

    This error occurrs, when a request returns with a status_code other than ``200``.

    :param status_code: the invalid status_code
    :type status_code: int
    """
    def __init__(self, status_code, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.status_code = status_code

    def __str__(self):
        data = {
            "base": json.loads(super().__str__()),
            "InvalidStatusCode": {
                "status_code": str(self.status_code)
            }
        }

        json_string = json.dumps(data)

        return json_string        


class ProxyError(GermanCollectorsException):
    """Proxy Errors

    Errors that occurred while fetching data using proxies.

    :param url: url of the requests that failed using the proxy
    :type url: str

    :param proxies: list of the proxies that failed
    :type proxies: list[Proxy]
    """
    def __init__(self, url, proxies, *args, **kwargs):
        super().__init__(*args, **kwargs)
                
        self.url = url
        self.proxies = proxies        

    def __str__(self):        
        data = {
            "base": json.loads(super().__str__()),
            "ProxyError": {
                "url": str(self.url),
                "proxies": [{
                    "ip": x['proxy']["ip"],
                    "port": x['proxy']["port"]
                } for x in self.proxies]
            }
        }

        json_string = json.dumps(data)

        return json_string        


class ProxyRequestError(ProxyError):
    """ProxyRequest Error

    This error occurrs, when a request with proxy failed because an invalid status_code or something else.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        data = {
            "base": json.loads(super().__str__()),
            "ProxyRequestError": ""
        }

        json_string = json.dumps(data)

        return json_string


class InvalidProxy(ProxyError):
    """InvalidProxy Error

    This error occurrs, when a connection cannot be established with a proxy.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        data = {
            "base": json.loads(super().__str__()),
            "InvalidProxy": ""
        }

        json_string = json.dumps(data)

        return json_string        


class TwitterError(GermanCollectorsException):
    """Twitter Errors

    Errors that occurred while fetching tweets in the Twitter feature.    

    :param status_code: the status code of the exception that was raised
    :type status_code: int
    """
    def __init__(self, status_code, *args, **kwargs):
        super().__init__(*args, **kwargs)        

        self.status_code = status_code

    def __str__(self):
        data = {
            "base": json.loads(super().__str__()),
            "TwitterError": {
                "status_code": str(self.status_code)
            }
        }

        json_string = json.dumps(data)

        return json_string


class ClientLoopError(GermanCollectorsException):
    """ClientLoop Errors

    Errors that occurred when the loop of the discord client failed.    

    :param message: ``message`` contains more specific information about the exception
    :type message: str    
    """
    def __init__(self, message='', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.message = message        

    def __str__(self):
        data = {
            "base": json.loads(super().__str__()),
            "ClientLoopError": {
                "message": self.message
            }
        }

        json_string = json.dumps(data)

        return json_string


class ShopmonitorError(GermanCollectorsException):
    """Shopmonitor Errors

    Errors that occurred inside one of the shopmonitors.

    :param monitor: name of the shopmonitor, that raised the exception
    :type monitor: str
    """
    def __init__(self, monitor, *args, **kwargs):
        super().__init__(*args, **kwargs)  

        self.monitor = monitor      

    def __str__(self):
        data = {
            "base": json.loads(super().__str__()),
            "ShopmonitorError": {
                "monitor": self.monitor
            }
        }

        json_string = json.dumps(data)

        return json_string        

class ShopmonitorLoopError(ShopmonitorError):
    """Shopmonitor Errors

    Errors that occurred inside one of the shopmonitor-loops.

    :param url: url of the site that was fetched
    :type url: str

    :param title: title of the item that was fetched
    :type title: str

    :param link: link of the item that was fetched
    :type link: str
    """
    def __init__(self, url, title, link, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.url = url
        self.title = title
        self.link = link

    def __str__(self):        
        data = {
            "base": json.loads(super().__str__()),
            "ShopmonitorLoopError": {
                "url": self.url,
                "title": self.title,
                "link": self.link
            }
        }

        json_string = json.dumps(data)

        return json_string


class InfoMessage():
    """InfoMessage

    Information, when something other than an exception happened.

    :param message: ``message`` contains more specific information
    :type message: str

    :param when: datetime, when the exception eccirred
    :type when: datetime.datetime
    """
    def __init__(self, message):
        self.message = message
        self.when = getCurrentDatetime()

    def __str__(self):
        data = {
            "base": json.loads(super().__str__()),
            "InfoMessage": {
                "message": self.message,
                "when": self.when.strftime('%Y-%m-%d %H:%M:%S')
            }
        }

        json_string = json.dumps(data)

        return json_string
