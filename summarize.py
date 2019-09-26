file_name = "/Users/jenny/Downloads/doc3"
summary_file_name = "/Users/jenny/Downloads/doc4"

f = open(file_name, "r")
  
num_of_lines = 0
dictn = {}
while (True):
    line = f.readline()

    if (line == ''):
        print("end of the file")
        break
    
    dictn[num_of_lines] = line
    num_of_lines += 1
    print(num_of_lines, line)
f.close()


f = open(summary_file_name, "w") #overwrite
f.write(dictn[0])

f.write(dictn[num_of_lines - 1])
f.close()
