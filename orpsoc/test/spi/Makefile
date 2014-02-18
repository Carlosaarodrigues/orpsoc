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
FLAGS_SIM = -mboard=or1ksim-uart 
FLAGS_BOARD = -mboard=de0_nano

SOURCES = spi.c
OBJECTS = $(SOURCES:.cpp=.o)
EXECUTABLE_SIM = elf_file_sim
EXECUTABLE_BOARD = elf_file_board

sim: $(EXECUTABLE_SIM)
board: $(EXECUTABLE_BOARD)

$(EXECUTABLE_BOARD): $(OBJECTS)
	$(Q)$(OR1K_CC) $(FLAGS_BOARD) $< -o $@

$(EXECUTABLE_SIM): $(OBJECTS)
	$(Q)$(OR1K_CC) $(FLAGS_SIM) $< -o $@

%.o: %.c
	$(Q)$(OR1K_CC) $(OR1K_CFLAGS) $< -o $@

clean:
	$(Q)rm -f *.o $(EXECUTABLE_SIM) $(EXECUTABLE_BOARD)

