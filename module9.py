import unittest
import math

'''
TL;DR for those unacquainted with IPv4 subnetting:
There is a value, known as the CIDR prefix, associated with any given subnet. These look like /30 or /24, for example.
This number represents the number of 1's present when a subnet mask (255.255.255.0 for example) is converted to binary.
As these subnet masks can only be one of relatively few numbers, the binary conversion is easy to remember; 255 is eight
 1's. Therefore 255.255.255.0 has a CIDR prefix of /24. It's easy enough to calculate the number of usable hosts within 
 a given CIDR prefix; this is 2^(32-prefix) - 2. However calculating the most efficient CIDR prefix given the number of 
 hosts needed is not quite so simple, as you'll see in the code below.
 
'''


def get_most_efficient_subnet(hosts_needed):
    return math.floor((math.log(4294967296 / (hosts_needed + 2))) / (math.log(2)))


class SubnetTest(unittest.TestCase):
    def test(self):
        self.assertEqual(get_most_efficient_subnet(4), 29)
        self.assertEqual(get_most_efficient_subnet(439584), 13)
        self.assertEqual(get_most_efficient_subnet(1), 30)
        self.assertEqual(get_most_efficient_subnet(1073741760), 2)
        self.assertEqual(get_most_efficient_subnet(1073741822), 2)
