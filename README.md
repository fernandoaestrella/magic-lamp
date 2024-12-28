# magic-lamp
a tool to give and receive help in a structured manner

## The gist of it
1. Define what requests and offers you have out of 7 levels that map to each of the chakras. Toggle the corresponding selectors
2. Identify yourself in very general terms by toggling certain selectors if appropriate, so people can visually find you
3. Press "Start Advertising". You can stop using your phone now.
4. When a match is found, your phone will notify you and you can look for the person based on the general identifying information that the other person shared, or peple may come to you based on the identifying features you shared, and you can chat, in person, about how you can help each other based on what you have advertised

## Variables to handle in the future

when advertising:
    - user is on the device or not
    - user has the app open or not

user advertises:
    - its own data and/or other's data

platform (python code, MIT App Inventor, Androdi app, iOS app, etc)

protocol:
    - Bluetooth Low Energy
    - Internet
    - None

## Standard for transmission

68 bits available as data in BLE advertisements if device name is one character long
1000010000100001000010000100001000010000100001000010000100001000010

14 bits required for data regarding the needs (7 requests + 7 offers)
68 - 14 = 54

identification:
1 bit for male/female
1 bit for if at or taller than 5' 9" (175.259 cm) for men, or at or taller than 5'4" (162.56 cm) for women
1 bit for if older than 32 for men, or is older than 34 for women
1 bit for facial hair if men, or hair reaching shoulder or beyond if woman
1 bit for wearing glasses
4 bits for 16 tshirt colors
3 bits for 8 pants color
11 total

54 - 11 = 43

## Notes

If needed, the app will act as both a Broadcaster and an Observer, as both GAP profiles do not allow connections, which we don't need. Source [here](https://novelbits.io/bluetooth-low-energy-advertisements-part-1/)

## Next Steps

- MIT App Inventor:
    - To get data, we need the device's MAC Address and the Service UUID. With personal Android smartphone and emitting data from iPhone, load app in Android. To confirm how the app is seeing both data points, based on https://iot.appinventor.mit.edu/#/bluetoothle/bluetoothleintro, look at:
        - "AdvertiserAddresses"
        - "DeviceCharacteristics" and/or "DeviceServices"