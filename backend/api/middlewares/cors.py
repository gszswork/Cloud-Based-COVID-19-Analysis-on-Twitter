# coding: utf-8
"""
@Author: Guangzheng Hu
Student ID: 692277

Description: This files including the views that used to control CORS problem
"""
from django.utils.deprecation import MiddlewareMixin


class CrosMeddleware(MiddlewareMixin):

    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET,OPTIONS,POST'
        response['Access-Control-Allow-Headers'] = '*'
        response['Access-Control-Max-Age'] = 3628800
        return response
