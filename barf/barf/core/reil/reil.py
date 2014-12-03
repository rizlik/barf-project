"""
This module contains all the classes that handle the intermediate
representation language. It is basically the REIL language with minor
changes. Below there is an overview of the REIL language and its
instruction format. For full details see "REIL: A platform-independent
intermediate representation of disassembled code for static code
analysis."

All algorithms within the framework are designed to operate on the
intermediate representation. This provides great flexibility when it
comes to implement a cross-platform framework.

Instruction Format
------------------

    mnemonic oprnd1, oprnd2, oprnd3

Instructions
------------

    Arithmetic    : ADD, SUB, MUL, DIV, MOD, BSH
    Bitwise       : AND, OR, XOR
    Data Transfer : LDM, STM, STR
    Conditional   : BISZ, JCC
    Other         : UNDEF, UNKN, NOP

"""

# Display operands size in intruction
show_size = True

class ReilMnemonic(object):

    """Enumeration of IR mnemonics.
    """

    # Arithmetic Instructions
    ADD   = 1
    SUB   = 2
    MUL   = 3
    DIV   = 4
    MOD   = 5
    BSH   = 6

    # Bitwise Instructions
    AND   = 7
    OR    = 8
    XOR   = 9

    # Data Transfer Instructions
    LDM   = 10
    STM   = 11
    STR   = 12

    # Conditional Instructions
    BISZ  = 13
    JCC   = 14

    # Other Instructions
    UNKN  = 15
    UNDEF = 16
    NOP   = 17

    # Added Instructions
    RET   = 18

    @staticmethod
    def to_string(mnemonic):
        """Return the string representation of the given mnemonic.
        """
        strings = {
            # Arithmetic Instructions
            ReilMnemonic.ADD : "add",
            ReilMnemonic.SUB : "sub",
            ReilMnemonic.MUL : "mul",
            ReilMnemonic.DIV : "div",
            ReilMnemonic.MOD : "mod",
            ReilMnemonic.BSH : "bsh",

            # Bitwise Instructions
            ReilMnemonic.AND : "and",
            ReilMnemonic.OR : "or",
            ReilMnemonic.XOR : "xor",

            # Data Transfer Instructions
            ReilMnemonic.LDM : "ldm",
            ReilMnemonic.STM : "stm",
            ReilMnemonic.STR : "str",

            # Conditional Instructions
            ReilMnemonic.BISZ : "bisz",
            ReilMnemonic.JCC : "jcc",

            # Other Instructions
            ReilMnemonic.UNKN  : "unkn" ,
            ReilMnemonic.UNDEF : "undef" ,
            ReilMnemonic.NOP : "nop" ,

            # Added Instructions
            ReilMnemonic.RET : "ret",
        }

        return strings[mnemonic]

    @staticmethod
    def from_string(string):
        """Return the mnemonic represented by the given string.
        """
        mnemonics = {
            # Arithmetic Instructions
            "add" : ReilMnemonic.ADD,
            "sub" : ReilMnemonic.SUB,
            "mul" : ReilMnemonic.MUL,
            "div" : ReilMnemonic.DIV,
            "mod" : ReilMnemonic.MOD,
            "bsh" : ReilMnemonic.BSH,

            # Bitwise Instructions
            "and" : ReilMnemonic.AND,
            "or" : ReilMnemonic.OR,
            "xor" : ReilMnemonic.XOR,

            # Data Transfer Instructions
            "ldm" : ReilMnemonic.LDM,
            "stm" : ReilMnemonic.STM,
            "str" : ReilMnemonic.STR,

            # Conditional Instructions
            "bisz" : ReilMnemonic.BISZ,
            "jcc" : ReilMnemonic.JCC,

            # Other Instructions
            "unkn" : ReilMnemonic.UNKN,
            "undef" : ReilMnemonic.UNDEF,
            "nop" : ReilMnemonic.NOP,

            # Added Instructions
            "ret" : ReilMnemonic.RET,
        }

        return mnemonics[string]


REIL_MNEMONICS = (
    # Arithmetic Instructions
    ReilMnemonic.ADD,
    ReilMnemonic.SUB,
    ReilMnemonic.MUL,
    ReilMnemonic.DIV,
    ReilMnemonic.MOD,
    ReilMnemonic.BSH,

    # Bitwise Instructions
    ReilMnemonic.AND,
    ReilMnemonic.OR,
    ReilMnemonic.XOR,

    # Data Transfer Instructions
    ReilMnemonic.LDM,
    ReilMnemonic.STM,
    ReilMnemonic.STR,

    # Conditional Instructions
    ReilMnemonic.BISZ,
    ReilMnemonic.JCC,

    # Other Instructions
    ReilMnemonic.UNKN,
    ReilMnemonic.UNDEF,
    ReilMnemonic.NOP,

    # Added Instructions
    ReilMnemonic.RET,
)

