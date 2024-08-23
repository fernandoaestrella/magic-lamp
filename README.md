# magic-lamp
a tool to give and receive help in a structured manner

## The gist of it
1. Define what needs you have out of 7 levels that map to each of the chakras, and if you can help in each of the levels. Toggle the corresponding selectors
2. Identify yourself in very general terms by toggling certain selectors if appropriate, so people can find you
3. Press "Start Advertising"
4. Store your phone away
5. When a match is found, your phone will notify you and you can look for the person based on the general identifying information that the other person shared, or peple may come to you based on the indenficating features you shared, and you can chat about how you can help each other based on what you have advertised

Current plan:

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
