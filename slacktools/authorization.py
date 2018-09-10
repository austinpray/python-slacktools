import hmac
from hashlib import sha256

from time import time


class SignatureVersionException(ValueError):
    pass


def verify_signature(slack_signing_secret: str,
                     timestamp: int,
                     body: str,
                     slack_signature: str):
    """
    Verifies a signature from X-Slack-Signature and X-Slack-Request-Timestamp

    see: https://api.slack.com/docs/verifying-requests-from-slack

    also see the implementation in: `slackapi/python-slack-events-api <https://github.com/slackapi/python-slack-events-api>`_.
    Check out `SlackServer.verify_signature`. History:
    `2018-09-09 <https://github.com/slackapi/python-slack-events-api/blob/6a269ed11fc46d7b14edd1fc11caf655922bf1a6/slackeventsapi/server.py#L47-L83>`_

    :raises: SignatureVersionException if the signature version is something other than v0
    """

    if not slack_signing_secret:
        raise ValueError('slack_signing_secret not provided')
    if not timestamp or not isinstance(timestamp, int):
        raise ValueError('timestamp is not good int')
    if not body:
        raise ValueError('body not provided')
    if not slack_signature:
        raise ValueError('signature not provided')
    if not slack_signature.startswith('v0'):
        raise SignatureVersionException(
            "expected the signature to be version 'v0' but got '{}'".format(slack_signature[:2]))

    if abs(time() - timestamp) > 60 * 5:
        # The request timestamp is more than five minutes from local time.
        # It could be a replay attack, so let's ignore it.
        return False

    sig_basestring = "v0:{}:{}".format(timestamp, body)

    my_signature = 'v0=' + hmac.new(
        slack_signing_secret.encode(),
        sig_basestring.encode(),
        sha256
    ).hexdigest()

    return hmac.compare_digest(my_signature, slack_signature)
