
Examples
========

:any:`Getpublicdata`
++++++++++++++++++++

A simple :any:`Getpublicdata` example::

    import netatmo

    # your netatmo connect developer credentials
    credentials = {
        "password":"5uP3rP45sW0rD",
        "username":"user.email@internet.com",
        "client_id":    "03012823b3fd2e420fbf980b",
        "client_secret":"YXNkZmFzZGYgamFzamYgbGFzIG"
    }

    # create an api client
    client = netatmo.api.client.NetatmoClient()
    # tell the client's authentication your credentials
    client.authentication.credentials = credentials
    # optionally give the authentication a temporary file.
    # The tokens are then stored there for later reuse, 
    # e.g. next time you invoke this script.
    # This saves time because no new tokens have to be requested.
    # New tokens are then only requested if the old ones expire.
    client.authentication.tmpfile = "temp_auth.json"

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
    print(hamburg.dataframe)


Output::
    
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

