# Project: 项目1
# Makefile created by Dev-C++ 5.10

CPP      = g++
CC       = gcc
WINDRES  = windres.exe
OBJ      = Stack.o main.o
LINKOBJ  = main.o Stack.o
LIBS     = -L"/mnt/Documents/100-语言/S6-C/1-C_code/0-数据结构/2-堆栈/顺序存储结构的栈/Stack"
INCS     = -I"/mnt/Documents/100-语言/S6-C/1-C_code/0-数据结构/2-堆栈/顺序存储结构的栈/Stack"

path = /mnt/Documents/100-语言/S6-C/1-C_code/0-数据结构/2-堆栈/顺序存储结构的栈/Stack/

BIN      = rode

RM       = rm -f

.PHONY: all all-before all-after clean clean-custom

all: all-before $(BIN) all-after

clean: clean-custom
	${RM} $(OBJ) $(BIN) 


#$(BIN): main.o
#	echo("静态库的链接\n")
#	#export LD_LIBRARY_PATH=$(path):$LD_LIBRARY_PATH
#	sudo $(CC) main.o $(INCS) $(LIBS) -lStack -o $(BIN) 

$(BIN): $(OBJ)
	$(CC) main.o Stack.o $(INCS) -o $(BIN) 	
	#此处的头文件，用于拼接两个ｃ文件 $(LIBS) -lStack

main.o: main.c 
	$(CC) -c main.c -o main.o $(INCS)  

Stack.o: $(path)/Stack.c
	$(CC) -c $(path)/Stack.c -o Stack.o $(INCS)

