# -*- coding: utf-8 -*-
"""
crc64iso3309.py

Module for calculating 64-bit CRC checksum according to the ISO 3309 standard using Python 3.x.

Generator polynomial:
x64 + x4 + x3 + x + 1

Reference:
W. H. Press, S. A. Teukolsky, W. T. Vetterling, and B. P. Flannery, "Numerical recipes in C", 2nd ed.,
Cambridge University Press. Pages 896ff.
"""

# Cached tables
CRC_TABLE_H = [0, 28311552, 56623104, 47185920, 113246208, 124780544, 94371840, 68157440, 226492416, 204472320,
               249561088, 256901120, 188743680, 183500800, 136314880, 160432128, 452984832, 447741952, 408944640,
               433061888, 499122176, 477102080, 513802240, 521142272, 377487360, 389021696, 367001600, 340787200,
               272629760, 300941312, 320864256, 311427072, 905969664, 934281216, 895483904, 886046720, 817889280,
               829423616, 866123776, 839909376, 998244352, 976224256, 954204160, 961544192, 1027604480, 1022361600,
               1042284544, 1066401792, 754974720, 749731840, 778043392, 802160640, 734003200, 711983104, 681574400,
               688914432, 545259520, 556793856, 601882624, 575668224, 641728512, 670040064, 622854144, 613416960,
               1811939328, 1840250880, 1868562432, 1859125248, 1790967808, 1802502144, 1772093440, 1745879040,
               1635778560, 1613758464, 1658847232, 1666187264, 1732247552, 1727004672, 1679818752, 1703936000,
               1996488704, 1991245824, 1952448512, 1976565760, 1908408320, 1886388224, 1923088384, 1930428416,
               2055208960, 2066743296, 2044723200, 2018508800, 2084569088, 2112880640, 2132803584, 2123366400,
               1509949440, 1538260992, 1499463680, 1490026496, 1556086784, 1567621120, 1604321280, 1578106880,
               1468006400, 1445986304, 1423966208, 1431306240, 1363148800, 1357905920, 1377828864, 1401946112,
               1090519040, 1085276160, 1113587712, 1137704960, 1203765248, 1181745152, 1151336448, 1158676480,
               1283457024, 1294991360, 1340080128, 1313865728, 1245708288, 1274019840, 1226833920, 1217396736,
               3623878656, 3652190208, 3680501760, 3671064576, 3737124864, 3748659200, 3718250496, 3692036096,
               3581935616, 3559915520, 3605004288, 3612344320, 3544186880, 3538944000, 3491758080, 3515875328,
               3271557120, 3266314240, 3227516928, 3251634176, 3317694464, 3295674368, 3332374528, 3339714560,
               3464495104, 3476029440, 3454009344, 3427794944, 3359637504, 3387949056, 3407872000, 3398434816,
               3992977408, 4021288960, 3982491648, 3973054464, 3904897024, 3916431360, 3953131520, 3926917120,
               3816816640, 3794796544, 3772776448, 3780116480, 3846176768, 3840933888, 3860856832, 3884974080,
               4110417920, 4105175040, 4133486592, 4157603840, 4089446400, 4067426304, 4037017600, 4044357632,
               4169138176, 4180672512, 4225761280, 4199546880, 4265607168, 4293918720, 4246732800, 4237295616,
               3019898880, 3048210432, 3076521984, 3067084800, 2998927360, 3010461696, 2980052992, 2953838592,
               3112173568, 3090153472, 3135242240, 3142582272, 3208642560, 3203399680, 3156213760, 3180331008,
               2936012800, 2930769920, 2891972608, 2916089856, 2847932416, 2825912320, 2862612480, 2869952512,
               2726297600, 2737831936, 2715811840, 2689597440, 2755657728, 2783969280, 2803892224, 2794455040,
               2181038080, 2209349632, 2170552320, 2161115136, 2227175424, 2238709760, 2275409920, 2249195520,
               2407530496, 2385510400, 2363490304, 2370830336, 2302672896, 2297430016, 2317352960, 2341470208,
               2566914048, 2561671168, 2589982720, 2614099968, 2680160256, 2658140160, 2627731456, 2635071488,
               2491416576, 2502950912, 2548039680, 2521825280, 2453667840, 2481979392, 2434793472, 2425356288]
CRC_TABLE_L = [0] * 256


def _calculate_tables():
    poly64_rev_h = 0xd8000000
    bit_toggle = 1 << 31

    crc_table_h = [0] * 256
    crc_table_l = [0] * 256

    for i in range(256):
        part_l = i
        part_h = 0
        for j in range(8):
            r_flag = part_l & 1
            part_l >>= 1
            if part_h & 1:
                part_l ^= bit_toggle
            part_h >>= 1
            if r_flag:
                part_h ^= poly64_rev_h
        crc_table_h[i] = part_h
        crc_table_l[i] = part_l
    return crc_table_h, crc_table_l


def crc64_pair(bytes_, crc_pair=(0, 0)):
    """
    Calculates 64-bit CRC as two 32-bit integers given bytes to checksum

    Args:
        bytes_ (bytes): Bits of data to checksum
        crc_pair (tuple): Higher and lower halves of 64-bit CRC result. Defaults to (0, 0) to compute from scratch.
    Return:
        tuple: Higher and lower halves of 64-bit CRC result
    """
    if not isinstance(bytes_, bytes):
        raise AssertionError('crc64_pair needs bytes object as first argument')

    crc_h, crc_l = crc_pair
    for b in bytes_:
        shr = (crc_h & 0xFF) << 24
        tmp_1h = crc_h >> 8
        tmp_1l = (crc_l >> 8) | shr
        table_i = (crc_l ^ b) & 0xFF
        crc_h = tmp_1h ^ CRC_TABLE_H[table_i]
        crc_l = tmp_1l ^ CRC_TABLE_L[table_i]
    return crc_h, crc_l


def format_crc64_pair(crc_pair):
    """
    Formats two 32-bit integers to digest

    Args:
        crc_pair (tuple): Higher and lower halves of 64-bit CRC result
    Returns:
        str: 64-bit checksum (digest)
    """
    return "%08X%08X" % crc_pair


def crc64(input_str):
    """
    Calculates 64-bit CRC digest

    Args:
        input_str (str): String to checksum
    Returns:
        str: 64-bit checksum (digest)
    """
    return format_crc64_pair(crc64_pair(input_str.encode('utf8')))


if __name__ == '__main__':
    CRC_TABLE_H_CALC, CRC_TABLE_L_CALC = _calculate_tables()
    assert CRC_TABLE_H == CRC_TABLE_H_CALC
    assert CRC_TABLE_L == CRC_TABLE_L_CALC
    assert crc64_pair("IHATEMATH".encode('utf8')) == (3822890454, 2600578513)
    assert crc64("IHATEMATH") == "E3DCADD69B01ADD1"
