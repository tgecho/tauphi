import sys
import json
import tweepy


def oauth_dance():
    try:
        with open('tauphi_config.json') as handle:
            raw = handle.read().strip()
        config = json.loads(raw)

    except IOError:
        print('Creating new tauphi_config.json')
        config = {}

    except ValueError as e:
        if raw == '':
            print('Creating new tauphi_config.json')
            config = {}
        else:
            print('Error parsing tauphi_config.json: {}'.format(e))
            sys.exit(1)

    if not config.get('max_items'):
        config['max_items'] = raw_input('Max items in feed? ').strip()

    if not config.get('max_days'):
        config['max_days'] = raw_input('Maximum number of days items should be retained? ').strip()

    if not config.get('feed_url'):
        config['feed_url'] = raw_input('Final S3 url? (example: https://s3.amazonaws.com/tauphi/feed.xml)').strip()

    if not config.get('api_key'):
        config['api_key'] = raw_input('API key? ').strip()

    if not config.get('api_secret'):
        config['api_secret'] = raw_input('API secret? ').strip()

    auth = tweepy.OAuthHandler(config['api_key'], config['api_secret'])

    if not config.get('access_token') or not config.get('access_token_secret'):
        try:
            redirect_url = auth.get_authorization_url()
        except tweepy.TweepError as e:
            print('Error! Failed to get request token: {}'.format(e))
            sys.exit(1)

        print('Please authorize this application at {}'.format(redirect_url))
        verifier = raw_input('Verification PIN? ').strip()

        try:
            auth.get_access_token(verifier)
        except tweepy.TweepError as e:
            print('Error! Failed to get access token: {}'.format(e))
            sys.exit(1)

        config['access_token'] = auth.access_token
        config['access_token_secret'] = auth.access_token_secret

    with open('tauphi_config.json', 'w') as handle:
        json.dump(config, handle, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == '__main__':
    oauth_dance()
