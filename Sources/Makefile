
CC				=	gcc
CFLAGS			=	-L/usr/local/fftw/lib  -lfftw3 -lm -static -static-libgcc -static-libstdc++
CPPFLAGS		=	-fPIC


output_objects 	=	ch2d_alloy.o ch3d_alloy.o ch2d_qualitative.o hkl_2d.o hkl_3d.o

all: $(output_objects) 
$(output_objects): %.o: %.c
	$(CC) -w $< -o $@ $(CFLAGS) $(CPPFLAGS) 

clean:
	rm *.o 