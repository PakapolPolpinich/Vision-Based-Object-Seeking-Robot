/*
 * gpio.h
 *
 *  Created on: Feb 11, 2026
 *      Author: Admin
 */

#ifndef GPIO_H_
#define GPIO_H_

#include "stm32g4xx.h"

#define RCC_GPIOA		(1<<0)
#define RCC_GPIOB		(1<<1)
#define RCC_GPIOC		(1<<2)
#define RCC_GPIOD		(1<<3)
#define RCC_GPIOE		(1<<4)
#define RCC_GPIOF		(1<<5)
#define RCC_GPIOG		(1<<6)

#define INPUT					0x0
#define	OUTPUT					0x1
#define ALTERNATE_FUNCTION		0x2
#define ANALOG					0x3

#define LOW_SPEED				0x0
#define MEDIUM_SPEED			0x1
#define FAST_SPEED				0x2
#define HIGH_SPEED				0x3

#define NO_PUPD					0x0
#define PULL_UP					0x1
#define PULL_DOWN				0x2
#define RESERVED				0x3

#define AF0						0x0
#define AF1						0x1
#define AF2						0x2
#define AF3						0x3
#define AF4						0x4
#define AF5						0x5
#define AF6						0x6
#define AF7						0x7
#define AF8						0x8
#define AF9						0x9
#define AF10					0xA
#define AF11					0xB
#define AF12					0xC
#define AF13					0xD
#define AF14					0xE
#define AF15					0xF
#define NO_AF					0xFF

#define USART3_TX               AF7
#define USART3_RX               AF7

#define TIM1_CH1                AF6
#define TIM1_CH2                AF6
#define TIM1_CH3                AF6

#define TIM2_CH1                AF1 //PA0
#define TIM2_CH2                AF1 //PB3

#define TIM3_CH1                AF2
#define TIM3_CH2                AF2
#define TIM3_CH3                AF2
#define TIM3_CH4                AF2

#define TIM4_CH1                AF2 //PD12
#define TIM4_CH2                AF2 //PD13
#define TIM4_CH3                AF2
#define TIM4_CH4                AF2


#define TIM15_CH1               AF9
#define TIM15_CH2               AF9

#define TIM17_CH1				AF10

#define SPI_MOSI                AF5
#define SPI_MISO                AF5
#define SPI_SCK                 AF5
#define SPI_NSS					AF5

#define UART2_TX				AF7
#define UART2_RX				AF7

#define HIGH                    1
#define LOW                     0
void GPIO_pinMode(GPIO_TypeDef *pGPIO,uint8_t pin,uint8_t mode,uint8_t speed,uint8_t pupd,uint8_t AFRLH);

void GPIO_write(GPIO_TypeDef *pGPIO,uint8_t pin,uint8_t status);

void GPIO_Toggle(GPIO_TypeDef *pGPIO,uint8_t pin);

#endif /* GPIO_H_ */
