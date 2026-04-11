from enum import Enum

class ReactionType(str, Enum):
    like = "like"
    love = "love"
    haha = "haha"
    wow = "wow"
    sad = "sad"
    angry = "angry"