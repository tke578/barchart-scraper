import os
import requests
from datetime import datetime, date
from slackclient import SlackClient
from functools import wraps
import time
import logging
from dateutil.parser import parse

logger = logging.getLogger(__name__)

def is_datestring_today(date_string):
    '''Last Trade column gets converted to date string from time string when markets closed ~= 1:30pm i.e. 06:30 ET => 09/15/2020'''
    if not date_string:
        return False
    try:
        return parse(date_string).date() == date.today()
    except:
        return False


def retry(exceptions, tries=4, delay=10, backoff=2, logger=None):
    """
    Retry calling the decorated function using an exponential backoff.

    Args:
        exceptions: The exception to check. may be a tuple of
            exceptions to check.
        tries: Number of times to try (not retry) before giving up.
        delay: Initial delay between retries in seconds.
        backoff: Backoff multiplier (e.g. value of 2 will double the delay
            each retry).
        logger: Logger to use. If None, print.
    """
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    slack_client = Slack()
                    msg = '{}, Retrying in {} seconds...'.format(e, mdelay)
                    slack_client.send_message(str(e), channel={"name": 'scraper-logs'})
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


def log(msg, logger=None):
    if logger:
        logger.warning(msg)
    else:
        print(msg)


class Slack(object):
    ##v.1.3.2##
    def __init__(self, token=os.environ['SLACK_TOKEN']):
        self._client = SlackClient(token)
        # object caching - avoid api rate limiting
        self._channels = []
        self._conversations = []
        self._groups = []
        self._ims = []
        self._users = []

    def filter_channels(self, query):
        ''' Get the channels matching the given filter.
            Parameters: dict(query)
            Returns: list(Channel(channel)) OR []
        '''
        return list(filter(lambda channel: match_dict(channel, query), self.get_channels()))

    def filter_conversations(self, query):
        ''' Get the conversations matching the given filter.
            Parameters: dict(query)
            Returns: list(Conversation(conversation)) OR []
        '''
        return list(filter(lambda conversation: match_dict(conversation, query), self.get_conversations()))

    def filter_groups(self, query):
        ''' Get the groups matching the given filter.
            Parameters: dict(query)
            Returns: list(Group(group)) OR []
        '''
        return list(filter(lambda group: match_dict(group, query), self.get_groups()))

    def filter_ims(self, query):
        ''' Get the ims matching the given filter.
            Parameters: dict(query)
            Returns: list(IM(im)) OR []
        '''
        return list(filter(lambda im: match_dict(im, query), self.get_ims()))

    def filter_users(self, query):
        ''' Get the users matching the given filter.
            Parameters: dict(query)
            Returns: list(User(user)) OR []
        '''
        return list(filter(lambda user: match_dict(user, query), self.get_users()))

    def get_channel(self, query):
        ''' Get the channel matching the given filter.
            Parameters: dict(query)
            Notes: If more than one channel is found, None is returned.
            Returns: Channel(channel) OR None
        '''
        results = self.filter_channels(query)
        return None if len(results) != 1 else results[0]

    def get_channels(self):
        ''' Get a list of all channels if that information has not already been retrieved.
            Notes: Updates self._channels.
            Returns: list(Channel(channel)) OR []
        '''
        if self._channels: return self._channels
        else:
            result = self._client.api_call('channels.list')
            if result['ok']: self._channels = result['channels']
            return self._channels

    def get_conversation(self, query):
        ''' Get the conversation matching the given filter.
            Parameters: dict(query)
            Notes: If more than one conversation is found, None is returned.
            Returns: Conversation(conversation) OR None
        '''
        results = self.filter_conversations(query)
        return None if len(results) != 1 else results[0]

    def get_conversations(self):
        ''' Get a list of all conversations if that information has not already been retrieved.
            Notes: Updates self._conversations.
            Returns: list(Conversation(conversation)) OR []
        '''
        if self._conversations: return self._conversations
        else:
            result = self._client.api_call('conversations.list')
            if result['ok']: self._conversations = result['channels']
            return self._conversations

    def get_group(self, query):
        ''' Get the group matching the given filter.
            Parameters: dict(query)
            Notes: If more than one group is found, None is returned.
            Returns: Group(group) OR None
        '''
        results = self.filter_groups(query)
        return None if len(results) != 1 else results[0]

    def get_groups(self):
        ''' Get a list of all groups if that information has not already been retrieved.
            Notes: Updates self._groups.
            Returns: list(Group(group)) OR []
        '''
        if self._groups: return self._groups
        else:
            result = self._client.api_call('groups.list')
            if result['ok']: self._groups = result['groups']
            return self._groups

    def get_im(self, query):
        ''' Get the im matching the given filter.
            Parameters: dict(query)
            Notes: If more than one im is found, None is returned.
            Returns: IM(im) OR None
        '''
        results = self.filter_ims(query)
        return None if len(results) != 1 else results[0]

    def get_ims(self):
        ''' Get a list of all ims if that information has not already been retrieved.
            Notes: Updates self._ims.
            Returns: list(IM(im)) OR []
        '''
        if self._ims: return self._ims
        else:
            result = self._client.api_call('im.list')
            if result['ok']: self._ims = result['ims']
            return self._ims

    def get_message_link(self, channel='', thread_id='', thread_item_id=''):
        ''' Get the link for the given message.
            Parameters:
            - str(channel), str(thread_id)
            - Optional: str(thread_item_id)
            Notes: Parameters are kwargs to enable lazy rendering using "send_message" outputs.
            Returns: str(link)
        '''
        if not thread_item_id: return 'https://synapsepay.slack.com/archives/{channel_id}/p{thread_id}'.format(channel_id=channel, thread_id=thread_id.replace('.', ''))
        else: return 'https://synapsepay.slack.com/archives/{channel_id}/p{thread_id}?thread_ts={thread_ts}&cid={channel_id}'.format(channel_id=channel, thread_id=thread_item_id.replace('.', ''), thread_ts=thread_id)

    def get_user(self, query):
        ''' Get the user matching the given filter.
            Parameters: dict(query)
            Notes: If more than one user is found, None is returned.
            Returns: User(user) OR None
        '''
        results = self.filter_users(query)
        return None if len(results) != 1 else results[0]

    def get_users(self):
        ''' Get a list of all users if that information has not already been retrieved.
            Notes: Updates self._users.
            Returns: list(User(user)) OR []
        '''
        if self._users: return self._users
        else:
            result = self._client.api_call('users.list')
            if result['ok']: self._users = result['members']
            return self._users

    def send_message(self, content, channel={}, channels=[], user={}, users=[], as_me=False, thread='', **kwargs):
        ''' Send a message to the given set of channels.
            Parameters:
            - str(content)
            - Optional: dict(channel) or list(dict(channel))
            - Optional: dict(user) or list(dict(user))
            - Optional: bool(as_me), str(thread_id)
            Notes:
            - as_me: Send message as the user who owns the Slack token being used.
            - result:
              {
                  channel: str(channel_id),
                  thread: str(thread_id),
                  url: str(message_url),
                  success: bool(success)
              }
            - Results are returned in a consistent order: [channel, *channels, user, *users].
            Returns:
            - channel or user: dict(result) or None
            - (channel and user) or channels or users: list(dict(result))
        '''
        channel_ids = []
        for channel in filter(lambda query: query, [channel, *channels]):
            result = self.get_channel(channel)
            if result: channel_ids.append(result['id'])
            else: channel_ids.append(None)

        im_ids = []
        for user in filter(lambda query: query, [user, *users]):
            user = self.get_user(user)
            if not user: im_ids.append(None); continue

            result = self.get_im({'user': user['id']})
            if result: im_ids.append(result['id'])
            else: im_ids.append(None)

        results = []
        for id in [*channel_ids, *im_ids]:
            try:
                if not id: results.append({'success': False}); continue
                result = self._client.api_call('chat.%sMessage' % ('me' if (as_me and not thread) else 'post'), channel=id, text=content, thread_ts=thread, **kwargs)
                thread_ts = result['message']['ts']
                results.append(
                {
                    'channel': result['channel'],
                    'thread': thread or thread_ts,
                    'url': self.get_message_link(channel=result['channel'], thread_id=thread or thread_ts, thread_item_id='' if not thread else thread_ts),
                    'success': True
                })
            except: results.append({'success': False})

        if len(results) > 1: return results
        else: return None if not results[0]['success'] else results[0]

    def send_private_message(self, content, channel={}, channels=[], user=None, users=[], **kwargs):
        ''' Send a message to the given set of channels.
            Parameters: str(content), dict(channel) or list(dict(channel)), dict(user) or list(dict(user))
            Notes:
            - Threads are not an option available through the Slack platform for private messages.
            Returns: bool(success)
        '''
        channel_ids = []
        for channel in (channels or [channel]):
            result = self.get_channel(channel)
            if result: channel_ids.append(result['id'])

        user_ids = []
        for user in (users or [user]):
            result = self.get_user(user)
            if result: user_ids.append(result['id'])

        return all(
        [
            all(
            [
                self._client.api_call('chat.postEphemeral', channel=channel_id, user=user_id, text=content, **kwargs)['ok']
                for channel_id in channel_ids
            ])
            for user_id in user_ids
        ])

    def upload_file(self, file, file_name='', file_type='', message='', title='', channel={}, channels=[], user={}, users=[], thread='', **kwargs):
        ''' Upload the given file to Slack.
            Parameters:
            - bytes(file_content) or str(file_path)
            - Optional: str(file_name), str(file_type)
            - Optional: str(post_message), str(post_title)
            - Optional: dict(channel) or list(dict(channel))
            - Optional: dict(user) or list(dict(user))
            - Optional: bool(as_me), str(thread_id)
            Notes:
            - as_me: Send message as the user who owns the Slack token being used.
            - file: If you want to upload string content, it must be encoded as binary data (ie. utf-8).
            - file_name: Can be derived from "file" if the supplied value is a string, will be overridden if explicitly supplied.
            - file_type: Will be auto populated with file extension if file name is supplied, default value is "auto".
            - result:
              {
                  channel: str(channel_id),
                  file:
                  {
                      pretty: str(formatted_file_url),
                      raw: str(raw_file_url)
                  },
                  thread: str(thread_id),
                  success: bool(success)
              }
            - Results are returned in a consistent order: [channel, *channels, user, *users].
            Returns:
            - channel or user: dict(result) or None
            - (channel and user) or channels or users: list(dict(result))
        '''
        content = b'' if type(file) is str else file
        extension = '' if content or ('.' not in file) else file.split('.')[-1]

        file_name = file_name or (uuid.uuid4().hex if not type(file) is str else os.path.basename(file))
        file_type = file_type or extension or 'auto'

        channel_ids = []
        for channel in filter(lambda query: query, [channel, *channels]):
            result = self.get_channel(channel)
            if result: channel_ids.append(result['id'])
            else: channel_ids.append(None)

        im_ids = []
        for user in filter(lambda query: query, [user, *users]):
            user = self.get_user(user)
            if not user: im_ids.append(None); continue

            result = self.get_im({'user': user['id']})
            if result: im_ids.append(result['id'])
            else: im_ids.append(None)

        results = []
        try:
            result = self._client.api_call('files.upload', **
            {
                'channels': [*channel_ids, *im_ids],
                'content': content,
                'file': '' if content else open(file, 'r' if extension in str_file_types else 'rb'),
                'filename': file_name,
                'filetype': file_type,
                'initial_comment': message,
                'thread_ts': thread,
                'title': title,
                **kwargs
            })
            for id in [*channel_ids, *im_ids]:
                thread_ts = result['file']['shares']['public' if id in channel_ids else 'private'][id][0]['ts']
                results.append(
                {
                    'channel': id,
                    'file':
                    {
                        'download': result['file']['url_private_download'],
                        'pretty': result['file']['permalink'],
                        'raw': result['file']['url_private']
                    },
                    'thread': thread or result['file']['shares']['public' if id in channel_ids else 'private'][id][0]['ts'],
                    'url': self.get_message_link(channel=id, thread_id=thread or thread_ts, thread_item_id='' if not thread else thread_ts),
                    'success': True
                })
        except:
            for id in [*channel_ids, *im_ids]: results.append({'success': False})

        if len(results) > 1: return results
        else: return None if not results[0]['success'] else results[0]

        
def match_dict(object, filter_dict):
    ''' Abstract filter_object method for retrieving items.
        Parameters: dict(object), dict(filter_dict)
        Returns: bool(match)
    '''
    def compare_dict(object, filter_dict):
        for key in filter_dict.keys():
            if not all(
            [
                object.get(key),
                type(filter_dict[key]) is type(object[key])
            ]): return False
            elif type(object[key]) is dict:
                if not compare_dict(object[key], filter_dict[key]): return False
            elif type(object[key]) is list:
                if not compare_list(object[key], filter_dict[key]): return False
            elif not (object[key] == filter_dict[key]): return False
        return True
    
    def compare_list(object, filter_dict):
        if not len(filter_dict) <= len(object): return False
        for index in range(0, len(filter_dict)):
            if not (type(object[index]) is type(filter_dict[index])): return False
            elif type(object[index]) is dict:
                if not compare_dict(object, filter_dict): return False
            elif type(object[index]) is list:
                if not compare_list(object, filter_dict): return False
            elif not (filter_dict[index] in object): return False
        return True
    
    return False if not compare_dict(object, filter_dict) else True
