import struct
from collections.abc import Callable
from dataclasses import dataclass
from fractions import Fraction
from typing import TypeVar

VALID_BASES = (2, 8, 10, 16)
DIGITS = "0123456789ABCDEF"
MAX_FRAC_DIGITS = 48


def int_to_base(n: int, base: int) -> str:
    if base == 10:
        return str(n)
    if n == 0:
        return "0"
    sign = ""
    if n < 0:
        sign = "-"
        n = -n
    parts = []
    while n:
        n, rem = divmod(n, base)
        parts.append(DIGITS[rem])
    return sign + "".join(reversed(parts))


def parse_in_base(s: str, base: int) -> int | None:
    s = s.strip()
    if not s:
        return None
    try:
        return int(s, base)
    except ValueError:
        return None


def parse_rational_in_base(s: str, base: int) -> Fraction | None:
    s = s.strip()
    if not s or "." not in s:
        return None

    sign = 1
    if s[0] in "+-":
        if s[0] == "-":
            sign = -1
        s = s[1:].strip()
        if not s:
            return None

    parts = s.split(".")
    if len(parts) != 2:
        return None

    int_s, frac_s = parts
    if not int_s and not frac_s:
        return None

    try:
        int_val = int(int_s or "0", base)
    except ValueError:
        return None

    frac_val = Fraction(0)
    for i, ch in enumerate(frac_s, start=1):
        try:
            d = int(ch, base)
        except ValueError:
            return None
        if d >= base:
            return None
        frac_val += Fraction(d, base**i)

    return sign * (int_val + frac_val)


def fractional_to_base(frac: Fraction, base: int, max_digits: int) -> tuple[str, bool]:
    """Expand fractional part in (0, 1). Returns (digit string, exact)."""
    if frac == 0:
        return "", True

    digits: list[str] = []
    f = frac
    for _ in range(max_digits):
        f *= base
        d = f.numerator // f.denominator
        digits.append(DIGITS[d])
        f -= d
        if f == 0:
            return "".join(digits), True
    return "".join(digits), False


def rational_to_base(value: Fraction, base: int, max_frac_digits: int = MAX_FRAC_DIGITS) -> str:
    if value == 0:
        return "0"

    sign = ""
    if value < 0:
        sign = "-"
        value = -value

    int_part = value.numerator // value.denominator
    frac = value - int_part

    if frac == 0:
        return sign + int_to_base(int_part, base)

    int_str = int_to_base(int_part, base) if int_part != 0 else "0"
    frac_str, exact = fractional_to_base(frac, base, max_frac_digits)
    suffix = "" if exact else "..."
    return sign + int_str + "." + frac_str + suffix


def prompt_base(prompt: str, exclude: int | None = None) -> int | None:
    while True:
        print("2. Binary")
        print("8. Octal")
        print("10. Decimal")
        print("16. Hexadecimal")
        print("x. Back / exit this step")
        choice = input(prompt).strip()
        if choice.lower() == "x":
            return None
        try:
            base = int(choice)
        except ValueError:
            print("Invalid choice. Enter 2, 8, 10, or 16.")
            continue
        if base not in VALID_BASES:
            print("Invalid choice. Enter 2, 8, 10, or 16.")
            continue
        if exclude is not None and base == exclude:
            print("Target base must differ from source base. Choose again.")
            continue
        return base


T = TypeVar("T")


def prompt_validated_input(
    prompt: str,
    parse_fn: Callable[[str], T | None],
    invalid_message: str,
) -> tuple[str, T] | None:
    while True:
        raw = input(prompt).strip()
        if raw.lower() == "x":
            return None
        parsed = parse_fn(raw)
        if parsed is None:
            print(invalid_message)
            continue
        return raw, parsed


def parse_decimal_number(s: str) -> float | None:
    s = s.strip()
    if not s:
        return None
    if "." in s:
        value = parse_rational_in_base(s, 10)
        if value is None:
            return None
        return float(value)
    int_val = parse_in_base(s, 10)
    if int_val is None:
        return None
    return float(int_val)


