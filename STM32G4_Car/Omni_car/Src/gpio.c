/*
 * gpio.c
 *
 *  Created on: Feb 11, 2026
 *      Author: Admin
 */

#include "gpio.h"

void GPIO_pinMode(GPIO_TypeDef *pGPIO,uint8_t pin,uint8_t mode,uint8_t speed,uint8_t pupd,uint8_t AFRLH){
		static uint16_t clock = 0;
		GPIO_TypeDef * gpio_ports[] = {GPIOA,GPIOB,GPIOC,GPIOD,GPIOE,GPIOF,GPIOG};
		uint32_t gpio_enable_bits[] = {RCC_GPIOA, RCC_GPIOB, RCC_GPIOC, RCC_GPIOD, RCC_GPIOE, RCC_GPIOF,RCC_GPIOG};

		for (uint8_t i = 0; i <= 6; i++) {
		     if (pGPIO == gpio_ports[i] && !(clock & gpio_enable_bits[i])) {
		          RCC->AHB2ENR |= gpio_enable_bits[i];
		          clock |= gpio_enable_bits[i];
		          break;
		     	 }
		     }
		pGPIO->MODER	&= 	~(0x3 << (pin*2));
		pGPIO->MODER 	|= 	(mode << (pin*2));

		pGPIO->OSPEEDR 	&= 	~(0x3 << (pin*2));
		pGPIO->OSPEEDR 	|= 	(speed << (pin*2));
		pGPIO->PUPDR 	&= 	~(0x3 << (pin*2));
		pGPIO->PUPDR 	|= 	(pupd << (pin*2));

		if(mode == 0x2){
			pGPIO->AFR[pin/8] &= ~(0xF << ((pin%8)*4));
			pGPIO->AFR[pin/8] |= (AFRLH << ((pin%8)*4));
		}

	}



void GPIO_write(GPIO_TypeDef *pGPIO,uint8_t pin,uint8_t status){

	if(status == 1){
		pGPIO->ODR |= (1 << pin);
	}else{
		pGPIO->ODR &= ~(1 << pin);
	}

}

void GPIO_Toggle(GPIO_TypeDef *pGPIO,uint8_t pin){

	pGPIO->ODR ^= (1 << pin);

}
