import sys
import time
import xxhash
from bitarray import bitarray

# These are constants used throughout the program.
FILTER_SIZE = 2**23 # The size of the bloom filter (number of bits).
HASH_SEED = 8657309 # The seed of the hash to use.

# Alias the xxhash32 function from xxhash as x.  This will be used as our hash
# function.  It will be used with different seeds to generate different output
# As we need to hash either 3 or 5 times..
x = xxhash.xxh32

"""
Function: get_bit_locations(string, int)
Description: Takes a password (as a string) and hashes it num_hashes times.
Based on the size of the bloom filter defined by the constant FILTER_SIZE,
it will return (num_hashes) number of indexes that are within bounds of the
bloom filter's bit array.
"""
def get_bit_locations(password, num_hashes):
    # Initialize an empty array to store locations within the bloom filter
    bit_locations = []

    # We will use this as a seed for the first hash function
    h_seed = HASH_SEED

    # Generate any number of bit locations determined by num_hashes
    for i in range(num_hashes):
        # Set the new seed as the result from this hash
        h_seed = x(password, seed = h_seed).intdigest()
        # The result of the hash mod the bloom filter size is the location
        bit_locations.append(h_seed % FILTER_SIZE)

    # return the locations for a single password string
    return bit_locations


"""
Function: bloom_insert(bit array, string, int)
Description: Insert a password string with a certain number of hashes into
the bloom filter's bit array.  Uses get_bit_locations() to get where to insert
the password.  Sets the bit array to 1 at the locations
"""
def bloom_insert(bloom, password, num_hashes):
    bit_locations = get_bit_locations(password, num_hashes)

    # Set the appropriate bits returned by get_bit_locations
    for location in bit_locations:
        bloom[location] = 1


"""
Function: bloom_insert_from_file(file, bit array, int)
Description: Open the file specified, insert each line as a password
into the bloom filter's bit array.  Use num_hashes hashes for each password
"""
def bloom_insert_from_file(filename, bloom, num_hashes):
    # Open the file, get each line as a password.
    dictionary_file = open(filename, 'r')
    passwords = dictionary_file.readlines()

    for password in passwords:
        # Remove trailing characters.
        password = password.rstrip()
        # Insert the password into the bloom filter
        bloom_insert(bloom, password, num_hashes)


def check_passwords(input_file, output_file, bloom, num_hashes):
    # Open the file with passwords we want to check
    input_file = open(input_file, 'r')
    # Open the file that we want to write the results to
    output_file = open(output_file, 'w')

    # read the passwords from the input
    passwords = input_file.readlines()
    num_passwords = int(passwords[0], 10)

    # Write the number of passwords checked as the first line in the file
    output_file.write("%d\n" % num_passwords)

    # Remove the password count at the top.
    passwords = passwords[1:]

    # Iterate thorough the password array to check each password
    for password in passwords:
        # remove trailing characters
        password = password.rstrip()
        # Get the password's bit locations to check in the bloom filter
        bits = get_bit_locations(password, num_hashes)
        count = 0
        result = ''

        # Check each password in the bloom filter
        for bit in bits:
            if bloom[bit] == 1:
                count += 1

        # If nothing shows up, then we can conclude that it's not in the bad
        # passwords
        if count == 0:
            result = '%s %s\n' % (password, 'no')
        # If even a single bit shows up, it might be in the bad passwords
        else:
            result = '%s %s\n' % (password, 'maybe')

        # Write the result to the file
        output_file.write(result)

    # Close the open files.
    input_file.close()
    output_file.close()

    # Return the number of passwords processed
    return num_passwords


def main():
    # check for the correct number of arguments
    if len(sys.argv) != 9:
        print("Incorrect number of arguments. Correct usage:\n\n"
                "$> python gallegon_bloom_filter.py -d dictionary_file, -i "
                "input_file -o3 output3_file -o5 output5_file\n")
        quit()

    if sys.argv[1] != "-d" or sys.argv[3] != "-i" or sys.argv[5] != "-o3" or \
            sys.argv[7] != "-o5":

        print("Incorrect options usage. Correct usage:\n\n"
                "$> python gallegon_bloom_filter.py -d dictionary_file, -i "
                "input_file -o3 output3_file -o5 output5_file\n")
        quit()

    # Create Bloom filters with bit arrays of size FILTER_SIZE bits
    bloom_3 = bitarray(FILTER_SIZE)
    bloom_5 = bitarray(FILTER_SIZE)

    # Get the filenames from command line arguments.
    dictionary_file = sys.argv[2]
    input_file = sys.argv[4]
    output_3_file = sys.argv[6]
    output_5_file = sys.argv[8]


    # Initialize bloom filters with all zeros
    bloom_3.setall(0)
    bloom_5.setall(0)

    # Time the amount of time it takes to insert the dictionary in the bloom
    # filter with 3 hashes
    start = time.time()
    bloom_insert_from_file(dictionary_file, bloom_3, 3)
    end = time.time()

    print("Time to insert passwords from %s using 3 hashs: %fs" % \
            (dictionary_file, (end - start)))

    # Time the amount of time it takes to insert the dictionary in the bloom
    # filter with 5 hashes
    start = time.time()
    bloom_insert_from_file(dictionary_file, bloom_5, 5)
    end = time.time()
    print("Time to insert passwords from %s using 5 hashs: %fs" % \
            (dictionary_file, (end - start)))

    # Time how long it takes to check the passwords with 5 hashes
    start = time.time()
    check_5 = check_passwords(input_file, output_5_file, bloom_5, 5)
    end = time.time()
    print("Time to check %d passwords with 5 hashes: %fs" % \
            (check_5, (end - start)))
    # Time how long it takes to check the passwords with 3 hashes
    start = time.time()
    check_3 = check_passwords(input_file, output_3_file, bloom_3, 3)
    end = time.time()
    print("Time to check %d passwords with 3 hashes: %fs" % \
            (check_3, (end - start)))

    # Time how long it takes to check the passwords with 5 hashes
    start = time.time()
    check_5 = check_passwords(input_file, output_5_file, bloom_5, 5)
    end = time.time()
    print("Time to check %d passwords with 5 hashes: %fs" % \
            (check_5, (end - start)))


main()
