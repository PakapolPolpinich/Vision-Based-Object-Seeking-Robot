/*
 * spi.c
 *
 *  Created on: Feb 12, 2026
 *      Author: Admin
 */

#include "spi.h"

void Spi_init(){
	//GPIO
	GPIO_pinMode(GPIOB,12,ALTERNATE_FUNCTION,HIGH_SPEED,PULL_UP,SPI_NSS);
	GPIO_pinMode(GPIOB,13,ALTERNATE_FUNCTION,HIGH_SPEED,NO_PUPD,SPI_SCK);
	GPIO_pinMode(GPIOB,14,ALTERNATE_FUNCTION,HIGH_SPEED,NO_PUPD,SPI_MISO);
	GPIO_pinMode(GPIOB,15,ALTERNATE_FUNCTION,HIGH_SPEED,NO_PUPD,SPI_MOSI);

	RCC->APB1ENR1 |= RCC_APB1ENR1_SPI2EN;
	 /* Disable SPI before config */
	SPI2->CR1 &= ~SPI_CR1_SPE;

	SPI2->CR1 &= ~(SPI_CR1_BR | SPI_CR1_LSBFIRST | SPI_CR1_MSTR); // msb,slave config
	SPI2->CR1 &= ~(SPI_CR1_CPOL | SPI_CR1_CPHA); // mode 0
	SPI2->CR1 &= ~(SPI_CR1_SSM); /*use NSS pin (handware CS)*/
	//SPI2->CR1 |= (0x3 << SPI_CR1_BR_Pos); /*baudrate 100/16 = 6.25 MHz */
	SPI2->CR1 |= (0x1 << SPI_CR1_RXONLY_Pos); /*Rxonly not full duplex*/

    SPI2->CR2 &= ~(0xF << SPI_CR2_DS_Pos);
    SPI2->CR2 |= (0x7 << SPI_CR2_DS_Pos); //data 8bit
    /*// RX interrupt and RXNE event generate if FIFO equal 1/4 (8bit)*/
    SPI2->CR2 |= SPI_CR2_RXNEIE | SPI_CR2_FRXTH | SPI_CR2_ERRIE;

    /* Enable NVIC */
    NVIC_EnableIRQ(SPI2_IRQn);
    NVIC_SetPriority(SPI2_IRQn, 3);

    /* Enable SPI */
    SPI2->CR1 |= SPI_CR1_SPE;
}


