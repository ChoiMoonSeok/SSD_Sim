from collections import deque

import ssdclass


class FTL:
    """
    ssd를 관리하는 Flash Translation Layer에 대한 구현
    """

    def __init__(
        self,
        channel_per_ssd=8,
        chip_per_channel=8,
        plane_per_chip=1,
        block_per_plane=256,
        page_per_block=256,
    ):
        """
        ssd의 모든 page, block, plane, chip, chnnel을 생성
        """

        # ssd의 하드웨어 구성에 대한 전역 변수(용량과 관련 있음)
        self.channel_per_ssd = channel_per_ssd
        self.chip_per_channel = chip_per_channel
        self.plane_per_chip = plane_per_chip
        self.block_per_plane = block_per_plane
        self.page_per_block = page_per_block

        # ssd의 여러 측정 지표를 위한 전역 변수
        self.user_write_count = 0
        self.ftl_write_count = 0

        # ssd의 시뮬레이션을 위한 객체 생성
        page_pool = [
            ssdclass.Page(ppn)
            for ppn in range(
                channel_per_ssd
                * chip_per_channel
                * plane_per_chip
                * block_per_plane
                * page_per_block
            )
        ]
        block_pool = [
            ssdclass.Block(
                blk_num,
                page_pool[blk_num * page_per_block : (blk_num + 1) * page_per_block],
            )
            for blk_num in range(
                channel_per_ssd * chip_per_channel * plane_per_chip * block_per_plane
            )
        ]
        plane_pool = [
            ssdclass.Plane(
                plane_num,
                block_pool[
                    plane_num * block_per_plane : (plane_num + 1) * block_per_plane
                ],
            )
            for plane_num in range(channel_per_ssd * chip_per_channel * plane_per_chip)
        ]
        chip_pool = [
            ssdclass.Chip(
                chip_num,
                plane_pool[chip_num * plane_per_chip : (chip_num + 1) * plane_per_chip],
            )
            for chip_num in range(channel_per_ssd * chip_per_channel)
        ]
        channel_pool = [
            ssdclass.Channel(
                channel_num,
                chip_pool[
                    channel_num
                    * chip_per_channel : (channel_num + 1)
                    * chip_per_channel
                ],
            )
            for channel_num in range(channel_per_ssd)
        ]

        self.page_pool = page_pool
        self.block_pool = block_pool
        self.plane_pool = plane_pool
        self.chip_pool = chip_pool
        self.channel_pool = channel_pool

        # ssd의 lba와 ppn의 맵핑 테이블 정의
        self.lpn_pool = deque(
            [
                lpn
                for lpn in range(
                    channel_per_ssd
                    * chip_per_channel
                    * plane_per_chip
                    * block_per_plane
                    * page_per_block
                )
            ]
        )
        self.mapping_table_lba_lpn = dict()
        self.mapping_table_lpn_ppn = dict()

        # ssd의 내부 병렬성을 위한 변수
        self.line_pool = deque(
            [
                line_num
                for line_num in range(
                    chip_per_channel * plane_per_chip * block_per_plane * page_per_block
                )
            ]
        )

    def get_line(self):
        line_num = self.line_pool.pop()
        line = [None] * self.channel_per_ssd
        for channel in self.channel_pool:
            chip = channel.chips[
                line_num
                // (self.plane_per_chip * self.block_per_plane * self.page_per_block)
            ]
            plane = chip.planes[
                line_num // (self.chip_per_channel * self.block_per_plane * self.page_per_block)
            ]
            block = plane.blocks[plane.open_block]
            while len(block.open_pages) == 0:
                plane.open_block = (plane.open_block + 1 ) % self.block_per_plane 
            page = block.pages[block.open_pages.pop()]


            line[channel.channel_num] = page

        self.line_pool.appendleft(line_num)

        return line

    def write(self, lba, size):
        if self.mapping_table_lba_lpn.get(lba) != None:
            for lpn in self.mapping_table_lba_lpn.get(lba):
                ppn = self.mapping_table_lpn_ppn[lpn]
                self.page_pool[ppn].valid = False
                self.block_pool[ppn // self.page_per_block].valid_count -= 1
                self.block_pool[ppn // self.page_per_block].invalid_count += 1

                self.lpn_pool.appendleft(lpn)


        if size > self.channel_per_ssd:
            line = deque([page for page in self.get_line() for _ in range(size // self.channel_per_ssd + 1)])
            self.mapping_table_lba_lpn[lba] = [self.line_pool.pop() for _ in range(len(line))]
        else:
            line = deque(self.get_line())
            self.mapping_table_lba_lpn[lba] = [
                self.line_pool.pop() for _ in range(self.channel_per_ssd)
            ]

        for lpn in self.mapping_table_lba_lpn[lba]:
            ppn = line.pop()
            self.mapping_table_lpn_ppn[lpn] = ppn.ppn
            ppn.valid = True

            self.block_pool[ppn.ppn // self.page_per_block].valid_count += 1


    def erase(self, lba, size):
        pass

    def do_gc(self, n_blocks=1):  # n_blocks : gc할 블록의 수
        pass

    def do_wear_leveling(self):
        pass


ftl = FTL()

ftl.write(0, 7)
ftl.write(0, 7)