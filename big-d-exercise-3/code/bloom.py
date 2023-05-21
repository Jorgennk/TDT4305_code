# This is the code for the Bloom Filter project of TDT4305

import configparser  # for reading the parameters file
from pathlib import Path  # for paths of files
import time  # for timing

import random
import numpy as np
from colorama import Fore, Back, Style # Bonus for style points

# Global parameters

# This is changed from default parameters.ini to testing_parameters.ini
parameter_file = 'testing_parameters.ini'  # the main parameters file
# the main path were all the data directories are
data_main_directory = Path('data')
# dictionary that holds the input parameters, key = parameter name, value = value
parameters_dictionary = dict()


class BloomFilter:

    def __init__(self):
        self.h = None
        self.N = None
        self.hash_filter = []
        self.passwords_read = []

        self.num_fp = 0

    def print_self(self):
        print(f"h: {self.h}")
        print(f"N: {self.N}")
        # print(f"hash_filter: {self.hash_filter}")

    # DO NOT CHANGE THIS METHOD
    # Reads the parameters of the project from the parameter file 'file'
    # and stores them to the parameter dictionary 'parameters_dictionary'
    def read_parameters(self):
        config = configparser.ConfigParser()
        config.read(parameter_file)
        for section in config.sections():
            for key in config[section]:
                if key == 'data':
                    parameters_dictionary[key] = config[section][key]
                else:
                    parameters_dictionary[key] = int(config[section][key])

    def set_self_variables(self, h = None, n = None):
        if not h:
            self.h: int = int(parameters_dictionary['h'])
        else:
            self.h = h
            
        if not n:
            self.N: int = int(parameters_dictionary['n'])
        else:
            self.N = n
            
        self.hash_filter: list = list(np.zeros(self.N))

        # Only missing self.passwords_read, but that is set in the read_data method

    # TASK 2
    def bloom_filter(self, N, new_pass):
        # implement your code here

        # Hash the password
        hash_values = self.hash_functions(new_pass)

        # Set position in the filter to 1, this creates the signature of the password
        for i in hash_values:
            try:
                self.hash_filter[i] = 1
            except:
                print(f"Failed, it was because of {i} with h = {self.h} and N = {self.N}")
                print(f"Size of filter: {len(self.hash_filter)}")
                

        return self.hash_filter # This return isn't needed, but keep in case we change the code

    # DO NOT CHANGE THIS METHOD @@@@@@ I dun goofed, changed it. But it was needed @@@@@@@
    # Reads all the passwords one by one simulating a stream and calls the method bloom_filter(new_password)
    # for each password read

    def read_data(self, file, break_after=None):
        time_sum = 0
        pass_read = 0

        # Add utf8 encding
        with file.open(encoding="utf8") as f:
            for line in f:
                pass_read += 1
                new_password = line[:-3]
                self.passwords_read.append(new_password)
                ts = time.time()
                self.bloom_filter(self.N, new_password)
                te = time.time()
                time_sum += te - ts
                
                # Uncomment 2 lines below to see progress
                # if pass_read % 50000 == 0:
                #     print(f"{pass_read} passwords read and hashed")

                if break_after is not None and pass_read >= break_after:
                    break

        return pass_read, time_sum

    # A function that gives a list of primes between 0 and N
    # def primes(N):
    #     primes = []
    #     for i in range(2, N):
    #         if i %1000 == 0:
    #             print(f"counted {i}")
    #         prime = True
    #         for j in range(2, i):
    #             if i % j == 0:
    #                 prime = False
    #         if prime:
    #             primes.append(i)
    #     return primes

    # TASK 1
    # Created h number of hash functions

    def hash_functions(self, password):
        """
        --- These are set in the object variables ---
        param h: number of hash functions
        param N: size of the Bloom filter

        --- input ---
        param password: the password to hash

        returns: a list of h hash values (hashvalue of password)

        """

        # implement your code here

        # A random slection of primes to use for hash functions
        # These are set as an example, so we can replicate the results
        p = [31063, 24517, 44729, 73, 14251, 3023, 6577,
             48751, 457, 7177, 49499, 20479, 8867, 7717, 42643]

        sums_return = []
        for i in range(self.h):
            tmpsum = 0

            for j in range(len(password)):
                tmpsum += ord(password[j]) * (p[i]**j)
            tmpsum = tmpsum % self.N
            sums_return.append(tmpsum)

        # Line below is for bug testing
        # print(sums_return)
        
        
        return sums_return

    # TASK 3
    def count_fp(self):

        # Passwords from this found on piazza post 102
        passwords_not_in_passwords_csv_file = ['07886819', '0EDABE59B', '0BFE0815B', '01058686E', '09DFB6D3F', '0F493202C',
                                               '0CA5E8F91', '0C13EC1D9', '05EF96537', '03948BA8F', '0D19FB394', '0BF3BD96C',
                                               '0D3665974', '0BBDF91E9', '0A6083B64', '0D76EF8EC', '096CD1830', '04000DE73',
                                               '025C442BA', '0FD6CAA0A', '06CC18905', '0998DDE00', '02BAACDC4', '0D58264FC',
                                               '0CB8911AA', '0CF9E0BDC', '007B7F82F', '0948FD17A', '058BB08DB', '02EDBE8CA',
                                               '0D6F02EFD', '09C9797FB', '0F8CB3DA5', '0C2825430', '038BE7E61', '03F69C0F5',
                                               '07EB08903', '0917C741D', '0D01FEE8F', '01B09A600', '0BD197525', '06B6A2E60',
                                               '0B72DEF61', '095B17373', '0B6E0EEB1', '0078B3053', '08BD9D53F', '01995361F',
                                               '0F0B50CAE', '0B5D2887E', '004EB658C', '0D2C77EDB', '07221E24D', '0E8A4CC90',
                                               '00E947367', '0DBE190BB', '0D8726592', '06C02D59D', '0462B8BC6', '0F85122F8',
                                               '0FA1961EB', '035230553', '04CDFB216', '0356DB0AD', '0FD947DA3', '053BB206F',
                                               '0D1772CC1', '00DB759F5', '072FB4E7A', '0B47CB62D', '0616B627F', '0F3E153BC',
                                               '0F3AC7DEE', '01286192B', '009F3C478', '07D89E83E', '007CAFDE6', '0ABC9E80B',
                                               '091D1CDA5', '0BFC208A1', '0957D4C84', '00AAF260A', '09CF00D7C', '0D1C66C72',
                                               '0EA20CA23', '07D6BE324', '05B264527', '0D48C41F6', '081E31BF5', '0A1DC7455',
                                               '07BB493D8', '050036F1B', '00E73A1EC', '0C2D93CC0', '0FF47B30C', '0313062DE',
                                               '0E1BEFA3F', '0A24D069F', '02A984386', '0367F7405']

        
        self.num_fp = 0
        # Now we check the signatures of the passwords
        for item in passwords_not_in_passwords_csv_file:
            a = self.hash_functions(item)
            if all(self.hash_filter[i] == 1 for i in a):
                # print(f"{item} is probably in the filter")
                self.num_fp += 1
            else:
                # print(f"{item} is not in the filter")
                continue


