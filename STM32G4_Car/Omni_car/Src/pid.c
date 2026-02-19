/*
 * pid.c
 *
 *  Created on: Feb 11, 2026
 *      Author: Admin
 */

#include "pid.h"
#include "uart.h"
#include "stdio.h"

#define INTEGRAL_GAIN_MAX 49000.0f
#define INTEGRAL_GAIN_MIN -49000.0f

char rpm[500];
char pi[1000];


PIDControl PIDControllers[3] = {
    {0.0868f, 0.002698f, 2.0f, 0, 0, 0},//M3 perfect
    {0.0739f, 0.002686f, 2.0f, 0, 0, 0},//M4
    {0.0869f, 0.002697f, 0, 0, 0, 0}	//M1
};

// Velocity tracking
Velocity Count[3] = {
    {0, 0, 0},
    {0, 0, 0},
    {0, 0, 0}
};


float ChangetoRPM(long Pulse, uint8_t i) {
  float Vrpm = (((float)Pulse) - Count[i].PrevPulse) * 0.21428571;
  Count[i].PrevPulse = (float)Pulse;
  return Vrpm;
}

void VelocityEn(){
	for(uint8_t i = 0;i <= 2;i++){
		Count[i].Pulse = GetValueEncoder(i);
		Count[i].Vrpm = ChangetoRPM(Count[i].Pulse,i);
	}
//	sprintf(rpm,"M1 :%f  M3 :%f   M4 : %f  \r\n ",Count[2].Vrpm,Count[0].Vrpm,Count[1].Vrpm);
//	sprintf(rpm," M3 : %f ",Count[0].Vrpm);
//	USART2_SendString(rpm);

}

int32_t pid_control(int16_t setpoint,PIDControl * pid,Velocity * rpm){

		if ((setpoint > 0 && pid->state == 1) || (setpoint < 0 && pid->state == 0)) {
		        pid->integral = 0;
		        pid->state = setpoint > 0 ? 0 : 1;
		}

		float error = (float)setpoint - rpm->Vrpm;

		pid->integral += (error * 100); /*every 100ms*/


		/*Anti- windup*/
		if(pid->integral > INTEGRAL_GAIN_MAX){

			pid->integral = INTEGRAL_GAIN_MAX;

		}else if (pid->integral < INTEGRAL_GAIN_MIN){

			pid->integral = INTEGRAL_GAIN_MIN;

		}

		float derivative = (error - pid->previousError) / 100;

		float u = (pid->kp * error + pid->ki * pid->integral + pid->kd * derivative);

		pid->previousError = error;




		int32_t pwm = (int32_t)(u * 10000.0f) /MAX_VRPM;

		if (pwm > 10000) {
		    pwm = 10000;
		  } else if (pwm < -10000) {
		    pwm = -10000;
		  }

//		sprintf(pi," setpoint : %f \r\n ",pid->integral);
//		USART2_SendString(pi);

		return pwm;
}
