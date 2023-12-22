'''
SSD 시뮬레이터의 하드웨어 구성요소를 class로 정의하는 파일
'''

from collections import deque


class Page:
    '''
    ssd의 page에 대해 정의하는 클래스
    ssd는 page 단위로 읽기와 쓰기를 진행한다.
    '''

    def __init__(self, ppn):
        self.ppn = ppn # ppn = physical page number
        self.valid = False
    

    def get_ppn(self):
        return self.ppn
    

    def set_valid(self):
        self.valid = True


    def set_invalid(self):
        self.valid = False

    
    def get_valid(self):
        return self.valid



class Block:
    '''
    ssd의 block에 대해 정의하는 클래스
    ssd는 Block단위로 데이터를 삭제한다.
    '''

    def __init__(self, block_num, pages): 
        self.block_num = block_num
        self.valid_count = 0
        self.invalid_count = 0
        self.erase_count = 0
        self.open_pages = deque([i for i in range(len(pages))])
        self.pages = pages

    
    def get_block_num(self):
        return self.block_num
    

    def get_pages(self):
        return self.pages
    
class Plane:


    def __init__(self, plane_num, blocks):
        self.plane_num = plane_num
        self.blocks = blocks
        self.open_block = 0

    
    def get_plane_num(self):
        return self.plane_num
    

    def get_blocks(self):
        return self.blocks


class Chip:
    '''
    ssd의 Chip에 대해 정의하는 클래스
    Chip은 nand flash 1개를 말한다.
    '''

    def __init__(self, chip_num, planes): # chip_capa는 mb 단위
        self.chip_num = chip_num
        self.planes = planes


    def get_chip_num(self):
        return self.chip_num
    

    def get_planes(self):
        return self.planes


class Channel:
    '''
    ssd의 Channel에 대해 정의하는 클래스
    Channel은 nand flash가 컨트롤러와 연결되는 Bus를 말한다.
    '''

    def __init__(self, channel_num, chips):
        self.channel_num = channel_num
        self.chips = chips

    
    def get_channel_num(self):
        return self.channel_num
    

    def get_chips(self):
        return self.chips