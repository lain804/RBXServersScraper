import json
import hashlib
import base64
from .performance import measure_performance

class ChallengeDataEnum:
    TARGET = 'c'
    PREFIX = 's'
    ID     = 'i'

class Challenge:
    MAX_ITERATIONS = 1_000_000

    def __init__(self,data:dict):
        self.target       :str = data[ChallengeDataEnum.TARGET]
        self.prefix       :str = data[ChallengeDataEnum.PREFIX]
        self.challenge_id :str = data.get(ChallengeDataEnum.ID)

    #@measure_performance
    def solve(self) -> int:
        prefix_encoded = self.prefix.encode()
        hash_object = hashlib.sha256(prefix_encoded)

        for i in range(Challenge.MAX_ITERATIONS+1):

            hash_object_copy = hash_object.copy()
            hash_object_copy.update(str(i).encode())

            if hash_object_copy.hexdigest() == self.target:
                return i
            
    @classmethod
    def from_dict(cls,data:dict[str,str]) -> Challenge:
        return cls(data)
    
    @classmethod
    def from_json(cls,data:str) -> Challenge:
        return cls.from_dict(json.loads(data))

    @classmethod
    def from_base64(cls,data:str) -> Challenge:
        return cls.from_json(base64.b64decode(data))
