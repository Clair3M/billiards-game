CC = clang
CFLAGS = -Wall -std=c99 -pedantic

all: _phylib.so

_phylib.so: phylib_wrap.o
	$(CC) $(CFLAGS) -shared phylib_wrap.o -L. -L/opt/homebrew/opt/python@3.12/Frameworks/Python.framework/Versions/3.12/lib -lpython3.12 -lphylib -o $@

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c -fPIC $^ -I/opt/homebrew/opt/python@3.12/Frameworks/Python.framework/Versions/3.12/include/python3.12 -o $@

phylib_wrap.c phylib.py: phylib.i libphylib.so
	swig -python phylib.i > $@

libphylib.so: phylib.o phylib.h
	$(CC) $(CFLAGS) -shared phylib.o -lm -o $@

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -fPIC -c phylib.c -o $@

clean:
	rm *.o *.so

double_clean:
	make clean
	rm phylib_wrap.c phylib.py
