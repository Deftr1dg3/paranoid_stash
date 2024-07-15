#!/usr/bin/env python3

import re
import random
from dataclasses import dataclass
from typing import NamedTuple
from string import ascii_uppercase, ascii_lowercase, digits, punctuation


punctuation = punctuation.replace("\\", "")
punctuation = punctuation.replace("`", "")
punctuation = punctuation.replace("'", "")
punctuation = punctuation.replace('"', "")
punctuation = punctuation.replace("[", "")
punctuation = punctuation.replace("]", "")

class StrengthSpecification(NamedTuple):
    uppercase: int 
    lowercase: int 
    digit: int
    special_symbol: int
    length: int
    shuffle_cycle: int
     
@dataclass
class PasswordStrength:
    _SHUFFLE_CYCLE = 10
    MAX_PASSWORD_LEGTH = 32
    VERY_STRONG = StrengthSpecification(uppercase=1, lowercase=2, digit=2, special_symbol=1, length=16, shuffle_cycle=_SHUFFLE_CYCLE)
    STRONG = StrengthSpecification(uppercase=1, lowercase=1, digit=1, special_symbol=1, length=12, shuffle_cycle=_SHUFFLE_CYCLE)
    MEDIUM = StrengthSpecification(uppercase=1, lowercase=0, digit=1, special_symbol=0, length=8, shuffle_cycle=_SHUFFLE_CYCLE)
    WEAK = StrengthSpecification(uppercase=0, lowercase=1, digit=1, special_symbol=0, length=8, shuffle_cycle=_SHUFFLE_CYCLE)
    VERY_WEAK = StrengthSpecification(uppercase=0, lowercase=0, digit=0, special_symbol=0, length=8, shuffle_cycle=_SHUFFLE_CYCLE)
    

class GeneratePassword:
    def __init__(self):
        self._password = []
        
    def _uppercase(self, items: int) -> None:
        uppercase = [random.choice(ascii_uppercase) for _ in range(items)]
        self._password.extend(uppercase)
        
    def _lowercase(self, items: int) -> None:
        lowercase = [random.choice(ascii_lowercase) for _ in range(items)]
        self._password.extend(lowercase)
        
    def _digits(self, items: int) -> None:
        selected_digits = [random.choice(digits) for _ in range(items)]
        self._password.extend(selected_digits)

    def _special_symbols(self, items: int) -> None:
        selected_symbols = [random.choice(punctuation) for _ in range(items)]
        self._password.extend(selected_symbols)
        
    def _rest(self, items: int, s: StrengthSpecification) -> None:
        if s.uppercase == 0 and s.lowercase == 0 and s.special_symbol == 0 and s.digit == 0:
            rest = [random.choice(digits) for _ in range(items)]
        elif s.uppercase == 0 and s.special_symbol == 0:
            rest = [random.choice(ascii_lowercase + digits) for _ in range(items)]
        else:
            rest = [random.choice(ascii_lowercase + digits + ascii_uppercase + punctuation) for _ in range(items)]
        self._password.extend(rest)
        
    def _shuffle(self, cycles: int) -> None:
        for _ in range(cycles):
            random.shuffle(self._password)
    
    def generate_password(self, strength: StrengthSpecification) -> str:
        total_length = strength.length
        rest_length = total_length - strength.uppercase - strength.lowercase - strength.digit - strength.special_symbol
        self._uppercase(strength.uppercase)
        self._lowercase(strength.lowercase)
        self._digits(strength.digit)
        self._special_symbols(strength.special_symbol)
        self._rest(rest_length, strength)
        self._shuffle(strength.shuffle_cycle)
        return ''.join(self._password)
    

class ValidatePassword:
    def __init__(self) -> None:
        self._special_symbols = r"[!,#,$,%,&,',(,),*,+,\,,-,.,/,:,;,<,=,>,?,@,\[,\\,\],^,_,`,{,|,},~]"

    def _validate_very_strong(self, password: str) -> bool:
        s = PasswordStrength.VERY_STRONG
        r = f"^" + f"(?=" + ".*[A-Z]" * s.uppercase + ")" + f"(?=" + ".*[a-z]" * s.lowercase + ")" + f"(?=" + f".*{self._special_symbols}" * s.special_symbol + ")" + f"(?=" + ".*\\d" * s.digit + ")" + ".{" + f"{s.length}," + "}" + "$"
        rgx = re.compile(r)
        result = bool(rgx.match(password))
        return result
    
    def _validate_strong(self, password: str) -> bool:
        s = PasswordStrength.STRONG
        r = f"^" + f"(?=" + ".*[A-Z]" * s.uppercase + ")" + f"(?=" + ".*[a-z]" * s.lowercase + ")" + f"(?=" + f".*{self._special_symbols}" * s.special_symbol + ")" + f"(?=" + ".*\\d" * s.digit + ")" + ".{" + f"{s.length}," + "}" + "$"
        rgx = re.compile(r)
        result = bool(rgx.match(password))
        return result   
    
    def _validate_medium(self, password: str) -> bool:
        s = PasswordStrength.MEDIUM
        r = f"^" + f"(?=" + ".*[A-Z]" * s.uppercase + ")" + f"(?=" + ".*[a-z]" * s.lowercase + ")" + f"(?=" + f".*{self._special_symbols}" * s.special_symbol + ")" + f"(?=" + ".*\\d" * s.digit + ")" + ".{" + f"{s.length}," + "}" + "$"
        rgx = re.compile(r)
        result = bool(rgx.match(password))
        return result  
    
    def _validate_weak(self, password: str) -> bool:
        s = PasswordStrength.WEAK
        r = f"^" + f"(?=" + ".*[A-Z]" * s.uppercase + ")" + f"(?=" + ".*[a-z]" * s.lowercase + ")" + f"(?=" + f".*{self._special_symbols}" * s.special_symbol + ")" + f"(?=" + ".*\\d" * s.digit + ")" + ".{" + f"{s.length}," + "}" + "$"
        rgx = re.compile(r)
        result = bool(rgx.match(password))
        return result 
    
    def validate_password(self, password: str) -> str:
        if self._validate_very_strong(password):
            return "VERY STRONG"
        if self._validate_strong(password):
            return "STRONG"
        if self._validate_medium(password):
            return "MEDIUM"
        if self._validate_weak(password):
            return "WEAK"
        return "VERY WEAK"