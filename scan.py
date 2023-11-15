import simplepyble

if __name__ == "__main__":
    adapters = simplepyble.Adapter.get_adapters()

    if len(adapters) == 0:
        print("No adapters found")

    # Query the user to pick an adapter
    print("Please select an adapter:")
    for i, adapter in enumerate(adapters):
        print(f"{i}: {adapter.identifier()} [{adapter.address()}]")

    #choice = int(input("Enter choice: "))
    choice = 0
    adapter = adapters[choice]

    print(f"Selected adapter: {adapter.identifier()} [{adapter.address()}]")

    adapter.set_callback_on_scan_start(lambda: print("Scan started."))
    adapter.set_callback_on_scan_stop(lambda: print("Scan complete."))
    adapter.set_callback_on_scan_found(lambda peripheral: print(f"Found {peripheral.identifier()} [{peripheral.address()}]"))

    # Scan for 5 seconds
    adapter.scan_for(3000)

    peripherals = adapter.scan_get_results()
    print("The following peripherals were found:")
    for peripheral in peripherals:
        if peripheral.identifier() == "z":
            connectable_str = "Connectable" if peripheral.is_connectable() else "Non-Connectable"
            print(f"{peripheral.identifier()} [{peripheral.address()}] - {connectable_str}")
            print(f'    Address Type: {peripheral.address_type()}')
            print(f'    Tx Power: {peripheral.tx_power()} dBm')

            manufacturer_data = peripheral.manufacturer_data()
            for manufacturer_id, value in manufacturer_data.items():
                print(f"    Manufacturer ID: {manufacturer_id}")
                print(f"    Manufacturer data: {value}")

            services = peripheral.services()
            for service in services:
                print(f"    Service UUID: {service.uuid()}")
                print(f"    Service data: {service.data()}")
            
            print("STRING: " + str(service.data()))
            end = service.data().__len__() + 2
            #print(bin(int(str(service.data().subs))))
            print((str(service.data())[2:end]))
            print(bin(int(str(service.data())[2:end])))

        """M [51:96:d4:f2:90:e5] - Non-Connectable
    Address Type: BluetoothAddressType.RANDOM
    Tx Power: -32768 dBm
    Service UUID: 0000fef3-0000-1000-8000-00805f9b34fb
    Service data: b'2516655'
    
    Service data: b'4194303'
<class 'bytes'>
110100001100010011100100110100001100110011000000110011

always 7
    Service data: b'7'
<class 'bytes'>
110111
6
    """
