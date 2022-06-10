#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sanic import Sanic, Blueprint, json
from sanic.exceptions import NotFound, MethodNotSupported, SanicException



API_STATUS = 'STATUS'
API_MESSAGE = 'MESSAGE'


app = Sanic(name='sanicbehindapache')
app.config.OAS = False


@app.exception(NotFound)
async def error_404(request, exception):
    """
    Error 404 -> The server can not find the requested resource.
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404
    :param request:
    :param exception:
    :return:
    """
    retvalue = dict()
    retvalue[API_STATUS] = False
    retvalue[API_MESSAGE] = 'Error NotFound: %s -> %s' % (request.url, exception)
    return json(retvalue, status=404)


@app.exception(MethodNotSupported)
async def error_405(request, exception):
    """
    Error 405 -> The request method is known by the server but is not supported by the target resource.
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/405
    :param request:
    :param exception:
    :return:
    """
    retvalue = dict()
    retvalue[API_STATUS] = False
    retvalue[API_MESSAGE] = 'Error NotFound: %s -> %s' % (request.url, exception)
    return json(retvalue, status=405)


@app.exception(SanicException)
async def error_from_api(request, exception):
    """
    Create an error and return it.
    :param request:
    :param exception:
    :return:
    """
    retvalue = dict()
    retvalue[API_STATUS] = False
    retvalue[API_MESSAGE] = 'Error: %s' % exception
    return json(retvalue)


bp_part_one = Blueprint(name='one', url_prefix='/one')


@bp_part_one.route('/status')
async def one_status(request):
    """
    Get the status of part one.
    """
    try:
        retvalue = dict()
        retvalue[API_STATUS] = True
        retvalue[API_MESSAGE] = request.url
        return json(retvalue, status=200)
    except Exception as e:
        raise SanicException('Error during getting the status! -> %s' % e, status_code=500)


@bp_part_one.route('/echo', methods=['POST'])
async def one_echo(request):
    """
    Echo the post data from the request.
    curl -d '{"key1":"value1", "key2":"value2"}' -H "Content-Type: application/json" -X POST http://localhost:61210/api/one/echo
    """
    try:
        if request.json is None:
            raise SanicException('Request is empty!', status_code=500)
        else:
            retvalue = dict()
            retvalue[API_STATUS] = True
            retvalue[API_MESSAGE] = request.json
            return json(retvalue, status=200)
    except Exception as e:
        raise SanicException('There is an error during getting the JSON data: %s' % e, status_code=500)


@bp_part_one.route('/change/<nr:int>', methods=['PUT'])
async def one_change(request, nr: int):
    """
    Echo the put data from the request.
    curl -X PUT http://localhost:61210/api/one/change/11
    """
    try:
        if nr is None:
            raise SanicException('Request is empty!', status_code=500)
        else:
            retvalue = dict()
            retvalue[API_STATUS] = True
            retvalue[API_MESSAGE] = nr
            return json(retvalue, status=200)
    except Exception as e:
        raise SanicException('There is an error during getting the number: %s' % e, status_code=500)


@bp_part_one.route('/remove/<nr:int>', methods=['DELETE'])
async def one_delete(request, nr: int):
    """
    Echo the delete data from the request.
    curl -X DELETE http://localhost:61210/api/one/remove/22
    """
    try:
        if nr is None:
            raise SanicException('Request is empty!', status_code=500)
        else:
            retvalue = dict()
            retvalue[API_STATUS] = True
            retvalue[API_MESSAGE] = nr
            return json(retvalue, status=200)
    except Exception as e:
        raise SanicException('There is an error during getting the number: %s' % e, status_code=500)


bp_part_two = Blueprint(name='two', url_prefix='/two')


@bp_part_two.route('/status')
async def two_status(request):
    """
    Get the status of part two.
    """
    try:
        retvalue = dict()
        retvalue[API_STATUS] = True
        retvalue[API_MESSAGE] = request.url
        return json(retvalue, status=200)
    except Exception as e:
        raise SanicException('Error during getting the status! -> %s' % e, status_code=500)


api = Blueprint.group(bp_part_one, bp_part_two, url_prefix='/api')
app.blueprint(api)


def main():
    # Run the Sanic application
    app.run(host='localhost', port=61210, access_log=False, debug=False)


if __name__ == "__main__":
    main()
