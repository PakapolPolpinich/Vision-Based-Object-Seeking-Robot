#include"Systemclock.h"


void clk_init(){

	/* Enable Power Voltage Scale 1 */
		PWR->CR1 |= PWR_CR1_VOS;

	    /* Enable HSE */
	    RCC->CR |= RCC_CR_HSEON;
	    while (!(RCC->CR & RCC_CR_HSERDY));  // Wait until HSE is stable

	    /* Disable PLL before configuration */
	    RCC->CR &= ~RCC_CR_PLLON;
	    while (RCC->CR & RCC_CR_PLLRDY);  // Wait until PLL is OFF

	    /*Input (((24MHz/3)x25)/2) = 100MHz*/
	    /* Configure PLL */
	    RCC->PLLCFGR = (2    << RCC_PLLCFGR_PLLM_Pos) 	|  /*PLLM DIV 3*/
	                   (25   << RCC_PLLCFGR_PLLN_Pos) 	|  /*PLLN x25*/
					   (2    << RCC_PLLCFGR_PLLPDIV_Pos)|  /*PLLR DIV 2*/
	                   (0b00 << RCC_PLLCFGR_PLLR_Pos) 	|  // PLLR = 2
	                   (1    << RCC_PLLCFGR_PLLREN_Pos) | // Enable PLLR
	                   //(1 << RCC_PLLCFGR_PLLQEN_Pos) | // Enable PLLQ
	                   (0b00 << RCC_PLLCFGR_PLLQ_Pos);    // PLLQ = 4

	    /* Select HSE as PLL source */
	    RCC->PLLCFGR |= RCC_PLLCFGR_PLLSRC_HSE; // Set HSE as PLL source

	    /* Enable PLL */
	    RCC->CR |= RCC_CR_PLLON;
	    while (!(RCC->CR & RCC_CR_PLLRDY));  // Wait until PLL is stable

	    /* Configure Flash Latency */
	    FLASH->ACR &= ~FLASH_ACR_LATENCY;
	    FLASH->ACR |= FLASH_ACR_LATENCY_3WS; // Set Flash latency

	    /* Select PLL as System Clock */
	    RCC->CFGR &= ~RCC_CFGR_SW;
	    RCC->CFGR |= RCC_CFGR_SW_PLL;

	    /* Wait until PLL is used as System Clock */
	    while ((RCC->CFGR & RCC_CFGR_SWS) != RCC_CFGR_SWS_PLL); /*100MHz*/
	}
