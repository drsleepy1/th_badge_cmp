#!/usr/bin/env python3

import requests
import sys
from bs4 import BeautifulSoup as bs

def get_status_page(username):
    # get a list with the lines of the user page
    url = "http://telehack.com/u/" + username
    r = requests.get(url)
    if r.status_code != 200:
        return ([username], r.status_code)
    soup = bs(r.text, features="lxml")
    pre = soup.pre
    pretext = str(pre)
    page_lines = [line.strip() for line in pretext.split("<br/>")]
    return (page_lines, 0)

def get_badges(page):
    badges = []
    badges_start = page.index("user status bits:")+1
    badges_end = page.index("")
    for badge in page[badges_start:]:
        badge = badge.split(" ")[0]
        if badge:
            badges.append(badge)
        else:
            return badges

def main(args):
    user1 = args[1].upper()
    user2 = args[2].upper()

    user1_page, err = get_status_page(user1)
    if err == 404:
        print(f"{err}: user {user1} not found.")
        sys.exit(err)
    elif err:
        print(f"{user1}: {err}")
        sys.exit(err)

    user2_page, err = get_status_page(user2)
    if err == 404:
        print(f"{err}: user {user2} not found.")
        sys.exit(err)
    elif err:
        print(f"{user2}: {err}")
        sys.exit(err)

    user1_badges = get_badges(user1_page)
    user2_badges = get_badges(user2_page)

    # badge count for each user
    hdr_message = f"{user1} ({len(user1_badges)}) vs {user2} ({len(user2_badges)})"
    print("\n" + hdr_message)
    print("-" * len(hdr_message))

    # badges users have in common
    common_badges = list(set(user1_badges) & set(user2_badges))
    print(f"\n[+] Both users have this {len(common_badges)} badges:\n")
    print(", ".join(sorted(common_badges)))

    # badges only user2 have
    badges1 = sorted(list(set(user2_badges) - set(user1_badges)))
    print(f"\n[+] {user1} is missing this {len(badges1)} badges that {user2} already have:\n")

    if badges1:
        print(", ".join(badges1))
    else:
        print("None.")

    # badges only user1 have
    badges2 = sorted(list(set(user1_badges) - set(user2_badges)))
    print(f"\n[+] {user2} is missing this {len(badges2)} badges that {user1} already have:\n")
    
    if badges2:
        print(", ".join(badges2))
    else:
        print("None.")
    
    print("")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"  Usage: {sys.argv[0]} <user1> <user2>\n")
        sys.exit(1)
    main(sys.argv)