def parse_ieee754_single_bits(s: str) -> int | None:
    compact = s.strip().replace(" ", "").replace("_", "")
    if not compact:
        return None
    lower = compact.lower()
    if lower.startswith("0b"):
        compact = compact[2:]
    elif lower.startswith("0x"):
        compact = compact[2:]
        if len(compact) != 8:
            return None
        try:
            bits = int(compact, 16)
        except ValueError:
            return None
        if bits < 0 or bits > 0xFFFFFFFF:
            return None
        return bits

    if len(compact) == 8 and all(ch in "0123456789ABCDEFabcdef" for ch in compact):
        try:
            bits = int(compact, 16)
        except ValueError:
            return None
        return bits

    if len(compact) != 32 or any(ch not in "01" for ch in compact):
        return None
    return int(compact, 2)


def float_to_ieee754_single_bits(value: float) -> int:
    return struct.unpack(">I", struct.pack(">f", value))[0]


def ieee754_single_bits_to_float(bits: int) -> float:
    return struct.unpack(">f", struct.pack(">I", bits & 0xFFFFFFFF))[0]


def format_ieee754_single(bits: int) -> str:
    binary = f"{bits:032b}"
    sign, exponent, fraction = binary[0], binary[1:9], binary[9:]
    hex_repr = f"0x{bits:08X}"
    return (
        f"{sign} {exponent} {fraction} (32-bit, sign / exponent / fraction); hex {hex_repr}"
    )


def parse_non_negative_decimal_int(s: str) -> int | None:
    value = parse_in_base(s.strip(), 10)
    if value is None or value < 0:
        return None
    return value


def decimal_to_bcd(n: int) -> str:
    digits = str(n)
    return " ".join(f"{int(d):04b}" for d in digits)


def parse_bcd_bits(s: str) -> int | None:
    compact = s.strip().replace(" ", "").replace("_", "")
    if not compact:
        return None
    if compact.lower().startswith("0b"):
        compact = compact[2:]
    if not compact or len(compact) % 4 != 0:
        return None
    if any(ch not in "01" for ch in compact):
        return None

    digits: list[str] = []
    for i in range(0, len(compact), 4):
        nibble = int(compact[i : i + 4], 2)
        if nibble > 9:
            return None
        digits.append(str(nibble))
    return int("".join(digits))


def format_bcd(n: int) -> str:
    return f"{decimal_to_bcd(n)} (8421 BCD, one 4-bit digit per decimal digit)"


def binary_to_gray(binary: str) -> str:
    bits = binary.replace(" ", "")
    if not bits:
        return ""
    gray = [bits[0]]
    for i in range(1, len(bits)):
        gray.append("1" if int(bits[i]) ^ int(bits[i - 1]) else "0")
    return "".join(gray)


def gray_to_binary(gray: str) -> str:
    bits = gray.replace(" ", "")
    if not bits:
        return ""
    binary = [bits[0]]
    for i in range(1, len(bits)):
        binary.append("1" if int(bits[i]) ^ int(binary[-1]) else "0")
    return "".join(binary)


def parse_binary_bits(s: str) -> str | None:
    compact = s.strip().replace(" ", "").replace("_", "")
    if not compact:
        return None
    if compact.lower().startswith("0b"):
        compact = compact[2:]
    if not compact or any(ch not in "01" for ch in compact):
        return None
    return compact


def parse_gray_bits(s: str) -> str | None:
    return parse_binary_bits(s)


def parse_gray_to_binary(raw: str) -> str | None:
    gray = parse_gray_bits(raw)
    if gray is None:
        return None
    return gray_to_binary(gray)


MAX_FIXED_WIDTH = 64


@dataclass(frozen=True)
class FixedPointFormat:
    signed: bool
    a: int
    b: int

    @property
    def width(self) -> int:
        return self.a + self.b

    def label(self) -> str:
        kind = "Q" if self.signed else "U"
        return f"{kind}{self.a}.{self.b}"


def parse_non_negative_int(s: str) -> int | None:
    value = parse_in_base(s.strip(), 10)
    if value is None or value < 0:
        return None
    return value


def parse_decimal_fraction(s: str) -> Fraction | None:
    s = s.strip()
    if not s:
        return None
    if "." in s:
        return parse_rational_in_base(s, 10)
    value = parse_in_base(s, 10)
    if value is None:
        return None
    return Fraction(value)


