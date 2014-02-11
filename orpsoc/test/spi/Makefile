# Set V=1 when calling make to enable verbose output
# mainly for debugging purposes.
ifeq ($(V), 1)
Q=
else
Q ?=@
endif

OR1K_TOOL_PREFIX = or1k-elf-
OR1K_CC = $(OR1K_TOOL_PREFIX)gcc
OR1K_CFLAGS = -c
FLAGS_LINK = -mboard=or1ksim-uart 

SOURCES = spi.c
OBJECTS = $(SOURCES:.cpp=.o)
EXECUTABLE = elf_file

all: $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(Q)$(OR1K_CC) $(FLAGS_LINK)$< -o $@

%.o: %.c
	$(Q)$(OR1K_CC) $(OR1K_CFLAGS) $< -o $@

clean:
	$(Q)rm -f *.o $(EXECUTABLE)


