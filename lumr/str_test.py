if __name__ == '__main__':
    s = 'b4a3 1995 e993 0050 2d42 ca29 0c41 7c8b'
    byte_str = s.split(' ')
    bytes_str = []
    for by in byte_str:
        bytes_str.append(by[0:2])
        bytes_str.append(by[2:4])

    bytes_int = [int(by, 16) for by in bytes_str]
    print(str(bytes(bytes_int),'utf-8',))
