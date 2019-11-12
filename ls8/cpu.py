"""CPU functionality."""

import sys

HLT = 1
LDI = 130
PRN = 71
MUL = 162

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = bytearray(8)
        self.ram = [0] * 32
        self.pc = 0
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_HTL 
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL
        # debug flag for fun
        self.debug = False

    def load(self):
        """Load a program into memory."""
        # I thought I'd try argparse out, I wanted to be able to run this code with optional debug output. argparse gives us an easy way to do that, and gives us friendly -h output 
        # run python ls8.py -h, you'll see we have nice instructions on how to run ls8
        import argparse
        # initialize parser
        parser = argparse.ArgumentParser(description='Run a file in ls8')
        # create a required command line arg called file_dir with type string
        parser.add_argument('file_dir', type=str, help='Directory of file to run with ls8')
        # the -- lets the parser know this next argument is optional, and its action means debug=false when -d or --debug isn't supplied, and debug=true when ls8.py is run with -d or --debug. Since our arguments have different types (boolean and string) we can supply them in any order in the command line
        # either python `python ls8.py file_dir -d` or `python ls8.py -d file_dir` works now, or you can omit the flag altogether
        parser.add_argument('-d', '--debug', help='Run with --debug to run code with debug output', action="store_true")
        
        args = parser.parse_args()
        
        if (args.debug):
            self.debug = True
            
        # parse the file
        f = open(args.file_dir)
        program = []
        for line in f:
            if line[0] != '#' and len(line) > 0 and line != '\n':
                program.append(int(line[:8], 2))
        f.close()
        
        # load the program array into ram
        address = 0
        # For now, we've just hardcoded a program:
        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
        
    def ram_read(self, mar):
        return self.ram[mar]
    
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
        
    def run(self):
        """Run the CPU."""
        while True:
            command = self.ram[self.pc]
            if command in self.branchtable:
                self.branchtable[command]()
            else:
                print(f"Unknown command at {self.pc}")
                sys.exit(1)
                
    # OP HANDLERS FOR BRANCHTABLE
    def handle_HTL(self):
        if (self.debug):
            print(f'Exiting program at {self.pc}')
        sys.exit()
        
    def handle_LDI(self):
        operand_a = self.ram[self.pc + 1]
        operand_b = self.ram[self.pc + 2]
        if (self.debug):
            print(f'Storing {operand_b} at register[{operand_a}]')
        self.register[operand_a] = operand_b
        self.pc += 3
        
    def handle_PRN(self):
        operand = self.ram[self.pc + 1]
        if (self.debug):
            print(f'Printing from register[{operand}]')
        print(self.register[operand])
        self.pc += 2
        
    def handle_MUL(self):
        operand_a = self.ram[self.pc + 1]
        operand_b = self.ram[self.pc + 2]
        if (self.debug):
            print(f'Multiplying {self.register[operand_a]} and {self.register[operand_b]} and storing in register[{operand_a}]')
        self.register[operand_a] = (self.register[operand_a] * self.register[operand_b]) & 0xff
        self.pc += 3