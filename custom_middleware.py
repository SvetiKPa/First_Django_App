# from django.utils.deprecation import MiddlewareMixin
#
# class CustomMiddleware(MiddlewareMixin):
#     ...
#
# #------------------------------------------l.1
# class CustomMiddleware(MiddlewareMixin):
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, *args, **kwargs):