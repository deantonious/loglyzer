```
 ▄█        ▄██████▄     ▄██████▄   ▄█       ▄██   ▄    ▄███████▄     ▄████████    ▄████████ 
███       ███    ███   ███    ███ ███       ███   ██▄ ██▀     ▄██   ███    ███   ███    ███ 
███       ███    ███   ███    █▀  ███       ███▄▄▄███       ▄███▀   ███    █▀    ███    ███ 
███       ███    ███  ▄███        ███       ▀▀▀▀▀▀███  ▀█▀▄███▀▄▄  ▄███▄▄▄      ▄███▄▄▄▄██▀ 
███       ███    ███ ▀▀███ ████▄  ███       ▄██   ███   ▄███▀   ▀ ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
███       ███    ███   ███    ███ ███       ███   ███ ▄███▀         ███    █▄  ▀███████████ 
███▌    ▄ ███    ███   ███    ███ ███▌    ▄ ███   ███ ███▄     ▄█   ███    ███   ███    ███ 
█████▄▄██  ▀██████▀    ████████▀  █████▄▄██  ▀█████▀   ▀████████▀   ██████████   ███    ███ 
▀                                 ▀                                              ███    ███ 
```

Loglyzer is a command-line tool to analyze the content of Squid Proxy log files. The tool can provide the following details:
* Most frequent IP/s and the occurrence  count
* Least frequent IP/s and the occurrence  count
* Events per second (EPS)
* Total bytes exchanged

The output will be displayed on the console and saved to a local file.

# Installation
## Dependencies 
Requires Python 3.7+

## Docker

Loglyzer can be run using Docker. First build the docker image:
```
forty@two:~# git clone https://github.com/deantonious/loglyzer
forty@two:~# cd loglyzer
forty@two:~# docker build --tag loglyzer .
```

Example of running the CLI using the built image (remember mapping a volume to be able to access the file system):
``` 
forty@two:~# docker run -v /home/forty:/app --rm loglyzer data/access.log --eps --mfip
```

## From Source

This install option is building from source, simply run these commands and you are all set! 
<br>
```
forty@two:~# git clone https://github.com/deantonious/loglyzer
forty@two:~# cd loglyzer
forty@two:~# python -m pip install -r requirements.txt
```
Now you are ready to run loglyzer:
```
forty@two:~# python -m loglyzer --help
```
# Usage

The tool can be provided with a single file or a directory containing multiple logfiles. When providing a directory, the data will be analyzed for each individual file and the results will all be stored within the same output file. Please follow this command structure:

```
forty@two:~# loglyzer [PATH|DIRECTORY] [OPTIONS]
```

Available flags:
* `-v, --version     Version information.`
* `--mfip            Most frequent IP.`
* `--lfip            Least frequent IP.`
* `--eps             Events per second.`
* `--bytes           Total amount of bytes exchanged.`
* `--help            Show this message and exit.`

When the same number of occurrences is identified for multiple IP addresses, all these IPs will be shown among a single number of occurrences.

Example usage to get the most frequent IP, EPS and exchanged bytes count:
```
forty@two:~# python -m loglyzer .\data\access.log --mfip --eps --bytes
forty@two:~# [INFO] Analysis results for file .\data\access.log
forty@two:~# [RESULT] {'most_frequent_ips': {'list': ['10.105.23.212'], 'occurrences': 7224}, 'events_per_second': 24.83, 'exchanged_bytes': 2277502499}
forty@two:~# [INFO] Results saved to output_08_11_2022_23_45_39.json
```

Example output file:
```json
[
    {
        "file_path": "./data/access.log",
        "analysis_results": {
            "most_frequent_ips": {
                "list": [
                    "10.105.23.212"
                ],
                "occurrences": 7224
            },
            "events_per_second": 24.83,
            "exchanged_bytes": 2277502499
        }
    }
]
```

# Development
To execute the tests, run the following command:
```
forty@two:~# python -m pytest tests/
```

# Notes 
## Logfile Format
The reference document states field 2 refers to the _**Response header size in bytes**_, though the [official documentation](https://wiki.squid-cache.org/Features/LogFormat) states it refers to the duration: _**how many milliseconds the transaction busied the cache**_. Although, for this POC, the total amount of bytes has been calculated:

```
TOTAL_BYTES = SUM(RESPONSE_HEADER_BYTES + RESPONSE_SIZE_BYTES)
```

## EPS Calculation
This tool is used for logfiles, it is assumed the file starts at the earliest events and ends at the latest events.

EPS are calculated by dividing the total amount of events by the total amount of seconds within continuous intervals of time (taking > 1s jumps as 1s):

```
EPS = EVENT_COUNT / TOTAL_SECONDS
```