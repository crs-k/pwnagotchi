import gettext
import os


class Voice:
    def __init__(self, lang):
        localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
        translation = gettext.translation(
            'voice', localedir,
            languages=[lang],
            fallback=True,
        )
        translation.install()
        self._ = translation.gettext

    def custom(self, s):
        return s

    def default(self):
        return self._('Sleeping.')

    def on_starting(self):
        return self._('Pwnagotchi! Starting...')

    def on_ai_ready(self):
        return self._('AI ready.')

    def on_keys_generation(self):
        return self._('Generating keys, do not turn off.')

    def on_normal(self):
        return self._('Feeling normal.')

    def on_free_channel(self, channel):
        return self._('Hey, channel {channel} is free! Your AP will say thanks.').format(channel=channel)

    def on_reading_logs(self, lines_so_far=0):
        if lines_so_far == 0:
            return self._('Reading last session logs.')
        else:
            return self._('Read {lines_so_far} log lines so far.').format(lines_so_far=lines_so_far)

    def on_bored(self):
        return self._('I\'m bored.')

    def on_motivated(self, reward):
        return self._('Feeling motivated!')

    def on_demotivated(self, reward):
        return self._('Feeling demotivated.')

    def on_sad(self):
        return self._('I\'m sad.')

    def on_angry(self):
        return self._('Feeling angry!')

    def on_excited(self):
        return self._('Feeling excited!')

    def on_new_peer(self, peer):
        if peer.first_encounter():
            return self._('Hello {name}! Nice to meet you.').format(name=peer.name())
        else:
            return self._('Unit {name} is nearby!').format(name=peer.name())

    def on_lost_peer(self, peer):
        return self._('{name} is gone.').format(name=peer.name())

    def on_miss(self, who):
        return self._('{name} missed!').format(name=who)

    def on_grateful(self):
        return self._('Feeling grateful.')

    def on_lonely(self):
        return self._('Feeling lonely.')

    def on_napping(self, secs):
        return self._('Napping for ({secs}s)').format(secs=secs)

    def on_shutdown(self):
        return self._('Shutting down.')

    def on_awakening(self):
        return self._('Waking up.')

    def on_waiting(self, secs):
        return self._('Waiting for ({secs}s)').format(secs=secs)

    def on_assoc(self, ap):
        ssid, bssid = ap['hostname'], ap['mac']
        what = ssid if ssid != '' and ssid != '<hidden>' else bssid
        return self._('Associating to {what}').format(what=what)

    def on_deauth(self, sta):
        return self._('Deauthenticating {mac}').format(mac=sta['mac'])

    def on_handshakes(self, new_shakes):
        s = 's' if new_shakes > 1 else ''
        return self._('Ate {num} new handshake{plural}!').format(num=new_shakes, plural=s)

    def on_unread_messages(self, count, total):
        s = 's' if count > 1 else ''
        return self._('You have {count} new message{plural}!').format(count=count, plural=s)

    def on_rebooting(self):
        return self._("Something went wrong ... Rebooting.")

    def on_uploading(self, to):
        return self._("Uploading data to {to}.").format(to=to)

    def on_downloading(self, name):
        return self._("Downloading from {name}.").format(name=name)

    def on_last_session_data(self, last_session):
        status = self._('Kicked {num} stations\n').format(num=last_session.deauthed)
        if last_session.associated > 999:
            status += self._('Made >999 new friends\n')
        else:
            status += self._('Made {num} new friends\n').format(num=last_session.associated)
        status += self._('Got {num} handshakes\n').format(num=last_session.handshakes)
        if last_session.peers == 1:
            status += self._('Met 1 peer')
        elif last_session.peers > 0:
            status += self._('Met {num} peers').format(num=last_session.peers)
        return status

    def on_last_session_tweet(self, last_session):
        return self._(
            'I\'ve been running for {duration} and deauthed {deauthed} clients! I\'ve also met {associated} new friends and ate {handshakes} handshakes.').format(
            duration=last_session.duration_human,
            deauthed=last_session.deauthed,
            associated=last_session.associated,
            handshakes=last_session.handshakes)

    def hhmmss(self, count, fmt):
        if count > 1:
            # plural
            if fmt == "h":
                return self._("hours")
            if fmt == "m":
                return self._("minutes")
            if fmt == "s":
                return self._("seconds")
        else:
            # sing
            if fmt == "h":
                return self._("hour")
            if fmt == "m":
                return self._("minute")
            if fmt == "s":
                return self._("second")
        return fmt
