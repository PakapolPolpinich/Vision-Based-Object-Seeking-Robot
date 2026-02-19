################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Src/Systemclock.c \
../Src/encoder.c \
../Src/gpio.c \
../Src/main.c \
../Src/motor.c \
../Src/pid.c \
../Src/pwm.c \
../Src/spi.c \
../Src/syscalls.c \
../Src/sysmem.c \
../Src/uart.c 

OBJS += \
./Src/Systemclock.o \
./Src/encoder.o \
./Src/gpio.o \
./Src/main.o \
./Src/motor.o \
./Src/pid.o \
./Src/pwm.o \
./Src/spi.o \
./Src/syscalls.o \
./Src/sysmem.o \
./Src/uart.o 

C_DEPS += \
./Src/Systemclock.d \
./Src/encoder.d \
./Src/gpio.d \
./Src/main.d \
./Src/motor.d \
./Src/pid.d \
./Src/pwm.d \
./Src/spi.d \
./Src/syscalls.d \
./Src/sysmem.d \
./Src/uart.d 


# Each subdirectory must supply rules for building sources it contributes
Src/%.o Src/%.su Src/%.cyclo: ../Src/%.c Src/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DSTM32 -DSTM32G4 -DSTM32G441CBTx -DSTM32G441xx -c -I../Inc -I"C:/Users/Admin/Documents/python_ai/Final_project/Vision-Based-Object-Seeking-Robot/STM32G4_Car/LibCMSIS/CMSIS/Include" -I"C:/Users/Admin/Documents/python_ai/Final_project/Vision-Based-Object-Seeking-Robot/STM32G4_Car/LibCMSIS/CMSISG4/CMSIS/Device/ST/STM32G4xx/Include" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Src

clean-Src:
	-$(RM) ./Src/Systemclock.cyclo ./Src/Systemclock.d ./Src/Systemclock.o ./Src/Systemclock.su ./Src/encoder.cyclo ./Src/encoder.d ./Src/encoder.o ./Src/encoder.su ./Src/gpio.cyclo ./Src/gpio.d ./Src/gpio.o ./Src/gpio.su ./Src/main.cyclo ./Src/main.d ./Src/main.o ./Src/main.su ./Src/motor.cyclo ./Src/motor.d ./Src/motor.o ./Src/motor.su ./Src/pid.cyclo ./Src/pid.d ./Src/pid.o ./Src/pid.su ./Src/pwm.cyclo ./Src/pwm.d ./Src/pwm.o ./Src/pwm.su ./Src/spi.cyclo ./Src/spi.d ./Src/spi.o ./Src/spi.su ./Src/syscalls.cyclo ./Src/syscalls.d ./Src/syscalls.o ./Src/syscalls.su ./Src/sysmem.cyclo ./Src/sysmem.d ./Src/sysmem.o ./Src/sysmem.su ./Src/uart.cyclo ./Src/uart.d ./Src/uart.o ./Src/uart.su

.PHONY: clean-Src

