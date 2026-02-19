

#include"motor.h"


#define stop		's'
#define forward		'f'
#define left		'l'
#define right		'r'
#define backward	'b'
#define CLOCKWISE	'c'

volatile int16_t setpoint_M1;
volatile int16_t setpoint_M3;
volatile int16_t setpoint_M4;

struct motor_pin {
	volatile uint32_t* ln1;
	volatile uint32_t* ln2;
};

struct motor_pin motorPin[] = {
		{&(TIM1->CCR1),&(TIM1->CCR2)},	//M3
		{&(TIM17->CCR1),&(TIM1->CCR3)}, //M4
        {&(TIM15->CCR1),&(TIM15->CCR2)} //M1
};

void motor_init(){
	Pwm_init();
	Timer7_init();
	Timer6_init();
}

/*********************************************************************
 * @fn      		  - rotateMotor
 * @brief             - set speed for motor left and right
 *
 * @param[in]         -	channel 0-1 motor left and right
 * @param[in]         -	speed motor left and right
 *
 * @return            -	None
 *
 * @Note              -

 *//////////////////////////////////////////////////////////////////////
void rotateMotor(uint8_t channel, int32_t speed){
	if (speed > 0) {
	        *(motorPin[channel].ln1) = (uint32_t)speed; // Forward
	        *(motorPin[channel].ln2) = 0;
	    } else if (speed < 0) {
	        *(motorPin[channel].ln1) = 0;
	        *(motorPin[channel].ln2) = (uint32_t)abs(speed); // Reverse
	    } else {
	        *(motorPin[channel].ln1) = 0; // Stop
	        *(motorPin[channel].ln2) = 0;
	    }
}



void Omni_forward(){
	setpoint_M1 = 26;
	setpoint_M3 = -26;
	setpoint_M4 = 0;
}

void Omni_backward(){
	setpoint_M1 = -26;
	setpoint_M3 = 26;
	setpoint_M4 = 0;
}

void Omni_left(){
	setpoint_M1 = 26;
	setpoint_M3 = 26;
	setpoint_M4 = -52;
}

void Omni_right(){
	setpoint_M1 = -26;
	setpoint_M3 = -26;
	setpoint_M4 = 52;
}

void Omni_stop(){
	setpoint_M1 = 0;
	setpoint_M3 = 0;
	setpoint_M4 = 0;
}


void Omni_clockwise(){
	setpoint_M1 = 26;
	setpoint_M3 = 26;
	setpoint_M4 = 26;
}

void Omnicontrol(char receive_spi){
	switch (receive_spi)
	{
	case stop:		Omni_stop();		break;
	case forward:	Omni_forward();		break;
	case backward:	Omni_backward();	break;
	case left:		Omni_left();		break;
	case right:		Omni_right();		break;
	case CLOCKWISE: Omni_clockwise();	break;

	default:
		Omni_stop();
		break;
	}
}



void Timer7_init(){

	 RCC->APB1ENR1 |= RCC_APB1ENR1_TIM7EN;


	 TIM7->PSC = 999;
	 TIM7->ARR = 9999;

	 // Enable update interrupt
	 TIM7->DIER |= TIM_DIER_UIE;

	 // Enable TIM16
	 TIM7->CR1 |= TIM_CR1_CEN;


	 NVIC_EnableIRQ(TIM7_IRQn);
	 NVIC_SetPriority(TIM7_IRQn,2);
}
void Timer6_init(){

	 RCC->APB1ENR1 |= RCC_APB1ENR1_TIM6EN;


	 TIM6->PSC = 19999;
	 TIM6->ARR = 14999;

	 // Enable update interrupt
	 TIM6->DIER |= TIM_DIER_UIE;

	 // Disable TIM16
	 TIM6->CR1 &= ~TIM_CR1_CEN;

	 NVIC_EnableIRQ(TIM6_DAC_IRQn);
	 NVIC_SetPriority(TIM6_DAC_IRQn,3);
}

