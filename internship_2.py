def extract_data(filename):
    file = open(filename,"r")
    data = []
    for line in file:
        line = line.strip().strip("<").strip(">")
        data.append(line)
        print(line)
    return data

def xml_to_tree(filename):
    data = extract_data(filename)
    tree = []
    depth = 0
    index = 0
    carry_over = []
    contain_slash = False
    inline = False
    for i in range(2, len(data)):
        print()
        print(i)
        #print("Current Tree--------", tree)
        if is_inline_element(data[i]):
            inline = True
            print("data[i] = ",data[i])
            line = is_inline_element(data[i])
        else:
            inline = False
            line = data[i]  
            line = replace_space(line)
            line = line.split()
            line = replace_underscore(line)
            
        print("Carry over = ", carry_over ,"depth = ", depth, "index = ", index, inline)
        contain_slash = search_slash(data[i])

        if(len(line) > 2 ):
            depth += 1

        if contain_slash and make_node(line) == []:
            index += 1
            depth -= 1
            if carry_over and depth == 0:
                if tree == []:
                    tree = [carry_over]
                else:
                    print("appending carry over to tree---------------------------")
                    tree.append(carry_over)
                    carry_over = []
            print("exit")
            continue
        
        if contain_slash and not inline:
            depth -= 1
            if depth <= 0:
                index += 1
                
        if contain_slash and len(line) <= 1 and carry_over:
            carry_over = []
            print("reset carry over---------------------------")
 
        elif len(line) == 1 and not inline and not contain_slash:
            print("carrying over----------------------", line)
            carry_over = line
            depth += 1
            continue
        print("line" , line)
            
        if tree == [] and not carry_over:
            tree = [make_node(line)]
        
        elif carry_over and (depth > 0 or inline):
            print("appending to carry over---------------------------")
            carry_over.append(make_node(line))
            
        elif len(tree) - 1 == index :
            print("appending to index ---------------------------")
            tree[index].append(make_node(line))          

        else:
            print("appending to tree ---------------------------")
            tree.append(make_node(line))
                
    return tree
        
        
def search_slash(string):
    for i in string:
        if i == "/":
            return True
    return False

def is_inline_element(string):
    first_delim = False
    word = ''
    for i in string:
        if first_delim and i != "<":
            word += i
        if i == ">":
            first_delim = True
        elif first_delim and i == "<":
            print("is_inline_element")
            print([string.split(">")[0],'"' + word + '"'])
            return [string.split(">")[0], '"' + word + '"']
    return False
            
def replace_space(string):
    replace = False
    new_string = ""

    for i in range(len(string)):
        if string[i] == ' ' and replace:
            new_string += '_'
        else:
            new_string += string[i] 
            
        if replace and string[i] == '"':
            replace = False
        elif not replace and string[i] == '"':
            replace = True
    if(DEBUG):
        print("new String ---------", new_string)
    return new_string

def replace_underscore(lst):
    replace = False
    new_list = []
    new_string = ""
    
    for string in lst:
        new_string = ""
        if string[len(string) - 1] == '"':
            for i in range(len(string)):
                if string[i] == '_':
                    new_string += ' '
                else:
                    new_string += string[i]
            replace = True
            new_list.append(new_string)
        else:
            new_list.append(string)
    print("new list ---------", new_list)
    return new_list
            
    
    
        
def make_node(arr):
    if len(arr) == 2:
        return arr
    node = [arr[0]]
    for i in range(1,len(arr)):
        node.append(arr[i].split("="))
    
    if node[len(node) - 1][0] ==  '/':
        node.pop(len(node) - 1)
    print(node)
    return node
       
def treeToJson(lst, depth , size, flag, s_flag, f):
    
    if len(lst) == 2 and type(lst[1]) != list:
 
        f.write("\n" + "  " * (depth + 1 ) + '"' +lst[0] + '"' + ":  " + lst[1]  )
    
        if flag == "last":
            f.write("\n" + "  " * depth + "}")
        if s_flag and depth > 2:
            f.write("\n" + "  " * (depth - 1) + "}")
            
        if (flag == "mid" or flag == "first"):
            f.write(",")
        return
    
    if type(lst[0]) == list:
        f.write("{")
        
    if type(lst) == str:
        if flag != "first" and not s_flag and depth == 2:
            f.write("," )
        f.write("\n" + "  " * depth + '"' +lst + '"' + ":  " )
        if size:
            f.write("{")
            

    if type(lst) == list:
        for i in range(len(lst)):
            #print("recursion: ", node, "---------------------------------------------")
            if (flag == "last" and i == len(lst) - 1) or flag == "head" and i == 0:
                s_flag = True
            else:
                s_flag = False
                
            if i == len(lst) - 1:
                new_flag = "last"
            elif i == 1:
                new_flag = "first"
            elif i == 0:
                new_flag = "head"
            else:
                new_flag = "mid"
            treeToJson(lst[i], depth + 1, len(lst), new_flag, s_flag, f)

def treeToJson_Debug(lst, depth , size, flag, s_flag, f):
    if len(lst) == 2 and type(lst[1]) != list and type(lst) != str:
 
        print("\n" + "  " * (depth + 1 ) + '"' +lst[0] + '"' + ":  " + lst[1]  ,end ="")
    
        if flag == "last":
            print("\n" + "  " * depth + "}",end ="")
        if s_flag and depth > 2:
            print("\n" + "  " * (depth - 1) + "}",end ="")
            
        if (flag == "mid" or flag == "first"):
            print(",",end ="")
        return
    
    if type(lst[0]) == list:
        print("{",end ="")
        
    if type(lst) == str:
        if flag != "first" and not s_flag and depth == 2:
            print("," ,end ="")
        print("\n" + "  " * depth + '"' +lst + '"' + ":  " ,end ="")
        if size:
            print("{",end ="")
            

    if type(lst) == list:
        for i in range(len(lst)):
            #print("recursion: ", lst[i], "---------------------------------------------")
            if (flag == "last" and i == len(lst) - 1) or flag == "head" and i == 0:
                s_flag = True
            else:
                s_flag = False
                
            if i == len(lst) - 1:
                new_flag = "last"
            elif i == 1:
                new_flag = "first"
            elif i == 0:
                new_flag = "head"
            else:
                new_flag = "mid"
            treeToJson_Debug(lst[i], depth + 1, len(lst), new_flag, s_flag, f)
        
  
    

DEBUG = 0
filename1, filename2 = input().split()
tree = xml_to_tree(filename1)
if DEBUG:
    print('---------------ELement in Jack the tree--------------------')
    print(tree)
    for i in tree:
        if i:
            for k in i:
                print(k)
    print(tree)

output_stream = open(filename2, 'w')
treeToJson(tree, 0 , len(tree), "none", False, output_stream )
if DEBUG:
    treeToJson_Debug(tree, 0 , len(tree), "none", False, output_stream)
else: 
    treeToJson(tree, 0 , len(tree), "none", False, output_stream )
output_stream.write("\n}")
output_stream.close()

            