class ReilInstruction(object):

    """Representation of a REIL instruction.
    """


    def __init__(self):

        # A REIL mnemonic
        self._mnemonic = None

        # A list of operand. Exactly 3.
        self._operands = [ReilEmptyOperand()] * 3

        # Optionally, a comment for the instruction.
        self._comment = None

        # A REIL address for the instruction.
        self._address = None

    @property
    def mnemonic(self):
        """Get instruction mnemonic.
        """
        return self._mnemonic

    @mnemonic.setter
    def mnemonic(self, value):
        """Set instruction mnemonic.
        """
        if value not in REIL_MNEMONICS:
            raise Exception("Invalid instruction mnemonic : %s" % str(value))

        self._mnemonic = value

    @property
    def operands(self):
        """Get instruction operands.
        """
        return self._operands

    @operands.setter
    def operands(self, value):
        """Set instruction operands.
        """
        if len(value) != 3:
            raise Exception("Invalid instruction operands : %s" % str(value))

        self._operands = value

    @property
    def address(self):
        """Get instruction address.
        """
        return self._address

    @address.setter
    def address(self, value):
        """Set instruction address.
        """
        self._address = value

    @property
    def comment(self):
        """Get instruction comment.
        """
        return self._comment

    @comment.setter
    def comment(self, value):
        """Set instruction comment.
        """
        self._comment = value

    def __str__(self):
        def print_oprnd(oprnd):
            oprnd_str = str(oprnd)
            size_str = str(oprnd.size) if oprnd.size else ""

            sizes = {
                128 : "DQWORD",
                72  : "POINTER",
                64  : "QWORD",
                40  : "POINTER",
                32  : "DWORD",
                16  : "WORD",
                8   : "BYTE",
                1   : "BIT",
                ""  : "UNK",
            }

            if isinstance(oprnd, ReilEmptyOperand):
                return "%s" % (oprnd_str)
            else:
                return "%s %s" % (sizes[oprnd.size if oprnd.size else ""], oprnd_str)

        mnemonic_str = ReilMnemonic.to_string(self._mnemonic)

        if show_size:
            operands_str = ", ".join(map(print_oprnd, self._operands))
        else:
            operands_str = ", ".join(map(str, self._operands))

        return "%-5s [%s]" % (mnemonic_str, operands_str)


class ReilOperand(object):

    """Representation of an IR instruction's operand.
    """


    def __init__(self, size):

        # Size of the operand, in bits.
        self._size = size

        # The tag attribute is used for instruction translation. It is
        # set by ReilParser and used at the moment of a translation
        # instantiation. For more detail, see arch/x86/x86translator.py
        self._tag = None

    def __eq__(self, other):
        """Return self == other.
        """
        return type(other) is type(self) and self._size == other._size

    def __ne__(self, other):
        """Return self != other.
        """
        return not self.__eq__(other)

    @property
    def size(self):
        """Get operand size.
        """
        return self._size

    @size.setter
    def size(self, value):
        """Set operand size.
        """
        self._size = value

    @property
    def tag(self):
        """Get operand tag.
        """
        return self._tag

    @tag.setter
    def tag(self, value):
        """Set operand tag.
        """
        self._tag = value


class ReilImmediateOperand(ReilOperand):

    """Representation of a REIL instruction immediate operand.
    """


    def __init__(self, immediate, size=None):
        super(ReilImmediateOperand, self).__init__(size)

        if type(immediate) != int and type(immediate) != long:
            raise Exception("Invalid type : %s" % type(immediate))

        # Immediate value in two's complement representation.
        if self._size:
            self._immediate = (immediate if immediate >= 0 else 2**self._size -(-immediate))
        else:
            self._immediate = (immediate if immediate >= 0 else 2**32 -(-immediate))

    @property
    def immediate(self):
        """Get immediate.
        """
        return self._immediate

    @immediate.setter
    def immediate(self, value):
        """Set immediate.
        """
        self._immediate = value

    def __str__(self):
        """Return string representation of the operand.
        """
        if self._size:
            rv = hex(self._immediate & (2**self._size-1))
        else:
            rv = hex(self._immediate & (2**32-1))

        return rv if rv[-1] != 'L' else rv[:-1]

    def __eq__(self, other):
        """Return self == other.
        """
        return type(other) is type(self) and \
            self._size == other._size and \
            self._immediate == other._immediate


class ReilRegisterOperand(ReilOperand):

    """Representation of a REIL instruction register operand.
    """


    def __init__(self, name, size=None):
        super(ReilRegisterOperand, self).__init__(size)

        # Register name.
        self._name = name

    @property
    def name(self):
        """Get IR register operand name.
        """
        return self._name

    @name.setter
    def name(self, value):
        """Set IR register operand name.
        """
        self._name = value

    def __str__(self):
        """Return string representation of the operand.
        """
        return self._name

    def __eq__(self, other):
        """Return self == other.
        """
        return type(other) is type(self) and \
            self._size == other._size and \
            self._name == other._name


class ReilEmptyOperand(ReilRegisterOperand):

    """Representation of an IR instruction's empty operand.
    """

    def __init__(self):
        super(ReilEmptyOperand, self).__init__("EMPTY", size=None)


