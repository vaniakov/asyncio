import asyncio
import socket
import sys
import time

TARGETS = ["google.com","youtube.com","facebook.com","amazon.com","yahoo.com","wikipedia.org","reddit.com","twitter.com","ebay.com","linkedin.com","netflix.com","ntd.tv","instagram.com","diply.com","imgur.com","live.com","craigslist.org","bing.com","office.com","tumblr.com","cnn.com","microsoftonline.com","pinterest.com","t.co","chase.com","nytimes.com","livejasmin.com","imdb.com","blogspot.com","paypal.com","pornhub.com","wikia.com","espn.com","twitch.tv","wordpress.com","apple.com","walmart.com","msn.com","salesforce.com","weather.com","bankofamerica.com","breitbart.com","wellsfargo.com","washingtonpost.com","microsoft.com","huffingtonpost.com","zillow.com","stackoverflow.com","dropbox.com","googleusercontent.com"]

async def main(loop, targets):
    result = {}
    for target in targets:
        result[target] = []
        try:
            info = await loop.getaddrinfo(
                target,
                'https',
                proto=socket.IPPROTO_TCP,
            )

            for host in info:
                result[target].append(host[4][0])
                print('{:20}: {}'.format(target, host[4][0]))
        except socket.gaierror:
            print('No such domain name: {}'.format(target))
    return result

event_loop = asyncio.get_event_loop()
try:
    start = time.time()
    result = event_loop.run_until_complete(main(event_loop, TARGETS[:25]))
    print('Resolved {} hosts in {} seconds.'.format(len(TARGETS), time.time() - start))
    addrs = []
    for t in result.values():
        addrs.extend(t)
    print(addrs)
finally:
    event_loop.close()
