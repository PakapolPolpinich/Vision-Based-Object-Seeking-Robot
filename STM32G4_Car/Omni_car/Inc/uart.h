/*
 * uart.h
 *
 *  Created on: Feb 11, 2026
 *      Author: Admin
 */

#ifndef UART_H_
#define UART_H_


#include "stm32g4xx.h"
#include "gpio.h"

void USART2_Init(void);
void USART2_SendChar(char ch);
void USART2_SendString(char* str);

#endif /* UART_H_ */
