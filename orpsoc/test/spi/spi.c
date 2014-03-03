#include<stdio.h>

char* spi_base = (char*)  0xb0000000; // config Control Register
char* spi_base2 = (char*)  0xb0000003; // config Extension Register
char* spi_write = (char*) 0xb0000002; //write byte
char* spi_read = (char*) 0xb0000002; //read byte
char* spi_slave = (char*)  0xb0000004; //select slave

unsigned char line = 0x00; // 00(ADD2)(ADD1)(ADD0)000


int main()
{

#ifdef SIMULATOR

    printf("SPI OK\n");

#endif

#ifdef BOARD
	char data;

	int X;
	int Y;
	int Z;

	*(spi_base) = 0xFF;
	*(spi_base2) = 0xFF; 

	//X0
	*(spi_slave) = 0x01; //select slave
  	*(spi_write) = X0;
	data = *(spi_read);
	*(spi_slave) = 0x00; //select slave




#endif

return (0);
}
