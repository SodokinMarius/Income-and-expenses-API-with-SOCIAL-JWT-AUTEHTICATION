from rest_framework import renderers

import json
class  UserRenderer(renderers.JSONRenderer):
    charset='utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response=''
        if 'ErrorDetail' in str(data): #<--- S'il ya d'erreur dans la réponse renvoyée
            response=json.dumps({'errors':data})
        else:
            response=json.dumps({'data':data})
        return response
            