### Snipets
```python
# connect to the camera
# most chinese cameras have default IP 192.168.1.10 and onvif ports 80 or 8899
cam = ONVIFCamera('192.168.1.10', 80, 'admin', '')
```

```python
# typical getters
cam.devicemgmt.GetNetworkInterfaces()
cam.devicemgmt.GetNTP()
cam.devicemgmt.GetSystemDateAndTime()
cam.devicemgmt.GetDeviceInformation()

# quality settings
cam.create_imaging_service()
cam.create_media_service()
cam.media.GetProfiles()
cam.media.GetVideoEncoderConfigurations()
cam.media.GetVideoEncoderConfigurationOptions()
```

### Config snipets

#### Enable DHCP
```python
cam.devicemgmt.SetNetworkInterfaces({
'InterfaceToken': 'eth0', 
'NetworkInterface': {
    'Enabled': True,
    'IPv4': {
        'Enabled': True,
        'Manual': [],
        'DHCP': True,
    },  
}})
cam.devicemgmt.SystemReboot()
```
#### Set Manual IP address
```python
cam.devicemgmt.SetNetworkInterfaces(dict(
    InterfaceToken='eth0',    
    NetworkInterface=dict(         
        IPv4=dict(
            Enabled=True,
            Manual=[dict(
                Address='192.168.1.10',
                PrefixLength=24)],
            DHCP=False))))
```

### Setting current datetime
```python
from datetime import datetime, pytz
local_timezone = '<YOUR TIMEZONE>'
now = datetime.now(pytz.timezone(local_timezone))
# some cams are too stupid to work with NTP/timezones properly - trick them with UTC time
cam.devicemgmt.SetSystemDateAndTime({
    'DateTimeType': '<',
    'DaylightSavings': False,
    'TimeZone': {
        'TZ': 'UTC'
    },
    'UTCDateTime': {
        'Time': {
            'Hour': now.hour,
            'Minute': now.minute,
            'Second': now.second
        },  
        'Date': {
            'Year': now.year,
            'Month': now.month,
            'Day': now.day
        }   
    }
})
cam.devicemgmt.GetSystemDateAndTime()
```

### Get info

#### Get snapshot URIs
see https://www.onvif.org/onvif/ver10/media/wsdl/media.wsdl
```python
media_service = cam.create_media_service()
profiles = media_service.GetProfiles()
for profile in profiles:
    snapshot = media_service.create_type('GetSnapshotUri')
    snapshot.ProfileToken = profile.token
    output_snap_uri = media_service.GetSnapshotUri(snapshot)
    print("URI for snapshot: {}".format(output_snap_uri.Uri))
```

#### Get stream URIs
```python
cam.create_media_service()
for profile in cam.media.GetProfiles():
    print('profile %s' % profile.token)
    if not hasattr(profile, 'MetadataConfiguration'):
        cam.media.AddMetadataConfiguration({
            'ProfileToken': profile.token,
            'ConfigurationToken': config.token,
        })  
    resp = cam.media.GetStreamUri({
        'StreamSetup': {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}},
        'ProfileToken': profile.token,
    })  
    print(resp.Uri)

```
