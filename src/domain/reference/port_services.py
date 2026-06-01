"""Reference data about network ports.

This is domain reference knowledge (stable subject-matter information), not
deployment configuration, so it lives in domain/reference rather than in config.

Two distinct tables with different purposes:
- ``PORT_DESCRIPTIONS`` are full descriptions for the Port information tool.
- ``KNOWN_SERVICES`` are short labels for port-scanner result rows.
"""
from __future__ import annotations

from types import MappingProxyType
from typing import Mapping

__all__ = ["PORT_DESCRIPTIONS", "KNOWN_SERVICES", "describe_port", "service_label"]

PORT_DESCRIPTIONS: Mapping[int, str] = MappingProxyType({
    22: "SSH (Secure Shell) - remote access to systems",
    23: "Telnet - protocol for remote system management",
    25: "SMTP (Simple Mail Transfer Protocol) - email protocol",
    53: "DNS (Domain Name System) - domain name system",
    80: "HTTP (Hypertext Transfer Protocol) - the main data-transfer protocol on the internet",
    443: "HTTPS (HTTP Secure) - the secure version of HTTP",
    110: "POP3 (Post Office Protocol version 3) - email protocol",
    143: "IMAP (Internet Message Access Protocol) - email protocol",
    161: "SNMP (Simple Network Management Protocol) - network management protocol",
    389: "LDAP (Lightweight Directory Access Protocol) - directory access protocol",
    465: "SMTPS (SMTP over SSL) - secure email transport",
    587: "ESMTP (Extended Simple Mail Transfer Protocol) - email protocol",
    993: "IMAPS (IMAP over SSL) - secure email connection",
    995: "POP3S (POP3 over SSL) - secure email connection",
    1723: "PPTP (Point-to-Point Tunneling Protocol) - VPN protocol",
    3389: "RDP (Remote Desktop Protocol) - remote desktop",
    3306: "MySQL - MySQL database",
    5432: "PostgreSQL - object-relational database",
    1521: "Oracle Database - Oracle database",
    1433: "Microsoft SQL Server - Microsoft SQL Server database",
    5900: "VNC (Virtual Network Computing) - remote desktop access",
    10000: "Apache Hadoop - distributed big-data processing",
    27017: "MongoDB - NoSQL database",
    6379: "Redis - in-memory database",
    5985: "WinRM (Windows Remote Management) - remote Windows management",
    8080: "HTTP Proxy - HTTP proxy server",
    8443: "Tomcat - Java web server",
    8888: "Nginx - web server and reverse proxy",
    3128: "Squid - HTTP proxy server",
    5000: "ASP.NET Core - web application framework",
    8000: "Node.js - JavaScript runtime",
    9000: "Django - Python web framework",
    3000: "Express.js - Node.js web framework",
    7000: "Ruby on Rails - Ruby web framework",
    8008: "Jetty - Java web server and servlet container",
    9090: "JBoss - platform for developing and deploying Java EE applications",
    9200: "Elasticsearch - Lucene-based search engine",
    9300: "Kafka - distributed streaming platform",
    9418: "GitLab CI/CD - GitLab integration environment",
    9999: "Memcached - high-performance in-memory caching",
})

KNOWN_SERVICES: Mapping[int, str] = MappingProxyType({
    20: "FTP-Data", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 67: "DHCP", 68: "DHCP", 80: "HTTP", 110: "POP3",
    123: "NTP", 143: "IMAP", 161: "SNMP", 179: "BGP", 389: "LDAP",
    443: "HTTPS", 445: "SMB", 465: "SMTPS", 514: "Syslog", 587: "ESMTP",
    636: "LDAPS", 993: "IMAPS", 995: "POP3S", 1433: "MSSQL",
    1521: "Oracle", 1723: "PPTP", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 5900: "VNC", 6379: "Redis", 8080: "HTTP-Alt",
    8443: "HTTPS-Alt", 9200: "Elasticsearch", 27017: "MongoDB",
})


def describe_port(port: int) -> str | None:
    """Full description of a known port, or ``None``."""
    return PORT_DESCRIPTIONS.get(port)


def service_label(port: int) -> str:
    """Short service label for a scanner row (empty string if unknown)."""
    return KNOWN_SERVICES.get(port, "")
