#include "pwm.h"

void Pwm_init(){

	RCC->APB2ENR |= RCC_APB2ENR_TIM15EN |RCC_APB2ENR_TIM1EN |RCC_APB2ENR_TIM17EN;

	GPIO_pinMode(GPIOA,8,ALTERNATE_FUNCTION,LOW_SPEED,NO_PUPD,TIM1_CH1);/*motor1*/
	GPIO_pinMode(GPIOA,9,ALTERNATE_FUNCTION,LOW_SPEED,NO_PUPD,TIM1_CH2);

	GPIO_pinMode(GPIOB,5,ALTERNATE_FUNCTION,LOW_SPEED,NO_PUPD,TIM17_CH1);/*motor2*/
	GPIO_pinMode(GPIOA,10,ALTERNATE_FUNCTION,LOW_SPEED,NO_PUPD,TIM1_CH3);

	GPIO_pinMode(GPIOA,2,ALTERNATE_FUNCTION,LOW_SPEED,NO_PUPD,TIM15_CH1);/*motor3*/
	GPIO_pinMode(GPIOA,3,ALTERNATE_FUNCTION,LOW_SPEED,NO_PUPD,TIM15_CH2);

	/* Configure PWM Mode for TIM1 (Motor 1) */
	TIM1->CCMR1 &= ~(TIM_CCMR1_CC1S | TIM_CCMR1_CC2S);				/*set capture compare channel 1 and 2 for motor 1*/
	TIM1->CCMR2 &= ~(TIM_CCMR2_CC3S);								/*set capture compare channel 3 for motor 2*/

	TIM1->CCMR1 &= ~((0xF << 4)|(0xF<<12));							/*set zero output compare channel 1 and 2 mode */
	TIM1->CCMR1 |= ((0x6 << TIM_CCMR1_OC1M_Pos)|
					(0x6<<TIM_CCMR1_OC2M_Pos));						/*set channel 1 and 2 active as long as TIM_CNT < CCR else inactive */
	TIM1->CCMR2 &= ~(0xF << 4);										/*set zero output compare channel 3 mode */
	TIM1->CCMR2 |= 	(0x6 << TIM_CCMR2_OC3M_Pos);					/*set channel 3 active as long as TIM_CNT < CCR else inactive*/

	TIM1->CCER &= ~(TIM_CCER_CC1P | TIM_CCER_CC2P | TIM_CCER_CC3P);	/*capture compare 1,2,3 output polarity = 0 */
	TIM1->PSC = 1;													/*prescaler 1 */
	TIM1->ARR = 10000;												/*ARR 16 bit*/
	TIM1->CCMR1 |= (TIM_CCMR1_OC1PE | TIM_CCMR1_OC2PE);				/*set channel 1 and 2 output compare preload enable */
	TIM1->CCMR2 |= (TIM_CCMR2_OC3PE);								/*set channel 3 output compare preload enable */
	TIM1->CCER |= (TIM_CCER_CC1E | TIM_CCER_CC2E | TIM_CCER_CC3E);	/*capture compare 1,2 and 3 set OC signal is output on output pin (gpio pin)*/
	TIM1->BDTR |= (1<<15);
	TIM1->CR1 |= TIM_CR1_CEN;										/*Enable counter */

	/* Configure PWM Mode for TIM17 (Motor 2) */
	TIM17->CCMR1 &= ~(TIM_CCMR1_CC1S);								/*set capture compare channel 1 (cc1) as output  for motor 2*/
	TIM17->CCMR1 |= (0x6 << TIM_CCMR1_OC1M_Pos);					/*set channel 1 active as long as TIM_CNT < CCR else inactive*/
	TIM17->CCER &= ~(TIM_CCER_CC1P);								/*capture compare 1 output polarity = 0 */
	TIM17->PSC = 1;													/*prescaler 1 */
	TIM17->ARR = 10000;												/*ARR 16 bit*/
	TIM17->CCMR1 |= TIM_CCMR1_OC1PE;								/*set channel 1 output compare preload enable */
	TIM17->CCER |= TIM_CCER_CC1E;									/*capture compare 1 set OC signal is output on output pin (gpio pin)*/
	TIM17->BDTR |= (1<<15);
	TIM17->CR1 |= TIM_CR1_CEN;										/*Enable counter */

	/* Configure PWM Mode for TIM15 (Motor 3) */
	TIM15->CCMR1 &= ~(TIM_CCMR1_CC1S | TIM_CCMR1_CC2S);
	TIM15->CCMR1 &= ~((0xF << TIM_CCMR1_OC1M_Pos)|(0xF<<TIM_CCMR1_OC2M_Pos));
	TIM15->CCMR1 |= ((0x6 << TIM_CCMR1_OC1M_Pos) | (0x6 << TIM_CCMR1_OC2M_Pos));
	TIM15->CCER &= ~(TIM_CCER_CC1P | TIM_CCER_CC2P);
	TIM15->PSC = 1;
	TIM15->ARR = 10000;
	TIM15->CCMR1 |= (TIM_CCMR1_OC1PE | TIM_CCMR1_OC2PE);
	TIM15->CCER |= (TIM_CCER_CC1E | TIM_CCER_CC2E);
	TIM15->BDTR |= (1<<15);
	TIM15->CR1 |= TIM_CR1_CEN;

}


/*********************************************************************
 * @fn      		  - PWM_Setdutycycle
 * @brief             - Send PWM
 *
 * @param[in]         -	channel set channel pwm 1-4
 * @param[in]         -	compare_value 0-65535
 *
 *
 * @return            -	None
 *
 * @Note              -

 *//////////////////////////////////////////////////////////////////////

void PWM_Setdutycycle(uint8_t channel,uint16_t compare_value){
	 switch (channel) {
	        case 1: TIM1->CCR1 = compare_value; break;
	        case 2: TIM1->CCR2 = compare_value; break;
	        case 3: TIM1->CCR3 = compare_value; break;
	        case 4: TIM17->CCR1 = compare_value; break;
			case 5: TIM15->CCR1 = compare_value; break;
	        case 6: TIM15->CCR2 = compare_value; break;
		default:{
			TIM1->CCR1 	= 0; break;
			TIM1->CCR2 	= 0; break;
			TIM1->CCR3 	= 0; break;
			TIM17->CCR1 = 0; break;
			TIM15->CCR1 = 0; break;
			TIM15->CCR2 = 0; break;
		}
	    }
}
