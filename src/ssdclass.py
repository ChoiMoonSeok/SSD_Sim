'''
SSD 시뮬레이터의 하드웨어 구성요소를 class로 정의하는 파일
'''


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

    def __init__(self, block_num, block_capa, page_size): # block_capa는 kb 단위
        self.block_num = block_num
        self.pages = [Page(ppn) for ppn in range(block_num * (block_capa // page_size), (block_num + 1) * (block_capa // page_size))]

    
    def get_block_num(self):
        return self.block_num
    

    def get_pages(self):
        return self.pages
    


class Chip:
    '''
    ssd의 Chip에 대해 정의하는 클래스
    Chip은 nand flash 1개를 말한다.
    '''

    def __init__(self, chip_num, chip_capa, block_size, page_size): # chip_capa는 mb 단위
        self.chip_num = chip_num
        self.blocks = [Block(blk_num, block_size, page_size) for blk_num in range(chip_num * chip_capa * 1024 // block_size, (chip_num + 1) * chip_capa * 1024 // block_size)]


    def get_chip_num(self):
        return self.chip_num
    

    def get_blocks(self):
        return self.blocks



class SuperBlock:
    '''
    ssd에 존재하는 channel * way 개의 chip의 블록 묶음
    ex) channel = 4
        way = 2
        chip = 32

        1개의 super block = 4 * 2 개의 block(4 * 2개의 chip에서 각각 뽑아온)
    '''

    def __init__(self, super_block_num, chips):
        self.super_block_num = super_block_num
        self.blocks = [chip.blocks[self.super_block_num] for chip in chips]

    
    def get_super_block_num(self):
        return self.super_block_num


    def get_blocks(self):
        return self.blocks



class SuperChip:
    '''
    SuperBlock의 모음
    '''

    def __init__(self, super_chip_num, super_blocks):
        self.super_chip_num = super_chip_num
        self.super_blocks = super_blocks


    def get_super_chip_num(self):
        return self.super_chip_num
    

    def get_super_blocks(self):
        return self.super_blocks