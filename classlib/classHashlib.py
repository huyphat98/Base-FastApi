import hashlib 
SHA1_ALGOR=1
SHA224_ALGOR=2
SHA256_ALGOR=3
SHA384_ALGOR=4
SHA512_ALGOR=5

TEST_HASHLIB_CODE=0

def HashEncode(str_2_check, algorithm=SHA1_ALGOR):
    if algorithm== SHA1_ALGOR:
        res = hashlib.sha1(str.encode(str_2_check))
    elif algorithm== SHA224_ALGOR:
        res = hashlib.sha224(str.encode(str_2_check))
    elif algorithm== SHA256_ALGOR:
        res = hashlib.sha256(str.encode(str_2_check))
    elif algorithm== SHA384_ALGOR:
        res = hashlib.sha384(str.encode(str_2_check))
    elif algorithm== SHA512_ALGOR:
        res = hashlib.sha512(str.encode(str_2_check))
    return res.hexdigest()

### Kiem tra giong nhau 2 string neu bo qua tat
def CheckMatching(str_base, str_check):
    matching = False
    
    ## Bo dau khoang trang giua cac ki tu, bo \r\n, chuyen ve ki tu thuong, bo dau ,
    str1 = (str_base.strip()).replace(' ','')
    str1 = (str1.strip()).replace(',','')
    str1 = str1.lower()
    str2 = (str_check.strip()).replace(' ','')
    str2 = (str2.strip()).replace(',','')
    str2 = str2.lower()

    ## Parse dung SHA=================
    sha_of_str1 = HashEncode(str1, algorithm=SHA1_ALGOR)
    sha_of_str2 = HashEncode(str2, algorithm=SHA1_ALGOR)
    if (sha_of_str1==sha_of_str2): matching = True
    return matching

if TEST_HASHLIB_CODE:
    a = "phường Tây Thạnh, quận Tân Phú, TPHCM"
    b = "phường Tây thạnh,            quận tân phú, TPHCM"

    print ("Kiem tra chuoi ki tu sau (must True): ",CheckMatching(a,b))
    b = "phường Tây thanh,            quận tân phú, TPHCM"
    print ("Kiem tra chuoi ki tu sau (must False): ",CheckMatching(a,b))

