This plugin is not affiliated with pi-hole in any way.

## How to use the labels

You can add one or more keys to your labels by choosing one from the list below and put it into parentesis {}.

Available keys:
- domains_being_blocked
- dns_queries_today
- ads_blocked_today
- ads_percentage_today
- unique_domains
- queries_forwarded
- queries_cached
- clients_ever_seen
- unique_clients
- dns_queries_all_types
- reply_UNKNOWN
- reply_NODATA
- reply_NXDOMAIN
- reply_CNAME
- reply_IP
- reply_DOMAIN
- reply_RRNAME
- reply_SERVFAIL
- reply_REFUSED
- reply_NOTIMP
- reply_OTHER
- reply_DNSSEC
- reply_NONE
- reply_BLOB
- dns_queries_all_replies
- privacy_level
- status

Example usage: `{ads_percentage_today} %`