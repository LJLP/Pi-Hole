This plugin is not affiliated with pi-hole in any way.

## How to use the labels for the Info

You can add one or more keys to your labels by choosing one from the list below and put it into parentesis {}.

Available keys are all the keys that the PiHole endpoint offers in the response. Take a look [here](https://ftl.pi-hole.net/master/docs/#get-/stats/summary)

### Small list of useful keys:
| Key                              | Description                                            |
|--------------------------------- |----------------------------                            |
|**queries_total**                 | _Total number of queries_                              |
|**queries_blocked**               | _Number of blocked queries_                            |
|**queries_percent_blocked**       | _Percent of blocked queries_                           |
|**clients_active**                | _Number of active clients (seen in the last 24 hours)_ |
|**clients_total**                 | _Total number of clients seen by FTL_                  |
|**gravity_domains_being_blocked** | _Number of domain on your Pi-hole's gravity list_      |

Example usage: `{queries_total}`