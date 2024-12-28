# magic-lamp
a tool to give and receive help in a structured manner

## The gist of it
1. Define what requests and offers you have out of 7 levels that map to each of the chakras. Toggle the corresponding selectors
2. Identify yourself in very general terms by toggling certain selectors if appropriate, so people can visually find you
3. Press "Start Advertising". You can stop using your phone now.
4. When a match is found, your phone will notify you and you can look for the person based on the general identifying information that the other person shared, or peple may come to you based on the identifying features you shared, and you can chat, in person, about how you can help each other based on what you have advertised

## Current plan (from https://github.com/PunchThrough/ble-starter-android.git, which helps on the scanning part, but not on the advertising part. Using Bing Copilot for the advertising part):

Central/Client
A device that scans for and connects to BLE Peripherals to perform some operation. In the context of app development, this is typically an Android device.
NOT FOR MVP

Peripheral/Server
A device that advertises its presence and is connected to a Central to accomplish some task. In app development, this is typically a BLE device you’re working with, like a heart rate monitor.
YES

GATT Service
A collection of characteristics (data fields) that describes a device’s feature, e.g., the Device Information service, can contain a characteristic representing the serial number of the device and another characteristic representing the device’s battery level.
MAYBE FOR MVP (If we can get the MAC address elsewhere)

GATT Characteristic
An entity containing meaningful data that can typically be read from or written to, e.g., the Serial Number String characteristic.
YES

GATT Descriptor
A defined attribute that describes the characteristic it’s attached to, e.g., the Client Characteristic Configuration descriptor, shows if the Central is currently subscribed to a characteristic’s value change.
MAYBE

Notifications
A way for a BLE Peripheral to notify the Central when a characteristic’s value changes. The Central often doesn’t need to acknowledge receiving the packet.
MAYBE

Indications
It is the same as a Notification, except the Central acknowledges each data packet. This guarantees their delivery at the cost of throughput.
MAYBE

UUID
Universally Unique Identifier. It’s a 128-bit number to identify services, characteristics, and descriptors.
YES

BluetoothAdapter
A representation of the Android device’s Bluetooth hardware. An instance of this class is provided by the BluetoothManager class. BluetoothAdapter provides information on the on/off state of the Bluetooth hardware, allows us to query for Bluetooth devices bonded to Android, and allows us to start BLE scans.
YES

BluetoothLeScanner
Provided by the BluetoothAdapter class, this class allows us to start a BLE scan.
Note: ACCESS_COARSE_LOCATION or ACCESS_FINE_LOCATION is required for BLE scans starting from Android M (6.0) and above, ACCESS_FINE_LOCATION is required for Android 10 and above, and BLUETOOTH_SCAN is required for Android 12 and above.
YES, ALL

ScanFilter
It allows one to narrow down scan results to target specific devices we’re looking for during a BLE scan. A typical use case for apps is to filter BLE scan results based on the BLE devices’ advertised service UUIDs.
YES, BY SERVICE UUID

ScanResult
It represents a BLE scan result obtained via BLE scan and contains information such as the BLE device’s MAC address, RSSI (signal strength), and advertisement data. The getDevice() method exposes the BluetoothDevice handle, which may contain the name of the BLE device and allows the app to connect to it.
YES, ADVERTISEMENT DATA AND MAC ADDRESS AS UNIQUE IDENTIFIER

BluetoothDevice
Represents a physical Bluetooth (not specifically BLE) device that the app can connect to, bond (pair) with, or both. This class provides key information, including the device name, if it’s available, its MAC address, and its current bond state.
NO

BluetoothGatt
An entry point to the BLE device’s GATT profile. It allows us to perform service discovery and connection teardown, request MTU updates (more on this later), and get access to the services and characteristics that are present on the BLE device. We can think of this as a handle to an established BLE connection.
MAYBE, ONLY IF SERVICE DISCOVERY/SCAN FILTERING CAN ONLY BE DONE AFTER CONNECTING

BluetoothGattService, BluetoothGattCharacteristic and BluetoothGattDescriptor
Wrapper classes represent GATT services, characteristics, and descriptors, as defined in the Table of Glossary earlier in this guide.
YES, SERVICE AND CHARACTERISTIC

BluetoothGattCallback
The app must implement the main interface to receive callbacks for most BluetoothGatt-related operations like reading, writing, or getting notified about incoming Notifications or Indications.
YES

