def write_txt(fname,content):
 fname="Document/"+fname
 try:
     fobj = open(fname, 'a',encoding='utf-8')
 except IOError:
     print('*** file open error:')
 else:
     fobj.write('\n' + str(content))
     fobj.close()
def read_txt(fname):
    f = open(fname, "r")
    lines = f.read()
    #print(lines)
    return lines
#write_txt("1.txt")
#read_txt("cookie.txt")