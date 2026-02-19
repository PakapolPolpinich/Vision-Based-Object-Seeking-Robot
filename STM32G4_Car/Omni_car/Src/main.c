/**
 ******************************************************************************
 * @file           : main.c
 * @author         :
 * @brief          : Main program body
 ******************************************************************************

 ******************************************************************************
 */

#include "Systemclock.h"
#include "gpio.h"
#include "motor.h"
#include "encoder.h"
#include "pid.h"
#include "spi.h"

#define MOTOR_M1 2
#define MOTOR_M3 0
#define MOTOR_M4 1

extern volatile int16_t setpoint_M1;
extern volatile int16_t setpoint_M3;
extern volatile int16_t setpoint_M4;

volatile uint8_t spi_value = 0;

int main(void)
{
	/*clock 100MHz*/
	clk_init();
	/*Enable FPU*/
	SCB->CPACR |= ((3UL << 20U)|(3UL << 22U));
	/*Set output LED*/
	GPIO_pinMode(GPIOC,15,OUTPUT,LOW_SPEED,NO_PUPD,NO_AF);
	GPIO_pinMode(GPIOC,13,OUTPUT,LOW_SPEED,NO_PUPD,NO_AF);
	GPIO_pinMode(GPIOC,14,OUTPUT,LOW_SPEED,NO_PUPD,NO_AF);
	GPIO_write(GPIOC,15,HIGH);
	/*initial motor control*/
	motor_init();
	Encoder_init();
	Spi_init();
	/*Robot Stop*/
	Omnicontrol('s');

	while(1){
		Omnicontrol((char)(spi_value));
//		Omni_forward();
//		Omni_backward();
//		Omni_left();
//		Omni_right();
//		Omni_stop();
//		Omni_clockwise();
	}
}



/*Sampling every 100ms*/
void TIM7_IRQHandler(void) {
    if (TIM7->SR & TIM_SR_UIF) {
        TIM7->SR &= ~TIM_SR_UIF;

#ifdef DEBUG_PID
        sprintf(str,"receive %c prev %c check %d ",rxb,prev_rxb,check);
        sprintf(rpm," M1 : %f ",Count[2].Vrpm);
        sprintf(str," setpoint : %d  ",check);
        USART2_SendString(str);
#endif

       VelocityEn();
       rotateMotor(MOTOR_M1,pid_control(setpoint_M1, &PIDControllers[MOTOR_M1], &Count[MOTOR_M1]));
       rotateMotor(MOTOR_M3, pid_control(setpoint_M3, &PIDControllers[MOTOR_M3], &Count[MOTOR_M3]));
       rotateMotor(MOTOR_M4, pid_control(setpoint_M4, &PIDControllers[MOTOR_M4], &Count[MOTOR_M4]));
    }
}


void SPI2_IRQHandler(void){
	/* RXNE: receive not empty */
	if (SPI2->SR & SPI_SR_RXNE){
		/*read RXFIFO*/
		spi_value = (uint8_t)SPI2->DR;
	}
	if(SPI2->SR & SPI_SR_OVR){
		 (void)SPI2->DR;
		 (void)SPI2->SR;
	}
}
