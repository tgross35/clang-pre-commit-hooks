"""A script """

import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime
from typing import BinaryIO, Tuple
from urllib import request
from urllib.error import HTTPError

import magic

BASEURL = "https://commondatastorage.googleapis.com/chromium-clang-format"


@dataclass
class Entry:
    key: str
    date: datetime
    typename:str
    mime:str
    version:Tuple[int,int,int]=None

    def dump(self):
        return self.version,{self.platform:self.key}

def get_finfo(url:str, f:BinaryIO)->Entry:
    pass

def get_format_shas():
    with request.urlopen(BASEURL) as f:
        root = ET.parse(f).getroot()

    # File consists of a list of "Contents" elements like the following:
    # <Contents>
    #     <Key>025ca7c75f37ef4a40f3a67d81ddd11d7d0cdb9b</Key>
    #     <Generation>1542380408102454</Generation>
    #     <MetaGeneration>2</MetaGeneration>
    #     <LastModified>2018-11-16T15:00:08.102Z</LastModified>
    #     <ETag>"dc0a8156bf45a2c39e6bd45dff984bbb"</ETag>
    #     <Size>1967524</Size>
    # </Contents>
    # "Key" is its downloadable type

    # The {*} indicates catch from all namespaces
    content_elements = root.findall("{*}Contents")

    entries = []

    for el in content_elements:
        key=el.find("{*}Key").text
        # fromisoformat is too picky and doesn't like iso format
        lastmodified = datetime.fromisoformat(
            el.find("{*}LastModified").text.partition("Z")[0]
        )
        try:
            with request.urlopen(f"{BASEURL}/{key}") as f:
                buf = f.read(2048)
        except HTTPError:
            # Just carry on if we can't download for some reason
            continue

        entry = Entry(key, lastmodified,magic.from_buffer(buf),magic.from_buffer(buf,mime=True))
        entries.append(entry)

    pass

if __name__=='__main__':
    main()
