#!/usr/bin/env python3

import requests
import argparse
import socket
import asyncio

requests.packages.urllib3.disable_warnings()


async def main(domain, masscanOutput, urlOutput):
    domainsFound = {}
    domainsNotFound = {}
    if (not masscanOutput and not urlOutput):
        print("[+]: Downloading domain list from crt.sh...")
    response = collectResponse(domain)
    if (not masscanOutput and not urlOutput):
        print("[+]: Download of domain list complete.")
    domains = collectDomains(response)
    if (not masscanOutput and not urlOutput):
        print(f"[+]: Parsed {len(domains)} domain(s) from list.")
    if len(domains) == 0:
        exit(1)
    tasks = [resolve(domain) for domain in domains]   
    results = await asyncio.gather(*tasks)
    for result in results:
        if (result):
            for ip in result.values():
                if ip != 'none':
                    domainsFound.update(result)
                else:
                    domainsNotFound.update(result)
    if (urlOutput):
        printUrls(sorted(domains))
    if (masscanOutput):
        printMasscan(domainsFound)
    if (not masscanOutput and not urlOutput):
        print("\n[+]: Domains found:")
        printDomains(domainsFound)
        print("\n[+]: Domains with no DNS record:")
        printDomains(domainsNotFound)


async def resolve(domain):
    try:
        return({domain: socket.gethostbyname(domain)})
        await asyncio.sleep(2)
    except:
        return({domain: "none"})


def printDomains(domains):
    for domain in sorted(domains):
        print(f"{domains[domain]}\t{domain}")


def printMasscan(domains):
    iplist = set()
    for domain in domains:
        iplist.add(domains[domain])
    for ip in sorted(iplist):
        print(f"{ip}")


def printUrls(domains):
    for domain in domains:
        print(f"https://{domain}")


def collectResponse(domain):
    url = 'https://crt.sh/?q=' + domain + '&output=json'
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    try:
        response = requests.get(url, verify=False, headers={'user-agent':ua})
    except:
        print("[!]: Connection to server failed.")
        exit(1)
    try:
        domains = response.json()
        return domains
    except:
        print("[!]: The server did not respond with valid json.")
        exit(1)


def collectDomains(response):
    domains = set()
    for domain in response:
        domains.add(domain['common_name'])
        if '\n' in domain['name_value']:
            domlist = domain['name_value'].split()
            for dom in domlist:
                domains.add(dom)
        else:
            domains.add(domain['name_value'])
    return domains


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", type=str, required=True,
                        help="domain to query for CT logs, e.g.: domain.com")
    parser.add_argument("-u", "--urls", default=0, action="store_true",
                        help="ouput results with https:// urls for \
                        domains that resolve, one per line.")
    parser.add_argument("-m", "--masscan", default=0, action="store_true",
                        help="output resolved IP address, one per line. \
                        Useful for masscan IP list import \"-iL\" format.")
    args = parser.parse_args()
    asyncio.run(main(args.domain, args.masscan, args.urls))
