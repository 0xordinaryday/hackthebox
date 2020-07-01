# Nibbles

The first challenge with the Nibbles box is to log into the Nibbleblog web application. Trying a few of the obvious passwords, such as 'admin', 'password', 'qwerty', '12345678', etc., didn't work.

As a beginner, it's great to practise using many of the different tools at your disposal but, unfortunately, I ran into some problems when trying Burp Suite and Hydra. The main issue was that Nibbleblog blacklists an IP address for several minutes after 5 unsuccessful login attempts. It seemed like a good opportunity to try and write a program customised specifically for this attack.

## [bfg9000](bfg9000.py)

This program was written to work around the IP blacklisting. Using curl it was possible to test the theory that Nibbleblog might check the blacklist based on an IP address supplied in the `X-FORWARDED-FOR` HTTP header. This turned out to be the case. It was therefore possible to run an uninterrupted brute-force attack by changing the IP address in the `X-FORWARDED-FOR` header after every fifth attempt.

## Unsuccessful attempts

### Burp Suite

Using the Intruder tool in Burp Suite makes it quite simple to try and brute-force a login via HTTP request. Unfortunately my Kali Virtual Machine is a little underpowered and Burp Suite choked when trying to load a password list of a decent size.

I suspect it might be possible to randomise the `X-FORWARDED-FOR` header in Burp Suite but have not looked into that yet.

### Hydra

Password brute-forcing via HTTP requests can also be accomplished with hydra. The problem in this case was that Nibbleblog was blacklisting my IP address after five unsuccessful login attempts, making the brute-force process painfully slow.
