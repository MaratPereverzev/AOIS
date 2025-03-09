from Lab1.Binary import Binary

def d8421_to_decimal(tetrad):
    """Преобразует тетраду в коде Д8421 в десятичное число."""
    return Binary.binaryToInt(tetrad)

def decimal_to_d8421(decimal):
    """Преобразует десятичное число в тетраду в коде Д8421."""
    if 0 <= decimal <= 9:
        return Binary.intToBinary(decimal, False)[-4:]
    else:
        return Binary.intToBinary(decimal + 6, False)[-4:]

def d8421_plus_n(tetrad, n):
    """Преобразует тетраду в коде Д8421 в код Д8421+n."""
    decimal = d8421_to_decimal(tetrad)
    result_decimal = decimal + n
    return decimal_to_d8421(result_decimal)

tetrad = "0111"
n = 4

result = d8421_plus_n(tetrad, n)
print(f"Результат преобразования тетрады {tetrad} в код Д8421+{n}: {result}")