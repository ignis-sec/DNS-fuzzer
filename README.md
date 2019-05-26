# DNS-fuzzer
A script that fuzzes a domain server for domain names from a wordlist.

#### Requires nslookup.

### Usage

`python3 nsfuzzer.py <arguments> wordlist`

### Arguments
```
-t: Number of threads. Default is 10
-n:  Specific nameserver. Default is any
-v:  verbose
wordlist: Wordlist to attempt from
```

It just checkes nslookup results to see if the word from wordlist is registered under a dns server.
Useful for internal networks with arbitrary domain records.

Different from wfuzz, since wfuzz is not always able to send requests to multiple recepient servers, and that name-registered servers may not have a running http server.

While wfuzz is doing a http get request, nsfuzzer is validating host existance by negotiating with the dns server.
