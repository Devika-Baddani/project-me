class Stack:
    def __init__(self):
        self.items = []
    def is_empty(self):
        return self.items == []
    def push(self,item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
    def peek(self):
        return self.items[-1]
    def size(self):
        return len(self.items)
def infix_to_postfix(infix_expr):
    prec = {}
    prec['*']=3
    prec['/']=3
    prec['-']=2
    prec['+']=2
    prec['(']=1
    op_stack = Stack()
    postfix_list = []
    token_list = infix_expr.split(' ')
    for token in token_list:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "0123456789":
            postfix_list.append(token)
        elif token == '(':
            op_stack.push(token)
        elif token==")":
            top_token = op_stack.pop()
            while top_token != '(':
                postfix_list.append(top_token)
                top_token = op_stack.pop()
        else:
            while(not op_stack.is_empty()) and (prec[op_stack.peek()]>=prec[token]):
                postfix_list.append(op_stack.pop())
            op_stack.push(token)
    while not op_stack.is_empty():
        postfix_list.append(op_stack.pop())
    return " ".join(postfix_list)
def evaluation_postfix(postfix_expr):
    operand_stack = Stack()
    postfix_list = postfix_expr.split(' ')
    result = 0
    for i in postfix_list:
        if i in "0123456789":
            operand_stack.push(int(i))
        else:
                b = operand_stack.pop()
                a = operand_stack.pop()
                if i=="+":
                    result= a+b
                elif i=="-":
                    result = a-b
                elif i=="*":
                    result = a*b
                elif i == "/":
                    result = a/b
                operand_stack.push(result)
    return result
#print(infix_to_postfix("4 + 5 * 6"))
#print(evaluation_postfix(infix_to_postfix("4 + 5 * 6")))

    

def divide_by_2(dec_number):
    rem_stack = Stack()
    while dec_number >0:
        rem = dec_number % 2
        rem_stack.push(rem)
        dec_number = dec_number//2

    bin_string = ""
    while not rem_stack.is_empty():
        bin_string = bin_string + str(rem_stack.pop())
    return bin_string



def base_converter(dec_number,base):
    digits = "0123456789ABCDEF"
    rem_stack = Stack()
    while dec_number >0:
        rem = dec_number % base
        rem_stack.push(rem)
        dec_number = dec_number//base

    new_string = ""
    while not rem_stack.is_empty():
        new_string = new_string + digits[rem_stack.pop()]
    return new_string

print(base_converter(42,2))
print(base_converter(42,16))
    
        
        
        
                
                
                
    
    
