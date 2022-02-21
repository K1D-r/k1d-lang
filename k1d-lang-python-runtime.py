import sys


class Umjunsik:
    def __init__(self):
        self.data = [0]*256

    def toNumber(self, code):
        return eval('*'.join(list(map(lambda cmd:str((self.data[cmd.count('어')-1] if cmd.count('어') else 0) + cmd.count('.') - cmd.count(',')), code.split(' ')))))

    @staticmethod
    def type(code):
        if 'D드라이브빠짐' in code:
            return 'IF'
        if '1' in code:
            return 'MOVE'
        if '미친놈아!' in code:
            return 'END'
        if '드' in code and '?' in code:
            return 'INPUT'
        if '드' in code and '!' in code:
            return 'PRINT'
        if '드' in code and 'ㅋ' in code:
            return 'PRINTASCII'
        if '키' in code:
            return 'DEF'

    def compileLine(self, code):
        if code == '':
            return None
        TYPE = self.type(code)
        
        if TYPE == 'DEF':
            var, cmd = code.split('키')
            self.data[var.count('어')] = self.toNumber(cmd)
        elif TYPE == 'END':
            print(self.toNumber(code.split('미친놈아!')[1]), end='')
            sys.exit()
        elif TYPE == 'INPUT':
            self.data[code.replace('드?', '').count('어')] = int(input())
        elif TYPE == 'PRINT':
            print(self.toNumber(code[1:-1]), end='')
        elif TYPE == 'PRINTASCII':
            value = self.toNumber(code[1:-1])
            print(chr(value) if value else '\n', end='')
        elif TYPE == 'IF':
            cond, cmd = code.replace('D드라이브빠짐', '').split('?')
            if self.toNumber(cond) == 0:
                return cmd
        elif TYPE == 'MOVE':
            return self.toNumber(code.replace('1', ''))

    def compile(self, code, check=True, errors=100000):
        jun = False
        recode = ''
        spliter = '\n' if '\n' in code else '~'
        code = code.rstrip().split(spliter)
        if check and (code[0].replace(" ","") != '어떻게' or code[-1] != '이 사람이름이냐ㅋㅋ' or not code[0].startswith('어떻게')):
            raise SyntaxError('어떻게 이게 키랭이냐!')
        index = 0
        error = 0
        while index < len(code):
            errorline = index
            c = code[index].strip()
            res = self.compileLine(c)
            if jun:
                jun = False
                code[index] = recode                
            if isinstance(res, int):
                index = res-2
            if isinstance(res, str):
                recode = code[index]
                code[index] = res
                index -= 1
                jun = True

            index += 1
            error += 1
            if error == errors:
                raise RecursionError(str(errorline+1) + '번째 줄에서 무한 루프가 감지되었습니다.')

    def compilePath(self, path):
        with open(path) as file:
            code = ''.join(file.readlines())
            self.compile(code)
