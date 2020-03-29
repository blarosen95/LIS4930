import itertools
import re
import pandas as pd


class Port:
    def __init__(self, port, con_type, status, speed, mode, name):
        self.issues = []
        self.full_port = port
        try:
            self.interface = re.search(r'[A-Z](?=\d+)', port, re.IGNORECASE).group(0)
        except AttributeError as e:
            self.interface = 'ZZZ'
            # The regex match could fail even with a valid interface, if the port number isn't matched in the lookahead
            self.issues.append('invalid port parameter')
        try:
            self.port = re.search(r'(?<=[A-Z])\d+', port, re.IGNORECASE).group(0)
        except AttributeError as e:
            self.port = '0'
            # The regex match could fail even with a valid port number, if the interface isn't matched in the lookbehind
            self.issues.append('invalid port parameter')
        self.type = con_type
        self.status = status
        self.speed = speed
        self.mode = mode
        self.name = name

    def __str__(self):
        return f'Full Port: {self.full_port}, Connection Type: {self.type}, Status: {self.status}, Speed: ' \
               f'{self.speed}, Duplex: {self.mode}, Custom Name: {self.name} '

    def diagnose_speed(self):
        if self.status != 'Up':
            return f'{self.full_port} is not up.'
        speed_num = re.search(r'\d+(?=\w+)', self.speed).group(0)
        duplex = re.search(r'[HF]D', self.speed).group(0)
        if duplex != 'FD' and self.mode == 'Auto':
            return f'Check for loose connection on {self.full_port}\'s cable.'
        is_gig = bool(re.search(r'Gig', self.speed))
        if self.type == 'SFP+SR':
            if speed_num == '10' and is_gig:
                return f'{self.full_port}: no issues found.'
            else:
                return f'{self.full_port} is not achieving 10Gb speed ({speed_num}Mb). Inspect the connectors with a ' \
                       f'videoscope, and clean as necessary if experiencing speed issues with device "{self.name}".'
        if self.type == '10GbE-T':
            if speed_num == '10' and is_gig:
                return f'{self.full_port}: no issues found.'
            else:
                return f'{self.full_port} is not achieving 10Gb speed ({speed_num}Mb). Be sure to use the right ' \
                       f'category of ethernet cable and consider its length. Also investigate the NIC on other end ' \
                       f'for maximum throughput specifications.'
        if self.type == '100/1000T':
            if speed_num == '1000':
                return f'{self.full_port}: no issues found.'
            else:
                return f'{self.full_port} is not achieving 1Gb speed ({speed_num}Mb). Be sure to use the right ' \
                       f'category of ethernet cable and consider its length. Also investigate the NIC on other end ' \
                       f'for maximum throughput specifications.'
        else:
            return f'Interface {self.interface} is of an unsupported type ({self.type}) for speed diagnostics.'


def initialize():
    port_frame = pd.read_csv("switch1.csv")
    ports = []

    for index, row in port_frame.iterrows():
        if index == 0:
            pass
        if None:
            pass
        ports.append(Port(row['Port'], row['Type'], row['Status'], row['Speed'], row['Config-mode'], row['Name']))
    return ports


def infinite_iterator(ports):
    for port in itertools.cycle(ports):
        diagnosis = port.diagnose_speed()
        if 'no issues found' in diagnosis:
            continue
        if 'is not up' not in diagnosis:
            print(f'Alert for device "{port.name}":')
            print(f'{diagnosis}\n')


def cycle_n_times(ports, n):
    for port in itertools.islice(itertools.cycle(ports), n):
        diagnosis = port.diagnose_speed()
        if 'no issues found' in diagnosis:
            continue
        if 'is not up' not in diagnosis:
            print(f'Alert for device "{port.name}":')
            print(f'{diagnosis}\n')


def repeat_n_times(ports, n):
    for port in itertools.chain.from_iterable(itertools.repeat(ports, n)):
        diagnosis = port.diagnose_speed()
        if 'no issues found' in diagnosis:
            print(f'{str(port)}\n')
            continue
        if 'is not up' not in diagnosis:
            print(f'Alert for device "{port.name}":')
            print(f'{diagnosis}\n')


# Below function is turned off with a comment to give other functions a chance to run (see blog for further explanation)
# infinite_iterator(initialize())

# Argument "n" needs to include the ones that aren't printed out in the function (count of rows - header = 1 cycle)
cycle_n_times(initialize(), 42)

print(f'{"-" * 100}\n')

# Argument "n" is merely the number of iterations, unlike in cycle_n_times
repeat_n_times(initialize(), 1)