def fraction_round_to_int(value: Fraction) -> int:
    if value >= 0:
        n, d = value.numerator, value.denominator
        return (n + d // 2) // d
    n, d = (-value).numerator, (-value).denominator
    return -((n + d // 2) // d)


def twos_complement_to_int(raw: int, width: int) -> int:
    mask = (1 << width) - 1
    raw &= mask
    sign_bit = 1 << (width - 1)
    if raw & sign_bit:
        return raw - (1 << width)
    return raw


def int_to_twos_complement(value: int, width: int) -> int:
    return value & ((1 << width) - 1)


def fixed_raw_in_range(raw: int, fmt: FixedPointFormat) -> bool:
    width = fmt.width
    if fmt.signed:
        return -(1 << (width - 1)) <= raw < (1 << (width - 1))
    return 0 <= raw < (1 << width)


def decimal_to_fixed_raw(value: Fraction, fmt: FixedPointFormat) -> int | None:
    if not fmt.signed and value < 0:
        return None
    scaled = value * (2**fmt.b)
    raw = fraction_round_to_int(scaled)
    if not fixed_raw_in_range(raw, fmt):
        return None
    return raw


def fixed_raw_to_fraction(raw: int, fmt: FixedPointFormat) -> Fraction:
    if fmt.signed:
        signed = twos_complement_to_int(raw, fmt.width)
        return Fraction(signed, 2**fmt.b)
    return Fraction(raw, 2**fmt.b)


def parse_fixed_point_bits(s: str, width: int) -> int | None:
    compact = s.strip().replace(" ", "").replace("_", "")
    if not compact:
        return None
    lower = compact.lower()
    hex_width = (width + 3) // 4

    if lower.startswith("0b"):
        compact = compact[2:]
    elif lower.startswith("0x"):
        compact = compact[2:]
        if len(compact) != hex_width:
            return None
        try:
            bits = int(compact, 16)
        except ValueError:
            return None
        if bits < 0 or bits >= (1 << width):
            return None
        return bits

    if len(compact) == hex_width and all(
        ch in "0123456789ABCDEFabcdef" for ch in compact
    ):
        try:
            bits = int(compact, 16)
        except ValueError:
            return None
        if bits >= (1 << width):
            return None
        return bits

    if len(compact) != width or any(ch not in "01" for ch in compact):
        return None
    return int(compact, 2)


def format_fixed_point(bits: int, fmt: FixedPointFormat) -> str:
    width = fmt.width
    binary = f"{bits & ((1 << width) - 1):0{width}b}"
    hex_width = (width + 3) // 4
    hex_repr = f"0x{bits & ((1 << width) - 1):0{hex_width}X}"
    return f"{binary} ({fmt.label()}, {width}-bit); hex {hex_repr}"


def prompt_fixed_point_format() -> FixedPointFormat | None:
    while True:
        print("U. Unsigned fixed point (Ua.b)")
        print("Q. Signed fixed point (Qa.b, two's complement)")
        print("x. Back / exit this step")
        kind = input("Select format (U or Q): ").strip()
        if kind.lower() == "x":
            return None
        upper = kind.upper()
        if upper not in ("U", "Q"):
            print("Invalid choice. Enter U, Q, or x.")
            continue

        signed = upper == "Q"
        a_entry = prompt_validated_input(
            "Enter a (integer bits): ",
            parse_non_negative_int,
            "Invalid a. Enter a non-negative integer.",
        )
        if a_entry is None:
            continue
        _, a = a_entry

        b_entry = prompt_validated_input(
            "Enter b (fractional bits): ",
            parse_non_negative_int,
            "Invalid b. Enter a non-negative integer.",
        )
        if b_entry is None:
            continue
        _, b = b_entry

        width = a + b
        if width < 1:
            print("Invalid format: a + b must be at least 1.")
            continue
        if width > MAX_FIXED_WIDTH:
            print(f"Invalid format: total width a + b must be at most {MAX_FIXED_WIDTH}.")
            continue
        if signed and a < 1:
            print("Invalid format: Qa.b requires a >= 1 (sign included in integer bits).")
            continue

        return FixedPointFormat(signed=signed, a=a, b=b)


def call_fixed_point_conversion():
    fmt = prompt_fixed_point_format()
    if fmt is None:
        return

    encoding = "two's complement" if fmt.signed else "unsigned"
    print(
        f"Fixed point {fmt.label()} ({fmt.width}-bit, {encoding}): "
        f"{fmt.a} integer bit(s), {fmt.b} fractional bit(s); "
        f"binary point after the {fmt.b} least significant bit(s)."
    )

    width = fmt.width
    hex_width = (width + 3) // 4

    while True:
        print("1. Decimal -> fixed point binary")
        print("2. Fixed point binary -> decimal")
        print("x. Back / exit this step")
        direction = input("Select conversion direction: ").strip()
        if direction.lower() == "x":
            return
        if direction not in ("1", "2"):
            print("Invalid choice. Enter 1, 2, or x.")
            continue

        if direction == "1":
            if fmt.signed:
                invalid_decimal = (
                    "Invalid input. Enter a decimal in range for "
                    f"{fmt.label()}, representable with {fmt.b} fractional bits."
                )
            else:
                invalid_decimal = (
                    "Invalid input. Enter a non-negative decimal in range for "
                    f"{fmt.label()}, representable with {fmt.b} fractional bits."
                )

            def parse_decimal_to_fixed(raw: str) -> int | None:
                value = parse_decimal_fraction(raw)
                if value is None:
                    return None
                raw_int = decimal_to_fixed_raw(value, fmt)
                if raw_int is None:
                    return None
                return int_to_twos_complement(raw_int, width)

            print(
                "Enter a decimal number (integer or decimal). "
                "Enter x to go back."
            )
            while True:
                entry = prompt_validated_input(
                    "Decimal: ",
                    parse_decimal_to_fixed,
                    invalid_decimal,
                )
                if entry is None:
                    break
                raw, bits = entry
                print(f"{raw} -> {format_fixed_point(bits, fmt)}")
        else:
            invalid_bits = (
                f"Invalid input. Use {width} binary digits, "
                f"{hex_width} hex digits, or 0x-prefixed hex."
            )

            def parse_bits(raw: str) -> int | None:
                return parse_fixed_point_bits(raw, width)

            print(
                f"Enter {fmt.label()} as {width} binary digits, "
                f"{hex_width} hex digits, or 0x-prefixed hex. Enter x to go back."
            )
            while True:
                entry = prompt_validated_input(
                    "Fixed point: ",
                    parse_bits,
                    invalid_bits,
                )
                if entry is None:
                    break
                raw, bits = entry
                value = fixed_raw_to_fraction(bits, fmt)
                print(f"{raw} -> {value} ({format_fixed_point(bits, fmt)})")


def call_ieee754_single_conversion():
    print(
        "IEEE 754 single precision (32-bit: 1 sign bit, 8 exponent bits, 23 fraction bits)."
    )
    while True:
        print("1. Decimal -> IEEE 754 single precision")
        print("2. IEEE 754 single precision -> decimal")
        print("x. Back / exit this step")
        direction = input("Select conversion direction: ").strip()
        if direction.lower() == "x":
            return
        if direction not in ("1", "2"):
            print("Invalid choice. Enter 1, 2, or x.")
            continue

        if direction == "1":
            print(
                "Enter a decimal number (integer or decimal). "
                "Enter x to go back."
            )
            while True:
                entry = prompt_validated_input(
                    "Decimal: ",
                    parse_decimal_number,
                    "Invalid input. Enter a valid decimal integer or decimal fraction.",
                )
                if entry is None:
                    break
                raw, value = entry
                bits = float_to_ieee754_single_bits(value)
                print(f"{raw} -> {format_ieee754_single(bits)}")
        else:
            print(
                "Enter IEEE 754 single precision as 32 binary digits, "
                "8 hex digits, or 0x-prefixed hex. Enter x to go back."
            )
            while True:
                entry = prompt_validated_input(
                    "IEEE 754 single: ",
                    parse_ieee754_single_bits,
                    "Invalid input. Use 32 bits (0/1), 8 hex digits, or 0x........",
                )
                if entry is None:
                    break
                raw, bits = entry
                value = ieee754_single_bits_to_float(bits)
                print(f"{raw} -> {value} ({format_ieee754_single(bits)})")


def call_bcd_conversion():
    print("Binary coded decimal (8421 BCD): each decimal digit is encoded in 4 bits (0–9 per nibble).")
    while True:
        print("1. Decimal -> BCD")
        print("2. BCD -> decimal")
        print("x. Back / exit this step")
        direction = input("Select conversion direction: ").strip()
        if direction.lower() == "x":
            return
        if direction not in ("1", "2"):
            print("Invalid choice. Enter 1, 2, or x.")
            continue

        if direction == "1":
            print(
                "Enter a non-negative decimal integer. "
                "Enter x to go back."
            )
            while True:
                entry = prompt_validated_input(
                    "Decimal: ",
                    parse_non_negative_decimal_int,
                    "Invalid input. Enter a non-negative decimal integer.",
                )
                if entry is None:
                    break
                raw, value = entry
                print(f"{raw} -> {format_bcd(value)}")
        else:
            print(
                "Enter BCD as groups of 4 binary digits per decimal digit "
                "(spaces optional), or 0b-prefixed bits. Enter x to go back."
            )
            while True:
                entry = prompt_validated_input(
                    "BCD: ",
                    parse_bcd_bits,
                    "Invalid input. Use only 0/1, length a multiple of 4, each nibble 0000–1001.",
                )
                if entry is None:
                    break
                raw, value = entry
                print(f"{raw} -> {value} ({format_bcd(value)})")


def call_gray_code_conversion():
    print(
        "Gray code (binary reflected): adjacent codewords differ by one bit; "
        "convert between binary and Gray bit strings (bit width preserved)."
    )
    while True:
        print("1. Binary -> Gray code")
        print("2. Gray code -> binary")
        print("x. Back / exit this step")
        direction = input("Select conversion direction: ").strip()
        if direction.lower() == "x":
            return
        if direction not in ("1", "2"):
            print("Invalid choice. Enter 1, 2, or x.")
            continue

        if direction == "1":
            print(
                "Enter binary digits (spaces or 0b prefix optional). "
                "Enter x to go back."
            )
            while True:
                entry = prompt_validated_input(
                    "Binary: ",
                    parse_binary_bits,
                    "Invalid input. Enter a valid binary bit string (0/1 only).",
                )
                if entry is None:
                    break
                raw, binary = entry
                gray = binary_to_gray(binary)
                print(f"{raw} -> {gray} (Gray code)")
        else:
            print(
                "Enter Gray code as binary digits (spaces or 0b prefix optional). "
                "Enter x to go back."
            )
            while True:
                entry = prompt_validated_input(
                    "Gray code: ",
                    parse_gray_to_binary,
                    "Invalid input. Enter a valid Gray code bit string (0/1 only).",
                )
                if entry is None:
                    break
                raw, binary = entry
                print(f"{raw} -> {binary} (binary)")


def call_base_conversion():
    from_base = prompt_base("Select source base (from): ")
    if from_base is None:
        return

    to_base = prompt_base("Select target base (to): ", exclude=from_base)
    if to_base is None:
        return

    print(
        f"Converting from base {from_base} to base {to_base}. "
        f"Enter integers or decimals (non-terminating fractions end with ...). "
        f"Enter x to exit."
    )
    invalid_msg = "Invalid input. Enter a valid integer or decimal for the selected base."

    def parse_number_in_from_base(raw: str) -> str | None:
        if "." in raw:
            value = parse_rational_in_base(raw, from_base)
            if value is None:
                return None
            return rational_to_base(value, to_base)
        value = parse_in_base(raw, from_base)
        if value is None:
            return None
        return int_to_base(value, to_base)

    while True:
        entry = prompt_validated_input(
            f"Enter a number in base {from_base}: ",
            parse_number_in_from_base,
            invalid_msg,
        )
        if entry is None:
            return
        raw, result = entry
        print(f"{raw} (base {from_base}) -> {result} (base {to_base})")


if __name__ == "__main__":
    while True:
        print("1. Base conversion (integers or decimals)")
        print("2. Fixed point conversion")
        print("3. Floating point conversion (IEEE 754 single precision)")
        print("4. Binary coded decimal (BCD)")
        print("5. Gray code")
        print("x. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            call_base_conversion()
        elif choice == "2":
            call_fixed_point_conversion()
        elif choice == "3":
            call_ieee754_single_conversion()
        elif choice == "4":
            call_bcd_conversion()
        elif choice == "5":
            call_gray_code_conversion()
        elif choice.lower() == "x":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
