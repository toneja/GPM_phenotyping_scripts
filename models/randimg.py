#!/usr/bin/python3
#
# This file is part of the GPM phenotyping scripts.
#
# Copyright (c) 2024 Jason Toney
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import os
import random
import shutil


sample_count = 18
index = 1
for folder in os.listdir("../ImageJ/GPM/images"):
    if "48" in folder:
        used = []
        while len(used) < sample_count:
            i = random.randint(1, 96)
            if i in used:
                continue
            else:
                used.append(i)
                if i < 10:
                    img_name = f"Tile00000{i}.tif"
                else:
                    img_name = f"Tile0000{i}.tif"
                if not os.path.exists(f"MODEL/{index}.tif"):
                    shutil.copy(
                        f"../ImageJ/GPM/images/{folder}/{img_name}", f"images/{index}.tif"
                    )
                index += 1
