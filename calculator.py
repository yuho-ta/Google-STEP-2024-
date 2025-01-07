#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_multi(line, index):
    token = {'type': 'MULTI'}
    return token, index + 1

def read_divide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1

def read_lparen(line, index):
    token = {'type': 'LPAREN'}
    return token, index + 1

def read_rparen(line, index):
    token = {'type': 'RPAREN'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multi(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
        elif line[index] == '(':
            (token, index) = read_lparen(line, index)
        elif line[index] == ')':
            (token, index) = read_rparen(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

def first_evaluate(tokens):  #掛け算と割り算のみ処理
    new_tokens = []
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'MULTI':
            new_tokens.append({'type' :'NUMBER','number': new_tokens.pop()['number'] * tokens[index+1]['number'] }) #new_tokensに入っている*のひとつ前の要素と*の次の要素を掛け算
            index += 2
           
        elif tokens[index]['type'] == 'DIVIDE':
            new_tokens.append({'type':'NUMBER','number':new_tokens.pop()['number'] / tokens[index+1]['number'] })  #new_tokensに入っている/のひとつ前の要素と/の次の要素を掛け算
            index += 2

        else:
            new_tokens.append(tokens[index])
            index += 1
    if new_tokens[-1]['type'] != 'NUMBER':
       new_tokens.append(tokens[-1])   #もし最後の要素が掛け算や割り算ではなかったら+や-で終わってしまっているから最後の数字をつけてあげる

    return new_tokens


def second_evaluate(tokens):  #足し算と引き算のみ処理
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    answer = 0
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer

def is_paren(tokens):
    for token in tokens:
        if token['type'] == 'LPAREN': #もし"("が存在したらTrueを返す
            return True
    return False

def search_token(tokens): 
    stack = []
    for i in range(len(tokens)):
        if tokens[i]['type'] == 'LPAREN':
            stack.append(i)
        elif tokens[i]['type'] == 'RPAREN':
            start_index = stack.pop() 
            end_index = i
            return start_index, end_index #一番内側のカッコを処理するため始めに出てきた")"と対応する"("のindexを返す



def evaluate(tokens):
    while is_paren(tokens):   #もしカッコが残っていたらカッコ内の処理を行う
        start_index,end_index = search_token(tokens)
        part_tokens = tokens[start_index+1:end_index]  #カッコ内を切り出す
        part_tokens =first_evaluate(part_tokens)
        part_answer = second_evaluate(part_tokens)
        tokens = tokens[:start_index] + [{'type':'NUMBER', 'number':part_answer}] + tokens[end_index+1:] #カッコ内の計算結果を他部分と統合
    tokens = first_evaluate(tokens) #カッコなしの文を計算
    answer = second_evaluate(tokens)
    return answer


def test(line):
    tokens= tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.0")
    test("(3+2)")
    test("2")
    test("(3.0+4*(2-1))/5")
    test("1.0*3+3/3+1")
    test("(3+2)*(5-3)/1")
    test("5+3+2*(6-2)/3")
    test("(3.0+4.2*(2.5-1.1))/5.0")
    test("(3.7+2.3)*(5.0-3.1)/1.2")
    test("5.5+3.3+2.1*(6.2-2.8)/3.0")
    test("(2.5+3.5*2.5)/(1.5-0.5)")
    test("6.6/(2.0+1.3)-4.2*1.5")
    test("8.5-(3.5/2.5)+4.5*3.0")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