Parsing and Understanding Scan Results
A ScanResult object gets surfaced as part of ScanCallback’s onScanResult(...) method, and generally the things we care about in a ScanResult are:

The MAC address of the device that identifies the advertising scan results.
Obtained via getDevice() followed by getAddress(), or simply device.address in Kotlin.
Warning: a device implementing Bluetooth 4.2’s LE Privacy feature will randomize its public MAC address periodically, so a MAC address obtained via scanning should not generally be used as a long-term means to identify a device — unless the firmware guarantees that it’s not rotating MAC addresses, or if it has an out-of-band way to communicate what it’s current public MAC address is, or if the use case involves bonding, which would allow Android to derive the latest/current MAC address of the device.
NO

The name of the device that we can show to the user.
Obtained via getDevice() followed by getName(), or simply device.name in Kotlin. Not all BLE devices advertise the device name, so some BLE devices’ names may be null.
NO

The RSSI or signal strength of the advertising BLE device, measured in dBm.
Obtained via getRssi(), or simply rssi in Kotlin.
Sorting scan results by descending order of signal strength is a good way to find the peripheral closest to the Android device, but it’s not a 100% guarantee because RSSI can be affected by the transmission power of the advertising device’s antenna, and other physical factors such as the presence of metallic objects around the Android or BLE device.
The decibel values are oftentimes relative and not based on an absolute scale. This means that an RSSI reading of -42 dBm can be “close range” for one Android phone but “medium range” for another. It’s generally not recommended to universally map RSSI readings to real-world physical distances.
NO

The BluetoothDevice handle that we need in order to connect to the device, accessed via the getDevice() method.
NO

Extra advertisement data in the ScanResult’s ScanRecord, accessed via getScanRecord().
ScanRecord conveniently parses out any manufacturer specific data and service data from the scan record and these can be accessed using the getManufacturerSpecificData(...) and getServiceData(...) methods.
The raw scan record bytes can be accessed using the getBytes() method.
YES

Specifying Scan Settings
Aside from scan results filtering, Android also allows us to specify the scan settings to use during scanning, represented by the ScanSettings class, which also comes with its own ScanSettings.Builder builder class. Here are a few practical and commonly used scan settings that Android allows us to tweak:

Specify the desired BLE scan mode, from low-powered high-latency scans to high-powered low-latency scans.
Most apps scanning in the foreground should use SCAN_MODE_BALANCED for scans that will last longer than 30 seconds.
SCAN_MODE_LOW_LATENCY is recommended if the app only scans for a brief period, typically to find a very specific type of device.
SCAN_MODE_LOW_POWER is used for extremely long-duration scans or scans that occur in the background (with the user’s permission). Note that the high latency nature of this low-power scan mode may result in missed advertisement packets if the device you’re scanning for has a high enough advertising interval that it doesn’t overlap with the app’s scan frequency.
YES, LOW LATENCY

Specify the callback type for the BLE advertisement packets that were encountered.
Apps like LightBlue that require continuous updating of incoming advertisement packets should use CALLBACK_TYPE_ALL_MATCHES to get notified about all incoming packets. This is the default setting if an app doesn’t specify the desired callback type.
CALLBACK_TYPE_FIRST_MATCH is used if an app is only concerned about getting a single callback for each device that matches the filter criteria specified by ScanFilter (or all devices in the vicinity if a ScanFilter wasn’t specified). 
CALLBACK_TYPE_MATCH_LOST is a bit of an odd one — we’ve had mixed experience using this and don’t recommend it in general. You’re typically better off implementing a timer yourself that periodically goes through your list of ScanResults and removing outdated ones (e.g., haven’t been encountered in the last 10 seconds or so) based on ScanResult’s getTimestampNanos() method, but note that this method provides a timestamp since Android’s system boot time and not the time since Epoch time.
YES, TRY CALLBACK_TYPE_ALL_MATCHES AND CALLBACK_TYPE_FIRST_MATCH

Specify the threshold at which an advertisement packet sighting should be surfaced as a scan result.
MATCH_MODE_STICKY is useful in filtering out advertising BLE devices that are too far away from the Android device since it requires a higher threshold of signal strength and number of sightings before that BLE device is surfaced as a scan result to our app.
MATCH_MODE_AGGRESSIVE is the opposite of MATCH_MODE_STICKY and will show you every device advertising in the range of the BLE scanner, near or far.
YES, MATCH_MODE_AGGRESSIVE

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