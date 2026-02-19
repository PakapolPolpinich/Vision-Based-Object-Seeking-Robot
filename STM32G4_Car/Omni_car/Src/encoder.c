
#include"encoder.h"

volatile int32_t encoder_count[3] = {0, 0, 0}; // Software counter for 32-bit extension
 void Encoder_init(void){

	GPIO_pinMode(GPIOA,0,ALTERNATE_FUNCTION,LOW_SPEED,NO_PUPD,TIM2_CH1);
	GPIO_pinMode(GPIOA,1,ALTERNATE_FUNCTION,LOW_SPEED,NO_PUPD,TIM2_CH2);

	GPIO_pinMode(GPIOA,6,ALTERNATE_FUNCTION,LOW_SPEED,NO_PUPD,TIM3_CH1);
	GPIO_pinMode(GPIOA,7,ALTERNATE_FUNCTION,LOW_SPEED,NO_PUPD,TIM3_CH2);

	GPIO_pinMode(GPIOB,6,ALTERNATE_FUNCTION,LOW_SPEED,NO_PUPD,TIM4_CH1);
	GPIO_pinMode(GPIOB,7,ALTERNATE_FUNCTION,LOW_SPEED,NO_PUPD,TIM4_CH2);

	RCC->APB1ENR1 |= (0x7 << 0); /*enable timer 2,3,4*/

	TIM2->CCMR1 |= TIM_CCMR1_CC1S_0|TIM_CCMR1_CC2S_0;// input capture mode
	TIM3->CCMR1 |= TIM_CCMR1_CC1S_0|TIM_CCMR1_CC2S_0;
	TIM4->CCMR1 |= TIM_CCMR1_CC1S_0|TIM_CCMR1_CC2S_0;


	TIM2->CCER &= ~(TIM_CCER_CC1P | TIM_CCER_CC2P); // Non-inverted signals signal read for timer  = signal for encoder
	TIM3->CCER &= ~(TIM_CCER_CC1P | TIM_CCER_CC2P); // Non-inverted signals
	TIM4->CCER &= ~(TIM_CCER_CC1P | TIM_CCER_CC2P); // Non-inverted signals

	TIM2->SMCR |= TIM_SMCR_SMS_0 | TIM_SMCR_SMS_1;//set x4 encoder
	TIM3->SMCR |= TIM_SMCR_SMS_0 | TIM_SMCR_SMS_1;
	TIM4->SMCR |= TIM_SMCR_SMS_0 | TIM_SMCR_SMS_1;


	TIM3->DIER |= TIM_DIER_UIE;
	TIM4->DIER |= TIM_DIER_UIE;


	NVIC_EnableIRQ(TIM3_IRQn);
	NVIC_EnableIRQ(TIM4_IRQn);

	// Ensure non-inverted configuration for complementary signals
	TIM2->CR1 |= TIM_CR1_CEN;
	TIM3->CR1 |= TIM_CR1_CEN;
	TIM4->CR1 |= TIM_CR1_CEN;


}

/*********************************************************************
 * @fn      		  - GetValueEncoder
 * @brief             - receive value for encoder
 *
 * @param[in]         -	channel receive value for encoder TIM1 or TIM2
 *
 *
 * @return            -	None
 *
 * @Note              -

 *//////////////////////////////////////////////////////////////////////

int32_t GetValueEncoder(uint8_t channel){
	switch (channel) {
				case 0: return (encoder_count[2] & 0xFFFF0000) | TIM4->CNT; //M3
		        case 1: return (int32_t)(TIM2->CNT); //M4
		        case 2: return (encoder_count[1] & 0xFFFF0000) | TIM3->CNT; //M1
	}
	return 0;
}


void TIM3_IRQHandler(void) {
    if (TIM3->SR & TIM_SR_UIF) {
        TIM3->SR &= ~TIM_SR_UIF;
        if (TIM3->CR1 & TIM_CR1_DIR)
            encoder_count[1] -= 65536;
        else
            encoder_count[1] += 65536;
    }
}

void TIM4_IRQHandler(void) {
    if (TIM4->SR & TIM_SR_UIF) {
        TIM4->SR &= ~TIM_SR_UIF;
        if (TIM4->CR1 & TIM_CR1_DIR)
            encoder_count[2] -= 65536;
        else
            encoder_count[2] += 65536;
    }
}
