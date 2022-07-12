class Route:
    class V1:
        API = 'api'
        VERSION = 'v1'
        prefix_api = '' #'/' + API + '/' + VERSION

        #         Auth
        LOGIN = '/login'
        REGISTER = '/register'
        LOGOUT = '/logout'
        REFRESH_TOKEN= '/refresh-token'

        #        Station
        GETSTATION = '/get-station'