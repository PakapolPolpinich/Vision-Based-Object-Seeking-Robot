/*
 * encoder.h
 *
 *  Created on: Feb 11, 2026
 *      Author: Admin
 */

#ifndef ENCODER_H_
#define ENCODER_H_

#include "stm32g4xx.h"
#include "gpio.h"

void Encoder_init();

int32_t GetValueEncoder(uint8_t channel);

#endif /* ENCODER_H_ */
