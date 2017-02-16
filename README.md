# netatmo Python package [![Build Status](https://travis-ci.org/nobodyinperson/python3-netatmo.svg?branch=master)](https://travis-ci.org/nobodyinperson/python3-netatmo)

This packages provides easy access to the [netatmo](https://netatmo.com) [API](https://dev.netatmo.com).
It is **painless** as it completely and intelligently hides the OAuth2 authentication from you. 

## Capabilities

Currently, the weather API's methods `Getpublicdata`, `Getstationsdata` and `Getmeasure` are implemented.

## Example usage

An example of obtaining all public station's data in the region of Hamburg/Germany:

```python
import netatmo

# your netatmo connect developer credentials
credentials = {
        "client_id": "58357ea765d1c4ea7f8c8a7b",
        "client_secret": "7akCecdr31Bbw3nhdnplGLW4vV",
        "password": "5up3rpa55W0rd",
        "username": "user.email@internet.com"
    }

# create an api client
client = netatmo.api.client.NetatmoClient()
# tell the client's authentication your credentials
client.authentication.credentials = credentials

# lat/lon outline of Hamburg/Germany
hamburg_region = {
    "lat_ne" : 53.7499,
    "lat_sw" : 53.3809,
    "lon_ne" : 10.3471,
    "lon_sw" : 9.7085,
}

# issue the API request
hamburg = client.Getpublicdata(region = hamburg_region)
# convert the response to a pandas.DataFrame
print(hamburg.response_as_pandas_dataframe)
```

output (excerpt):

```
     index   altitude  humidity                 id   latitude  longitude  \
0        0  30.000000        84  70:ee:50:12:9a:b8  53.516950  10.155990   
1        1  23.000000        83  70:ee:50:03:da:4c  53.523361  10.167193   
2        2  23.000000        76  70:ee:50:01:47:34  53.510080  10.165600   
3        3  15.000000        93  70:ee:50:03:bc:2c  53.530948  10.134062    
..     ...        ...       ...                ...        ...        ...   

     pressure  temperature       time_humidity       time_pressure  \
0      1029.1          8.1 2017-02-16 10:59:31 2017-02-16 11:00:05   
1      1026.7          8.3 2017-02-16 10:53:53 2017-02-16 10:54:01   
2      1030.0          9.4 2017-02-16 10:53:06 2017-02-16 10:53:42   
3      1026.8          8.0 2017-02-16 10:56:32 2017-02-16 10:56:54   
..        ...          ...                 ...                 ...   

       time_temperature       timezone  
0   2017-02-16 10:59:31  Europe/Berlin  
1   2017-02-16 10:53:53  Europe/Berlin  
2   2017-02-16 10:53:06  Europe/Berlin  
3   2017-02-16 10:56:32  Europe/Berlin   
..                  ...            ...  

[708 rows x 12 columns]

```

## Install

Install this module via `pip3`:

```bash
# local user library under ~/.local
pip3 install --prefix=~/.local git+https://github.com/nobodyinperson/python3-netatmo
# system-wide
sudo pip3 install git+https://github.com/nobodyinperson/python3-netatm
```

## Development

The following might only be interesting for developers

### Local installation

Install this module from the repository root via `pip3`:

```bash
# local user library under ~/.local
pip3 install --prefix=~/.local .
# in "editable" mode
pip3 install --prefix=~/.local -e .
```

### Testing

To be able to run *all* tests, you need to specify valid **credentials and a device and model id** of your test station in the file `tests/USER_DATA.json`. Copy the example file (`cp tests/USER_DATA.json.example tests/USER_DATA.json`) and adjust it. Otherwise, only the possible tests are run.

Then:

- `make test` to run all tests directly
- `make testverbose` to run all tests directly with verbose output
- `make setup-test` to run all tests via the `./setup.py test` mechanism

### Versioning

- `make increase-patch` to increase the patch version number
- `make increase-minor` to increase the minor version number
- `make increase-major` to increase the major version number
