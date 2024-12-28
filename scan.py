# TO DO: Scan until finding the desired device
import simplepyble

delimiter = "============================================================================================="
descriptions_positive_men = ["Looks like a man", "Is taller than 5'9\" (175 cm)", "Is older than 32 years old", "Has facial hair", "Is wearing glasses"]
descriptions_negative_men = ["Looks like a woman", "Is shorter than 5'9\" (175 cm)", "Is younger than 32 years old", "Does not have facial hair", "Is not wearing glasses"]
descriptions_positive_women = ["Looks like a woman", "Is taller than 5'4\" (163 cm)", "Is older than 34 years old", "Her hair reaches below her shoulder", "Is wearing glasses"]
descriptions_negative_women = ["Looks like a woman", "Is shorter than 5'4\" (163 cm)", "Is younger than 34 years old", "Her hair reaches above her shoulder", "Is not wearing glasses"]
descriptions_arrays = [ [descriptions_negative_women, descriptions_positive_women], [descriptions_negative_men, descriptions_positive_men] ]
descriptions_requests = ["Basic need", "Players", "Support for project", "Support facing fears", "Filter negativity", "Clarity", "Profound connection"]

def get_bits(n):
    bits = []
    while n > 0:
        bits.append(n & 1)
        n >>= 1
    bits.reverse()
    return bits

class Match:
  def __init__(self, received_bits, match_count, person_description):
    self.received_bits = received_bits
    self.match_count = match_count
    self.person_description = person_description

def describe_person(received_bits):
    person_description = ""
    index = 0

    # Describe the person
    for bit in received_bits:
        if (index > 13) & (index < 19):
            person_description = person_description + descriptions_arrays[received_bits[14]][bit][index -  14] + "\n"

        index += 1
    
    return person_description

def analyze_match(received_bits):
    index = 0
    match_count = 0

    for bit in received_bits:
        # For all bits regarding our matches
        if index < 14:
            # For all even numbered index bits 
            if index % 2 == 0:
                # If I am requesting and the other person is offering, increase our match count
                if (my_bits[index] == 1) & (received_bits[index + 1] ==  1):
                    match_count += 1
            # For all uneven numbered index bits
            else:
                # If I am offering and the other person is requesting, increase our match count
                if (my_bits[index] == 1) & (received_bits[index - 1] ==  1):
                    match_count += 1
        
        index += 1
    
    return match_count
            
if __name__ == "__main__":
    received_matches = []

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

    # For all messages found
    received_matches = {}
    for peripheral in peripherals:    
        # For all messages directed to this app
        if True:
        # if peripheral.identifier() == "":
            # Save them in a dictionary
            
            """connectable_str = "Connectable" if peripheral.is_connectable() else "Non-Connectable"
            print(f"{peripheral.identifier()} [{peripheral.address()}] - {connectable_str}")
            print(f'    Address Type: {peripheral.address_type()}')
            print(f'    Tx Power: {peripheral.tx_power()} dBm')

            manufacturer_data = peripheral.manufacturer_data()
            for manufacturer_id, value in manufacturer_data.items():
                print(f"    Manufacturer ID: {manufacturer_id}")
                print(f"    Manufacturer data: {value}")"""
            services = peripheral.services()
            for service in services:
                print(f"    Service UUID: {service.uuid()}")
                print(f"    Service data: {service.data()}")
                
                end = service.data().__len__() + 2

                # Convert from byte to str to int to binary to string to list of strings to list of numbers. Don't ask why
                received_bits = list(str(bin(int(str(service.data())[2:end])))[2:])
                # Must fill with extra leading zeros to complete the amount of expected bits
                while received_bits.__len__() < 22:
                    received_bits.insert(0, 0)
                
                for index in range(0, received_bits.__len__()):
                    if received_bits[index] == '1':
                        received_bits[index] = 1
                    else:
                        received_bits[index] = 0
                
                index = 0
                #..........1  2  3  4  5  6  7  8  9  10 11 12 13 14 .  .  .  .  19 20 21 22
                my_bits = [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1]

                # Create a new match
                current_match = Match(received_bits, analyze_match(received_bits), describe_person(received_bits))
                received_matches[peripheral.address()] = current_match

    if received_matches.__len__() > 0:
        print(delimiter + "\nYou have matched with ")
        print(str(received_matches.__len__()))
        if received_matches.__len__() > 1:
            print("people")
        else:
            print("person")
        print(delimiter)

    index = 1
    for match in received_matches:
        print("Match " + str(index) + ":")
        print("You have matched in " + str(received_matches[match].match_count) + " categories, with a person that looks like this:\n")
        print(received_matches[match].person_description)
        print("Now go look for them!\n" + delimiter)

"""
        M [51:96:d4:f2:90:e5] - Non-Connectable
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
