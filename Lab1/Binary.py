from typing import Union

class Binary:
    BIN_1 = "00000001"
    BIN_0 = "00000000"
    BIT_SIZE_32 = 32
    BIT_SIZE_8 = 8
    BIN_SIZE_FRACTION = 20
    
    IEEE_754_FORMAT = {
        "END_SIGN_INDEX": 1,
        "END_POWER_INDEX": 9,
        "END_MANTISSA_INDEX": 32,
        "MANTISSA_LENGTH": 23
    }
    
    @staticmethod
    def intToBinary(number: int, signed: bool = True, to8Bit = True) -> str:
        if signed:
            if number < -128 or number > 127:
                raise ValueError("Значение выходит за пределы диапазона для 8-битного знакового числа")
            is_negative = number < 0
            number = abs(number)
            binary = ""
            while number > 0:
                binary = str(number % 2) + binary
                number //= 2
            binary = binary.zfill(7)
            return f'{int(is_negative)}{binary}'
        else:
            if number < 0 or number > 255:
                raise ValueError("Значение выходит за пределы диапазона для 8-битного беззнакового числа")
            binary = ""
            while number > 0:
                binary = str(number % 2) + binary
                number //= 2
            return binary.zfill(Binary.BIT_SIZE_8) if to8Bit else binary

    @staticmethod
    def toBinaryForward(number: Union[int, str], signed: bool = True) -> str:
        if isinstance(number, str):
            return number[::-1][:Binary.BIT_SIZE_8][::-1].zfill(Binary.BIT_SIZE_8)
        return Binary.intToBinary(number, signed)

    @staticmethod
    def toBinaryReverse(number: Union[int, str], signed: bool = True) -> str:
        binary = Binary.toBinaryForward(number, signed)
        if signed and binary[0] == "1":
            inverted = ''.join('1' if bit == '0' else '0' for bit in binary[1:])
            return binary[0] + inverted
        return binary

    @staticmethod
    def toBinaryComplement(number: Union[int, str], signed: bool = True) -> str:
        if not signed or (isinstance(number, int) and number >= 0) or (isinstance(number, str) and number[0] == "0"):
            return Binary.toBinaryForward(number, signed)
        reverse_code = Binary.toBinaryReverse(number, signed)
        complement = Binary._sum(reverse_code, Binary.BIN_1)[-Binary.BIT_SIZE_8:]
        return complement

    @staticmethod
    def binaryToInt(binary: str, signed: bool = True) -> int:
        if signed:
            sign_bit = binary[0]
            value = int(binary[1:], 2)
            return -value if sign_bit == "1" else value
        else:
            return int(binary, 2)

    @staticmethod
    def _sum(first: str, second: str) -> str:
        max_len = max(len(first), len(second))
        first, second = first.zfill(max_len), second.zfill(max_len)
        result, carry = "", 0
        for i in range(max_len - 1, -1, -1):
            s = carry + int(first[i]) + int(second[i])
            result = str(s % 2) + result
            carry = s // 2
        if carry:
            result = "1" + result
        return result

    @staticmethod
    def sum(first: Union[int, str], second: Union[int, str], signed: bool = True) -> str:
        if isinstance(first, int):
            first = Binary.intToBinary(first, signed)
        if isinstance(second, int):
            second = Binary.intToBinary(second, signed)
        
        if signed: sign = list(second)[0]
        
        if signed and sign: second = Binary.toBinaryComplement(second)
   
        result = Binary._sum(first, second)        

        return result[-Binary.BIT_SIZE_8:]

    @staticmethod
    def subtract(first: Union[int, str], second: Union[int, str], signed: bool = True) -> str:
        if isinstance(first, int):
            first = Binary.intToBinary(first, signed)
        if isinstance(second, int):
            second = Binary.intToBinary(second, signed)
        
        if signed and second[0] == '1':
            second_positive = Binary.toBinaryComplement(second, signed)
            return Binary.sum(first, second_positive, signed)
        
        if signed and first[0] == '1':
            second_negative = Binary.toBinaryComplement(second, signed)
            return Binary.sum(first, second_negative, signed)
        
        result = Binary._subtract(first, second)
        
        if signed and len(result) > Binary.BIT_SIZE_8:
            result = result[-Binary.BIT_SIZE_8:]
            if result[0] == '1':
                result = Binary.toBinaryComplement(result, signed)
        
        return result.zfill(Binary.BIT_SIZE_8)

    @staticmethod
    def multiply(first: Union[int, str], second: Union[int, str], signed: bool = True) -> str:
        result = Binary.BIN_0
        first_bin = Binary.toBinaryForward(first, signed)
        second_bin = Binary.toBinaryForward(second, signed)

        for bitPosition in range(len(second_bin) - 1, 0, -1):
            valueWithShift = first_bin + "0" * (7 - bitPosition)
            value8Bit = valueWithShift[::-1][:Binary.BIT_SIZE_8][::-1] if second_bin[bitPosition] == "1" else Binary.BIN_0
            result = Binary.toBinaryForward(Binary._sum(result, value8Bit), signed)
            
        result = list(result)
        result[0] = str((int(first_bin[0]) + int(second_bin[0])) % 2)
        
        return ''.join(result)

    @staticmethod
    def divide(dividend: Union[int, str], divisor: Union[int, str]) -> str:
        if isinstance(dividend, str):
            dividend = Binary.binaryToInt(dividend)
        if isinstance(divisor, str):
            divisor = Binary.binaryToInt(divisor)
        
        if divisor == 0:
            raise ZeroDivisionError("Деление на ноль невозможно")
        
        sign = "-" if (dividend < 0) ^ (divisor < 0) else ""

        dividend = abs(dividend)
        divisor = abs(divisor)

        dividend_bin = Binary.intToBinary(dividend)
        divisor_bin = Binary.intToBinary(divisor)

        quotient = 0
        remainder = 0

        for i in range(len(dividend_bin)):
            remainder = (remainder << 1) | int(dividend_bin[i])
            temp = Binary.binaryToInt(Binary.subtract(remainder, divisor_bin))
            if temp < 0:
                quotient = (quotient << 1) | 0
            else:
                quotient = (quotient << 1) | 1
                remainder = temp

        fractional_part = ""
        for _ in range(Binary.BIN_SIZE_FRACTION):
            remainder = remainder << 1
            temp = remainder - int(divisor_bin, 2)
            if temp < 0:
                fractional_part += "0"
            else:
                fractional_part += "1"
                remainder = temp

        result_bin = Binary.intToBinary(quotient) + "." + fractional_part
        
        return f"{result_bin}" 

    @staticmethod
    def binaryToDecimal(number: str) -> str:
        fractionIndex = number.index(".")
        
        intChunk = number[:fractionIndex][::-1]
        fractionChunk = number[fractionIndex + 1:]
        
        value = 0
        
        for bitIndex in range(len(intChunk)):
            value += 2**bitIndex if intChunk[bitIndex] == "1" else 0
        
        for bitIndex in range(len(fractionChunk)):
            value += 1 / 2 ** (bitIndex + 1) if fractionChunk[bitIndex] == "1" else 0
            
        return value
    
    @staticmethod
    def floatToBinary(number: float) -> str:
        result = ""
        while number > 0 and len(result) < Binary.IEEE_754_FORMAT["MANTISSA_LENGTH"]:
            number *= 2
            int_part = int(number)
            result += str(int_part)
            number -= int_part
        
        return result
    
    @staticmethod
    def toIEEE754(number: float) -> str:
        if number == 0:
            return "0" * Binary.BIT_SIZE_32

        sign_bit = "1" if number < 0 else "0"
        number = abs(number)

        int_part = int(number)
        frac_part = number - int_part

        binary_int = Binary.intToBinary(int_part, False, False)
        binary_frac = Binary.floatToBinary(frac_part)
        
        power = len(binary_int[1:])
        binary_frac = binary_int[1:] + binary_frac
        binary_int = binary_int[0]

        mantissa = (binary_int[1:] + binary_frac).ljust(Binary.IEEE_754_FORMAT["MANTISSA_LENGTH"],"0")
        
        exponent_bin = Binary.sum(127, power, False)
        exponent_bin = exponent_bin.zfill(Binary.BIT_SIZE_8)
 
        return sign_bit + exponent_bin + mantissa

    @staticmethod
    def IEEEtoDecimal(binary: str) -> float:
        if len(binary) != Binary.BIT_SIZE_32:
            raise ValueError("Длина двоичной строки должна быть 32 бита")
        
        if "0".zfill(Binary.BIT_SIZE_32) == binary: return 0

        sign_bit = binary[0]
        exponent_bin = binary[Binary.IEEE_754_FORMAT['END_SIGN_INDEX']:Binary.IEEE_754_FORMAT['END_POWER_INDEX']]
        mantissa_bin = binary[Binary.IEEE_754_FORMAT['END_POWER_INDEX']:Binary.IEEE_754_FORMAT['END_MANTISSA_INDEX']]

        exponent = Binary.binaryToInt(exponent_bin, signed=False) - 127
        mantissa = 1.0
        
        for i in range(len(mantissa_bin)):
            mantissa += int(mantissa_bin[i]) * (2 ** - (i + 1))

        value = mantissa * (2 ** exponent)
        return -value if sign_bit == "1" else value

    @staticmethod
    def _subtract(first: str, second: str) -> str:
        max_len = max(len(first), len(second))
        first, second = first.zfill(max_len), second.zfill(max_len)
        
        result = ""
        borrow = 0
        for i in range(max_len - 1, -1, -1):
            diff = int(first[i]) - int(second[i]) - borrow
            if diff < 0:
                diff += 2
                borrow = 1
            else:
                borrow = 0
            result = str(diff) + result
        
        return result.lstrip("0") or "0"
    
    @staticmethod
    def sumIEEE754(first: Union[float, str], second: Union[float, str]) -> str:
        if isinstance(first, str):
            first = Binary.IEEEtoDecimal(first)
        if isinstance(second, str):
            second = Binary.IEEEtoDecimal(second)
            
        ieee1 = Binary.toIEEE754(first)
        ieee2 = Binary.toIEEE754(second)

        sign1, sign2 = ieee1[0], ieee2[0]
        
        exponent1 = Binary.binaryToInt(ieee1[Binary.IEEE_754_FORMAT['END_SIGN_INDEX']:Binary.IEEE_754_FORMAT['END_POWER_INDEX']], signed=False)
        exponent2 = Binary.binaryToInt(ieee2[Binary.IEEE_754_FORMAT['END_SIGN_INDEX']:Binary.IEEE_754_FORMAT['END_POWER_INDEX']], signed=False)
        
        mantissa1 = ("1" + ieee1[Binary.IEEE_754_FORMAT['END_POWER_INDEX']:Binary.IEEE_754_FORMAT['END_MANTISSA_INDEX']])[:Binary.IEEE_754_FORMAT["MANTISSA_LENGTH"]]
        mantissa2 = ("1" + ieee2[Binary.IEEE_754_FORMAT['END_POWER_INDEX']:Binary.IEEE_754_FORMAT['END_MANTISSA_INDEX']])[:Binary.IEEE_754_FORMAT["MANTISSA_LENGTH"]]
        
        if exponent1 > exponent2:
            shift = exponent1 - exponent2
            mantissa2 = ("0" * shift + mantissa2)[:Binary.IEEE_754_FORMAT["MANTISSA_LENGTH"]]
            exponent2 = exponent1
        else:
            shift = exponent2 - exponent1
            mantissa1 = ("0" * shift + mantissa1)[:Binary.IEEE_754_FORMAT["MANTISSA_LENGTH"]]
            exponent1 = exponent2

        mantissa_sum = Binary._sum(mantissa1, mantissa2)
        
        if len(mantissa_sum) > Binary.IEEE_754_FORMAT["MANTISSA_LENGTH"]:
            exponent1 += 1

        mantissa_sum = mantissa_sum[1:]
        mantissa_sum = mantissa_sum[:Binary.IEEE_754_FORMAT["MANTISSA_LENGTH"]].ljust(Binary.IEEE_754_FORMAT["MANTISSA_LENGTH"], "0")
        
        exponent_bin = Binary.intToBinary(exponent1, signed=False)[-Binary.BIT_SIZE_8:].zfill(Binary.BIT_SIZE_8)
        sign = "0" if sign1 == sign2 else "1"
        
        return sign + exponent_bin + mantissa_sum
    

print(f'Первое число: {Binary.toIEEE754(16.625)}')
print(f'Второе число: {Binary.toIEEE754(1.5)}')
print(f'Сумма {Binary.sumIEEE754(Binary.toIEEE754(16.625),Binary.toIEEE754(1.5))}')
