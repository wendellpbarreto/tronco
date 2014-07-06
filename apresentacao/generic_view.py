#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging 
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.template.loader import render_to_string
from django.views.generic import View

logger = logging.getLogger(__name__)

class GenericView(View):
    '''
    Generic view to render all system requests
    '''
    def render_to_json(self, request, template, context_data):
        '''
        Dumps json objects to string template
        '''
        response = {}   

        try: 
            return context_data['file'] 
        except:
            pass
        
        try:
            template_data = context_data['template']
        except Exception, e:
            template_data = None

        try:
            leftover_data = context_data['leftover']
        except:
            leftover_data = None

        try:
            response['template'] = render_to_string(template, template_data, context_instance=RequestContext(request))
        except Exception, e:
            pass
                    
        try:
            for key, value in leftover_data.items():    
                if key == 'redirect' and value == 'none':
                    response['template'] = None
                else:
                    response[key] = value
        except Exception, e:
            pass
            
        try:
            return HttpResponse(json.dumps(response), mimetype='application/json')
        except Exception, e:
            logger.error(str(e))

            return None

    def load_json(self, request):
        '''
        Load json objects from request
        '''
        try:
            response = json.loads(request)
        except:
            response = None

        return response

    def _request(self, request, *args, **kwargs):

        if request.is_ajax():

            return self.render_to_json(request, self.get_template_name(request), self.get_context_data(request))
        else:
            context_data = self.get_context_data(request)

            try:
                return context_data['file']
            except:
                pass

            try:
                template_data = context_data['template']
            except Exception, e:
                template_data = None                        

            try:
                leftover_data = context_data['leftover']
            except:
                leftover_data = None

            try:
                for key, value in leftover_data.items():    
                    if key == 'redirect':
                        return HttpResponseRedirect(value)
            except Exception, e:
                pass

            return render_to_response(self.get_template_name(request), template_data, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):

        return self._request(request, args, kwargs)
        
    def get(self, request, *args, **kwargs):

        return self._request(request, args, kwargs)

    def get_context_data(self, request):
        data = {}
        page_name = request.resolver_match.url_name
        app_name = request.resolver_match.app_name
        
        try:
            slug = str(self.kwargs['slug'])
        except Exception, e:
            logger.error('Kwargs[slug] isn\'t defined! Raised: ' + str(e))
        else:   
            slug_method = getattr(self, slug)
            data = slug_method(request)

            try:
                data['template']['page_name'] = page_name
                data['template']['app_name'] = app_name
                data['template']['slug'] = slug
            except Exception, e:
                logger.info(str(e))
        finally:
            return data

    def get_template_name(self, request):
        page_name = request.resolver_match.url_name
        app_name = request.resolver_match.app_name

        if not page_name:
            page_name = ''  
            page_name_slashed = ''
        else:
            page_name_slashed = page_name + '/'

        if not app_name:
            app_name = ''
            app_name_slashed = ''
        else:
            app_name_slashed = app_name + '/'


        paths = []

        try:
            slug = str(self.kwargs['slug'])
        except Exception, e:
            logger.error('Kwargs[slug] aren\'t defined! Raised: ' + str(e))

            return app_name + '/404.html'
        else:
            if request.is_ajax(): 
                paths.append(app_name_slashed + page_name_slashed + 'ajax/' + slug + '.html')
                paths.append(app_name_slashed + 'ajax/' + page_name + '.html')
                paths.append(app_name_slashed + 'ajax/' + slug + '.html')
            else:
                paths.append(app_name_slashed + page_name_slashed + slug + '.html')
                paths.append(app_name_slashed + page_name + '.html')
                paths.append(app_name_slashed + slug + '.html')
                

            for path in paths:
                print path
                try:
                    template = loader.get_template(path)                
                except Exception, e:
                    logger.error('Template not found! Raised: ' + str(e))
                else:
                    logger.info('Template loaded: ' + str(path))

                    return path
                
            logger.info('Not found available templates, loading 404 template!')

            return '404.html'
 
    def paginate(obj, page, num_per_page):
        paginator = Paginator(obj, num_per_page)

        try:
            page = int(page)
            obj = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            obj = paginator.page(page)
        except EmptyPage:
            page = paginator.num_pages
            obj = paginator.page(page)
        except:
            page = 1
            obj = paginator.page(page)

        try:
            paginator.page(page - 10)
            paginator.page(page - 11)

            obj.has_less_ten = page - 10                    
        except EmptyPage:
            pass

        try:
            paginator.page(page - 2)
            obj.has_less_two = page - 2
        except EmptyPage:
            pass

        try:
            paginator.page(page - 3)
            obj.has_less_three = page - 3
        except EmptyPage:
            pass

        obj.page = page

        try:
            paginator.page(page + 2)
            obj.has_more_two = page + 2
        except EmptyPage:
            pass

        try:
            paginator.page(page + 3)
            obj.has_more_three = page + 3
        except EmptyPage:
            pass
        
        try:
            paginator.page(page + 10)
            paginator.page(page + 11)

            obj.has_more_ten = page + 10                    
        except EmptyPage:
            pass

        return obj