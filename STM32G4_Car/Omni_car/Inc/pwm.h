/*
 * pwm.h
 *
 *  Created on: Feb 11, 2026
 *      Author: Admin
 */

#ifndef PWM_H_
#define PWM_H_

#include"stm32g4xx.h"
#include "gpio.h"

void Pwm_init();

void PWM_Setdutycycle(uint8_t channel,uint16_t compare_value);


#endif /* PWM_H_ */
