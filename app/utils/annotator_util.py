from dataclasses import dataclass
from typing import List


@dataclass
class GemPoint:
    x: int
    y: int
    w: int
    h: int
    order_idx: int = -1

    @property
    def formatted_tuple(self):
        return self.x, self.y, self.w, self.h, self.order_idx


@dataclass
class GemBoundingBox:
    label: str
    boundingboxes: List[GemPoint]

    def add_point(self, point: GemPoint):
        self.boundingboxes.append(point)

    @property
    def len(self):
        return len(self.boundingboxes)

    @property
    def to_json(self):
        return {'label': self.label, 'boundingbox': self.boundingboxes}


@dataclass
class GemWord:
    start: int
    end: int
    label: str

    @property
    def formatted_tuple(self):
        return self.start, self.end, self.label

    @property
    def to_list(self):
        return [self.start, self.end, self.label]


@dataclass
class GemSentences:
    text: str
    words: List[GemWord]

    @property
    def formatted_tuple(self):
        return self.text, self.words

    def add_word(self, word: GemWord):
        self.words.append(word)

    @property
    def to_json(self):
        return {'text': self.text, 'labels': [word.to_list for word in self.words]}