class ReilInstructionBuilder(object):

    """REIL Instruction Builder. Generate REIL instructions, easily.
    """

    # Arithmetic Instructions
    # ======================================================================== #
    def gen_add(self, src1, src2, dst):
        """Return an ADD instruction.
        """
        return self.build(ReilMnemonic.ADD, src1, src2, dst)

    def gen_sub(self, src1, src2, dst):
        """Return a SUB instruction.
        """
        return self.build(ReilMnemonic.SUB, src1, src2, dst)

    def gen_mul(self, src1, src2, dst):
        """Return a MUL instruction.
        """
        return self.build(ReilMnemonic.MUL, src1, src2, dst)

    def gen_div(self, src1, src2, dst):
        """Return a DIV instruction.
        """
        return self.build(ReilMnemonic.DIV, src1, src2, dst)

    def gen_mod(self, src1, src2, dst):
        """Return a MOD instruction.
        """
        return self.build(ReilMnemonic.MOD, src1, src2, dst)

    def gen_bsh(self, src1, src2, dst):
        """Return a BSH instruction.
        """
        return self.build(ReilMnemonic.BSH, src1, src2, dst)

    # Bitwise Instructions
    # ======================================================================== #
    def gen_and(self, src1, src2, dst):
        """Return an AND instruction.
        """
        return self.build(ReilMnemonic.AND, src1, src2, dst)

    def gen_or(self, src1, src2, dst):
        """Return an OR instruction.
        """
        return self.build(ReilMnemonic.OR, src1, src2, dst)

    def gen_xor(self, src1, src2, dst):
        """Return a XOR instruction.
        """
        return self.build(ReilMnemonic.XOR, src1, src2, dst)

    # Data Transfer Instructions
    # ======================================================================== #
    def gen_ldm(self, src, dst):
        """Return a LDM instruction.
        """
        return self.build(ReilMnemonic.LDM, src, ReilEmptyOperand(), dst)

    def gen_stm(self, src, dst):
        """Return a STM instruction.
        """
        return self.build(ReilMnemonic.STM, src, ReilEmptyOperand(), dst)

    def gen_str(self, src, dst):
        """Return a STR instruction.
        """
        return self.build(ReilMnemonic.STR, src, ReilEmptyOperand(), dst)

    # Conditional Instructions
    # ======================================================================== #
    def gen_bisz(self, src, dst):
        """Return a BISZ instruction.
        """
        return self.build(ReilMnemonic.BISZ, src, ReilEmptyOperand(), dst)

    def gen_jcc(self, src, dst):
        """Return a JCC instruction.
        """
        return self.build(ReilMnemonic.JCC, src, ReilEmptyOperand(), dst)

    # Other Instructions
    # ======================================================================== #
    def gen_unkn(self):
        """Return an UNKN instruction.
        """
        empty_reg = ReilEmptyOperand()

        return self.build(ReilMnemonic.UNKN, empty_reg, empty_reg, empty_reg)

    def gen_undef(self):
        """Return an UNDEF instruction.
        """
        empty_reg = ReilEmptyOperand()

        return self.build(ReilMnemonic.UNDEF, empty_reg, empty_reg, empty_reg)

    def gen_nop(self):
        """Return a NOP instruction.
        """
        empty_reg = ReilEmptyOperand()

        return self.build(ReilMnemonic.NOP, empty_reg, empty_reg, empty_reg)

    # Ad hoc Instructions
    # ======================================================================== #
    def gen_ret(self):
        """Return a RET instruction.
        """
        empty_reg = ReilEmptyOperand()

        return self.build(ReilMnemonic.RET, empty_reg, empty_reg, empty_reg)

    # Auxiliary functions
    # ======================================================================== #
    def build(self, mnemonic, oprnd1, oprnd2, oprnd3):
        """Return the specified instruction.
        """
        ins = ReilInstruction()

        ins.mnemonic = mnemonic
        ins.operands = [oprnd1, oprnd2, oprnd3]

        return ins


class DualInstruction(object):

    """Represents an assembler instruction paired with its IR
    representation.

    """


    def __init__(self, address, asm_instr, ir_instrs):

        # Address of the assembler instruction.
        self._address = address

        # Assembler instruction.
        self._asm_instr = asm_instr

        # REIL translation of the assembler instruction. Note that one
        # assemlber instruction is mapped to more than one REIL
        # instruction.
        self._ir_instrs = ir_instrs

    @property
    def address(self):
        """Get instruction address.
        """
        return self._address

    @property
    def asm_instr(self):
        """Get assembly instruction.
        """
        return self._asm_instr

    @property
    def ir_instrs(self):
        """Get IR representation of the assembly instruction.
        """
        return self._ir_instrs

    def __eq__(self, other):
        return self.address == other.address and \
            self.asm_instr == other.asm_instr

    def __ne__(self, other):
        """Return self != other.
        """
        return not self.__eq__(other)
