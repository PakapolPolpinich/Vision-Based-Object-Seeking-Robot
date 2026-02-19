#include "uart.h"
#include "stm32g4xx.h"

void USART2_Init(void)
{

	GPIO_pinMode(GPIOB,3,ALTERNATE_FUNCTION,LOW_SPEED,NO_PUPD, UART2_TX);
	GPIO_pinMode(GPIOB,4,ALTERNATE_FUNCTION,LOW_SPEED,NO_PUPD, UART2_RX);

	RCC->APB1ENR1 |= RCC_APB1ENR1_USART2EN;

    // Configure USART3
    USART2->CR1 &= ~USART_CR1_UE;  // Disable USART3 to configure

    // Set baud rate
    USART2->BRR = 0x364; //set baudrate 100000000/115200

    // Enable transmitter and receiver
    USART2->CR1 |= USART_CR1_TE | USART_CR1_RE ;
  //  USART2->CR1 |= USART_CR1_TE | USART_CR1_RE |USART_CR1_RXNEIE_RXFNEIE;

    // Enable USART3
    USART2->CR1 |= USART_CR1_UE;
//    NVIC_EnableIRQ(USART2_IRQn);
//    NVIC_SetPriority(USART2_IRQn,1);
}

void USART2_SendChar(char ch)
{
    while (!(USART2->ISR & (1<<7)));// Wait until TXFNF is set
    USART2->TDR = ch & (uint8_t)0xFF;
}

void USART2_SendString(char* str)
{
    while (*str)
    {
        USART2_SendChar(*str++);
    }
    while (!(USART2->ISR & (1<<6)));
}
