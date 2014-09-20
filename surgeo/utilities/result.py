import collections
import inspect
import io
import operator


class Result(object):
    '''Result class containing proxy data.

    Attributes:
        Depends on keyword arguments

    Methods:
        self.absorb(other_proxy_result): returns new proxy_result
        self.as_csv(): returns csv formatted string
        self.as_dict(): returns dict
        self.as_string(): returns long string
        self.attribute_list(): returns list of attribute
        self.errorify(): returns nothing but makes it fail conspicuously
        self.value_list(): returns list of values
        
    '''

    def __init__(self,
                 **kwargs):
        for keyword, value in kwargs.items():
            setattr(self, keyword, value)
        self._error_result = False
        try:
            calling_class = inspect.stack()[1][0].f_locals.get('self', None)
            self._created_by = calling_class.__class__.__name__
        except:
            pass
        
    def absorb(self, other_result):
        '''Get another result's data. If already has that attribute, skip.'''
        members_self = inspect.getmembers(self)
        members_other = inspect.getmembers(other_result)
        for member_other_name, member_other_obj in members_other:
            # if magic method, or priate, skip
            if member_other_name[0] == '_':
                continue
            if not member_other_name in [item[0] for item in members_self]:
                setattr(self, member_other_name, member_other_obj)

    def as_csv(self, tuple_to_list=('all',)):
        '''Provides csv string. Defaults all. Tuple is attributes to list.'''
        members = inspect.getmembers(self)
        csv_string = io.StringIO('')
        for member_name, member_obj in members:
            # If not in tuple_to_list, skip
            if not ('all' in tuple_to_list or member_name in tuple_to_list):
                continue
            # if magic method, skip
            if member_name[0] == '_':
                continue
            if inspect.ismethod(member_obj):
                continue
            csv_string.write('\"')
            csv_string.write(str(member_obj))
            csv_string.write('\",')
        csv_string = csv_string.getvalue()[:-1]
        return csv_string
        
    def as_dict(self):
        '''Returns a dictionary.'''
        zipped_list = zip(self.attribute_list(), self.value_list())
        info_dict = { key : value for (key, value) in zipped_list }
        return info_dict
        
    def as_string(self, tuple_to_list=('all',)):
        '''Provides string. Defaults all attr. Tuple is attributes to list.'''
        members = inspect.getmembers(self)
        string = io.StringIO('')
        for member_name, member_obj in members:
            # If not in tuple_to_list, skip
            if not ('all' in tuple_to_list or member_name in tuple_to_list):
                continue
            # if magic method, skip
            if member_name[0] == '_':
                continue
            # if method, continue
            if not inspect.ismethod(member_obj):
                string.write(str(member_name))
                string.write('=')
                string.write(str(member_obj))
                string.write('\n')
        return string.getvalue()[:-1]
        
    def attribute_list(self):
        '''This returns a list of a ProxyResult's attributes.'''
        attribute_list = []
        members = inspect.getmembers(self)
        for member_name, member_obj in members:
            # if magic method, skip
            if member_name[0] == '_':
                continue
            # if method, skip
            if inspect.ismethod(member_obj):
                continue
            else:
                attribute_list.append(member_name) 
        return attribute_list
        
    def errorify(self):
        '''Make the result a conspicuously fail when listing.'''
        self._error_result = True
        members = inspect.getmembers(self)
        for member_name, member_obj in members:
            # if magic method, skip
            if member_name[0] == '_':
                continue
            # if method, skip
            if inspect.ismethod(member_obj):
                continue
            else:
                setattr(self, member_name, 'error')
                
    def value_list(self):
        '''This returns a list of a ProxyResult's values.'''
        # Order dependent on getmembers
        value_list = []
        members = inspect.getmembers(self)
        for member_name, member_obj in members:
            # if magic method, skip
            if member_name[0] == '_':
                continue
            # if method, skip
            if inspect.ismethod(member_obj):
                continue
            else:
                value_list.append(str(member_obj)) 
        return value_list

