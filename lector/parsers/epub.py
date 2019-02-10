# This file is a part of Lector, a Qt based ebook reader
# Copyright (C) 2017-2019 BasioMeusPuga

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import zipfile
import logging

from lector.readers.read_epub import EPUB

logger = logging.getLogger(__name__)


class ParseEPUB:
    def __init__(self, filename, temp_dir, file_md5):
        # TODO
        # Maybe also include book description
        self.book_ref = None
        self.book = None
        self.temp_dir = temp_dir
        self.filename = filename
        self.extract_path = os.path.join(temp_dir, file_md5)

    def read_book(self):
        self.book_ref = EPUB(self.filename, self.temp_dir)
        self.book_ref.generate_metadata()
        self.book = self.book_ref.book
        return True

    def get_title(self):
        return self.book['title']

    def get_author(self):
        return self.book['author']

    def get_year(self):
        return self.book['year']

    def get_cover_image(self):
        return self.book['cover']

    def get_isbn(self):
        return self.book['isbn']

    def get_tags(self):
        return self.book['tags']

    def get_contents(self):
        zipfile.ZipFile(self.filename).extractall(self.extract_path)

        self.book_ref.generate_toc()
        self.book_ref.generate_content()

        toc = []
        content = []
        for count, i in enumerate(self.book['content']):
            toc.append((i[0], i[1], count + 1))
            content.append(i[2])

        # Return toc, content, images_only
        return toc, content, False
