######################################################################################################################
#	WebTools module unit
#
#	Author: dane22, a Plex Community member
#
# This module is for misc utils
#
# Path of code here shamelessly stolen from Plex scanner bundle
#
######################################################################################################################

import os
import re
import string
import unicodedata
import sys
import json

RE_UNICODE_CONTROL = u'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])' + \
    u'|' + \
    u'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' % \
    (
        unichr(0xd800), unichr(0xdbff), unichr(0xdc00), unichr(0xdfff),
        unichr(0xd800), unichr(0xdbff), unichr(
            0xdc00), unichr(0xdfff),
        unichr(0xd800), unichr(0xdbff), unichr(
            0xdc00), unichr(0xdfff)
    )


class misc(object):
    init_already = False							# Make sure part of init only run once
    # Init of the class

    def __init__(self):
        return

    ''' Below function shamefully stolen from the scanner.bundle, yet modified a bit '''
    # Safely return Unicode.

    def Unicodize(self, s):
        filename = s
        form = 'NFC'
        try:
            filename = unicodedata.normalize(form, unicode(s.decode('utf-8')))
        except:
            try:
                filename = unicodedata.normalize(
                    form, unicode(s.decode(sys.getdefaultencoding())))
            except:
                try:
                    filename = unicodedata.normalize(
                        form, unicode(s.decode(sys.getfilesystemencoding())))
                except:
                    try:
                        filename = unicodedata.normalize(
                            form, unicode(s.decode('ISO-8859-1')))
                    except:
                        try:
                            filename = unicodedata.normalize(form, s)
                        except Exception, e:
                            Log(type(e).__name__ + ' exception precomposing: ' +
                                str(e) + ' with ' + form)
        try:
            filename = re.sub(RE_UNICODE_CONTROL, '', filename)
        except:
            Log.Debug('Couldn\'t strip control characters: ' + filename)
        return filename

    ####################################################################################################
    # This function will return the loopback address
    ####################################################################################################
    def GetLoopBack(self):
        # For now, simply return the IPV4 LB Addy, until PMS is better with this
        return 'http://127.0.0.1:32400'

        ''' Code below not used for now
		try:
			httpResponse = HTTP.Request(
			    'http://[::1]:32400/web', immediate=True, timeout=5)
			return 'http://[::1]:32400'
		except:
			return 'http://127.0.0.1:32400'
		'''

    def getFunction(self, FUNCTIONS, metode, req):
        """ This function will break  up a req, and split it out into function to call, and params for it """
        params = req.request.uri[8:].upper().split('/')
        function = None
        if metode not in FUNCTIONS:
            Log.Critical('Method not found')
            return [function, '']
        for param in params:
            if param in FUNCTIONS[metode]:
                function = param
                break
            else:
                pass
        paramsStr = req.request.uri[req.request.uri.upper().find(
            function) + len(function):]
        # remove starting and ending slash
        if paramsStr.endswith('/'):
            paramsStr = paramsStr[:-1]
        if paramsStr.startswith('/'):
            paramsStr = paramsStr[1:]
        # Turn into a list
        params = paramsStr.split('/')
        # If empty list, turn into None
        if params[0] == '':
            params = None
        Log.Debug('Function to call is: %s with params: %s' %
                  (function, str(params)))
        return [function, params]

    def enum(self, *sequential, **named):
        """
        This will emulate an emun
        Params: 
            enum('users', 'users_self', 'users_all', 'users_self_all')
                Above will create the enum
            enum.users_self_all 
                Above will return 3
            enum.reverse_mapping[3]
                Above will return users_self_all
        """
        enums = dict(zip(sequential, range(len(sequential))), **named)
        reverse = dict((value, key) for key, value in enums.iteritems())
        enums['reverse_mapping'] = reverse
        return type('Enum', (), enums)

    ####################################################################################################
    # This function will return a filtered json, Non case sensitive, based on a url params filter
    ####################################################################################################
    def filterJson(self, origen, filter):
        # Remove start of filter string
        filter = filter[7:]
        # Split into filters
        filterlist = filter.split('&')
        jsonFilter = {}
        for filter in filterlist:
            filterEntry = filter.split('=')
            jsonFilter[filterEntry[0]] = filterEntry[1]
        try:
            # Transform json input to python objects
            input_dict = json.loads(origen)
            jsonOutput = []
            for item in input_dict:
                iFilters = len(jsonFilter) - 1
                for filter in jsonFilter:
                    if jsonFilter[filter].upper() in item[filter].upper():
                        iFilters = iFilters - 1
                if iFilters < 0:
                    jsonOutput.append(item)
        except Exception, e:
            Log.Exception('Exception in Misc.filterJson is: ' + str(e))
            return
        return jsonOutput


misc = misc()
