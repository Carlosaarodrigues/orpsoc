# Set V=1 when calling make to enable verbose output
# mainly for debugging purposes.
ifeq ($(V), 1)
Q=
else
Q ?=@
endif

OR1K_TOOL_PREFIX = or1k-elf-
OR1K_CC = $(OR1K_TOOL_PREFIX)gcc
OR1K_CFLAGS = -c -Wall

SOURCES = hello.c
OBJECTS = $(SOURCES:.cpp=.o)
EXECUTABLE = elf_file

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(Q)$(OR1K_CC) $< -o $@

%.o: %.cpp
	$(Q)$(OR1K_CC) $(OR1K_CFLAGS) $< -o $@

clean:
	$(Q)rm -f *.o $(EXECUTABLE)


