import json
from aiohttp import web
import datetime
import DataRequest as dr

routes = web.RouteTableDef()


@routes.get('/api')
async def get_handler(request):
    return web.Response(body=json.dumps({'status': 200, 'message': 'Query API is running'}),
                        status=200, content_type='application/json')


@routes.get('/api/info')
async def get_handler(request):
    print(datetime.datetime.now().strftime('%m-%d %H:%M:%S'), request.remote, request.rel_url)
    data = dr.info()
    return web.Response(body=data[1], status=200, content_type='application/json')


@routes.get('/api/grades')
async def get_handler(request):
    print(datetime.datetime.now().strftime('%m-%d %H:%M:%S'), request.remote, request.rel_url)
    params = request.rel_url.query
    if 'campus' not in params:
        return web.Response(body=json.dumps({'status': 400, 'message': 'campus required'}),
                            status=200, content_type='application/json')
    if 'examName' not in params:
        return web.Response(body=json.dumps({'status': 400, 'message': 'examName required'}),
                            status=200, content_type='application/json')
    if 'studentCode' not in params:
        return web.Response(body=json.dumps({'status': 400, 'message': 'studentCode required'}),
                            status=200, content_type='application/json')

    data = dr.grades(campus=params['campus'], studentCode=params['studentCode'], examName=params['examName'])
    return web.Response(body=data[1], status=200, content_type='application/json')


@routes.get('/api/answercard')
async def get_handler(request):
    print(datetime.datetime.now().strftime('%m-%d %H:%M:%S'), request.remote, request.rel_url)
    params = request.rel_url.query
    if 'campus' not in params:
        return web.Response(body=json.dumps({'status': 400, 'message': 'campus required'}),
                            status=200, content_type='application/json')
    if 'examName' not in params:
        return web.Response(body=json.dumps({'status': 400, 'message': 'examName required'}),
                            status=200, content_type='application/json')
    if 'studentCode' not in params:
        return web.Response(body=json.dumps({'status': 400, 'message': 'studentCode required'}),
                            status=200, content_type='application/json')

    data = dr.answercard(campus=params['campus'], studentCode=params['studentCode'], examName=params['examName'])
    return web.Response(body=data[1], status=200, content_type='application/json')


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host='127.0.0.1', port=3001)
