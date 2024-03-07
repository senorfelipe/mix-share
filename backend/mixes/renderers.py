from rest_framework import renderers

class AudioMPEGRenderer(renderers.BaseRenderer):
    media_type = 'audio/mpeg'
    format = 'audio'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data