import json
import sys

class JSONFileException(Exception):
    pass

class Enigma:
    def __init__(self, hash_map, wheels, reflector_map):
        self.hash_map = hash_map
        self.rev_hash_map = {v: k for k, v in hash_map.items()}
        self.init_wheels = wheels[:]
        self.wheels = wheels[:]
        self.reflector_map = reflector_map
        self.counter = 0  
    def _encrypt_char(self, c):
        if c not in self.hash_map:
            return c

        i = self.hash_map[c]
        w1, w2, w3 = self.wheels

        temp = (2 * w1 - w2 + w3) % 26
        i = (i + (temp if temp != 0 else 1)) % 26

        c1 = self.rev_hash_map[i]
        c2 = self.reflector_map[c1]
        i = self.hash_map[c2]

        i = (i - (temp if temp != 0 else 1)) % 26
        c3 = self.rev_hash_map[i]

        self.counter += 1
        return c3

    def _update_wheels(self):
        self.wheels[0] = self.wheels[0] + 1 if self.wheels[0] < 8 else 1
        if self.counter % 2 == 0:
            self.wheels[1] *= 2
        else:
            self.wheels[1] -= 1

        if self.counter % 10 == 0:
            self.wheels[2] = 10
        elif self.counter % 3 == 0:
            self.wheels[2] = 5
        else:
            self.wheels[2] = 0

    def encrypt(self, message):
        encrypted = []
        self.wheels = self.init_wheels[:]  
        self.counter = 0
        for c in message:
            encrypted_char = self._encrypt_char(c)
            encrypted.append(encrypted_char)
            self._update_wheels()
        return ''.join(encrypted)

def load_enigma_from_path(path):
    try:
        with open(path, 'r') as f:
            config = json.load(f)
            return Enigma(config['hash_map'], config['wheels'], config['reflector_map'])
    except Exception:
        raise JSONFileException

def main():
    args = sys.argv[1:]
    if '-c' not in args or '-i' not in args:
        print("Usage: python3 enigma.py -c <config_file> -i <input_file> -o <output_file>", file=sys.stderr)
        exit(1)

    try:
        config_file = args[args.index('-c') + 1]
        input_file = args[args.index('-i') + 1]
        output_file = None
        if '-o' in args:
            output_file = args[args.index('-o') + 1]
    except Exception:
        print("Usage: python3 enigma.py -c <config_file> -i <input_file> -o <output_file>", file=sys.stderr)
        exit(1)

    try:
        enigma = load_enigma_from_path(config_file)

        with open(input_file, 'r') as infile:
            lines = infile.readlines()

        encrypted_lines = [enigma.encrypt(line.rstrip('\n')) for line in lines]

        if output_file:
            with open(output_file, 'w') as outfile:
                for line in encrypted_lines:
                    outfile.write(line + '\n')
        else:
            for line in encrypted_lines:
                print(line)

    except Exception:
        print("The enigma script has encountered an error", file=sys.stderr)
        exit(1)

if __name__ == '__main__':
    main()
