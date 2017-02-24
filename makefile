#phony target.
current_target: main


#Compiler flags
#CXXFLAGS = -O0 -Wall -ggdb
CXXFLAGS = -O2 -fpic
#Linker flags
#LDFLAGS = -O0 -Wall -ggdb
LDFLAGS = -O2


#Modules
main.o: main.cpp visilibity.hpp
visilibity.o: visilibity.cpp visilibity.hpp


#Executables
main: main.o visilibity.o
	g++ -o main $(CXXFLAGS) main.o visilibity.o


clean:   
	rm main *~ *.o *.do *.db
	clear
	pwd
	ls

.SECONDARY:
python: _visilibity.so

%_wrap.cxx: %.i $(FILES_H)
	swig -Wall -python -c++ $<
%_wrap.o: %_wrap.cxx
	$(CXX) -fPIC $(INCLUDE) -c $<  `python2.7-config --cflags`

_%.so: %_wrap.o
ifeq ($(OS), Darwin)
	$(CXX) -fpic -Wall -dynamiclib  $< visilibity.o $(LDFLAGS) `python2.7-config --ldflags` -o $@
else
	$(CXX) -fpic -Wall -shared  $< visilibity.o $(LDFLAGS) `python2.7-config --ldflags` -o $@
endif
