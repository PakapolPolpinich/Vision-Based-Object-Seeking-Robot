/*
 * motor.h
 *
 *  Created on: Feb 11, 2026
 *      Author: Admin
 */

#ifndef MOTOR_H_
#define MOTOR_H_

#include "stm32g4xx.h"
#include "pwm.h"
#include <stdlib.h>

#define MOTOR_P1    2
#define MOTOR_P4    1
#define MOTOR_P3    0

void motor_init();
void rotateMotor(uint8_t channal, int32_t speed);
void Timer7_init();
void Timer6_init();
void Omni_forward();
void Omni_backward();
void Omni_left();
void Omni_right();
void Omni_stop();
void Omni_clockwise();

void Omnicontrol(char receive_spi);

#endif /* MOTOR_H_ */
