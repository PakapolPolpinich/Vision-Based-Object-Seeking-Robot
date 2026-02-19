/*
 * pid.h
 *
 *  Created on: Feb 11, 2026
 *      Author: Admin
 */

#ifndef PID_H_
#define PID_H_

#include "stm32g4xx.h"
#include "encoder.h"

#include <stdint.h>

// Define MAX_VRPM if it's missing
#define MAX_VRPM 143.357f

// Struct for PID control parameters
typedef struct {
	float kp;
	float ki;
	float kd;
	float integral;
	float previousError;
	uint8_t state;
} PIDControl;

// Struct for velocity tracking
typedef struct {
	 float Pulse;
	 float PrevPulse;
	 float Vrpm;
} Velocity;

// Declare the arrays externally
extern PIDControl PIDControllers[3];
extern Velocity Count[3];

// PID control function prototype
int32_t pid_control(int16_t setpoint, PIDControl* pid, Velocity* rpm);
void VelocityEn(void);

#endif /* PID_H_ */