if __name__ == '__main__':
    bloom = BloomFilter()
    # Reading the parameters
    bloom.read_parameters()
    bloom.set_self_variables()
    # bloom.print_self()



    # Reading the data for initial run
    print("Stream reading...")
    data_file = (data_main_directory /
                 parameters_dictionary['data']).with_suffix('.csv')

    # Possible to do input "break_after = (int)" to stop after x passwords
    passwords_read, times_sum = bloom.read_data(data_file)

    print(passwords_read, "passwords were read and processed in average", times_sum / passwords_read,
          "sec per password\n")

    bloom.count_fp()
    bloom.print_self()
    print(
        f"Number of false positives: {bloom.num_fp} with values of h: {bloom.h} and N: {bloom.N}")
    
    
    # Now we test with parameters from the assignment, task 3
    
    test_h = [1, 2, 3, 5, 10]
    
    print("\n\n" + Fore.YELLOW + Back.BLUE + f"Running tests for task 3 in the report")
    print(f"Testing for different values of h: {test_h}"+ Style.RESET_ALL + "\n")
    t1 = time.time()
    for i in test_h:
        bloom.read_parameters()
        bloom.set_self_variables(h = i)
        passwords_read, times_sum = bloom.read_data(data_file)
        print(passwords_read, "passwords were read and processed in average", times_sum / passwords_read,
          "sec per password\n")
        
        bloom.count_fp()
        print(
            f"Number of false positives: {bloom.num_fp} with values of h: {bloom.h} and N: {bloom.N}")
    t2 = time.time()
    # Now we test with parameters from the assignment, task 4
    print("\n\n" + Fore.YELLOW + Back.BLUE + f"Task 3 is done! It was done in {t2 - t1} seconds")
    
    test_N = [100000, 200000, 300000, 500000, 1000000]
    print(f"Running tests for task 4 in the report")
    print(f"Testing for different values of N: {test_N}" + Style.RESET_ALL + "\n")
    
    
    t3  = time.time()
    for i in test_N:
        bloom.read_parameters()
        bloom.set_self_variables(n = i)

        passwords_read, times_sum = bloom.read_data(data_file)
        print(passwords_read, "passwords were read and processed in average", times_sum / passwords_read,
          "sec per password\n")
        
        bloom.count_fp()
        print(
            f"Number of false positives: {bloom.num_fp} with values of h = {bloom.h} and N = {bloom.N}")
        
    t4 = time.time()
    print(f"Task 4 is done! It was done in {t4 - t3} seconds")
