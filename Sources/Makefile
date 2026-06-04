
CC       = gcc
CFLAGS   = -lfftw3 -lm -static -static-libgcc -static-libstdc++
CPPFLAGS = -fPIC -Wall -Wno-unused-variable

# All solver binaries (named .o to match the rest of the project)
SOLVERS  = ch2d_qualitative.o ch2d_alloy.o ch3d_alloy.o
POSTPROC = hkl_2d.o hkl_3d.o

all: $(SOLVERS) $(POSTPROC)

# CH solvers depend on the shared header, kv parser, and helper .c files
$(SOLVERS): %.o: %.c ch_common.h kv_parser.h nrutil.c gasdev.c
	$(CC) $< -o $@ $(CFLAGS) $(CPPFLAGS)

# Post-processing tools use kv_parser.h but have no FFTW dependency
hkl_2d.o: hkl_2d.c kv_parser.h
	$(CC) $< -o $@ -lm -static -static-libgcc -static-libstdc++ $(CPPFLAGS)

hkl_3d.o: hkl_3d.c kv_parser.h
	$(CC) $< -o $@ -lm -static -static-libgcc -static-libstdc++ $(CPPFLAGS)

clean:
	rm -f $(SOLVERS) $(POSTPROC)
