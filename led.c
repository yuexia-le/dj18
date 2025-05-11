#include "stm32f10x.h"                  // Device header
#include "Delay.h"  
int main(void)
{
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);	//开启时钟
	
	GPIO_InitTypeDef GPIO_InitStructure;	//定义结构体变量
	//结构体成员
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;	//推挽输出类型，高低电平均可有效驱动
//	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_OD;	//开漏输出模式，高阻态，只有低电平有驱动能力
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_2;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOA, &GPIO_InitStructure);	//完成初始化
	
//	GPIO_SetBits(GPIOA, GPIO_Pin_0);		//高电平
//	GPIO_ResetBits(GPIOA, GPIO_Pin_0);		//低电平
//	GPIO_WriteBit(GPIOA, GPIO_Pin_0, Bit_RESET);	//低电平
	GPIO_WriteBit( GPIOA, GPIO_Pin_0, Bit_SET);	//高电平
	while(1)
	{
//		GPIO_ResetBits(GPIOA, GPIO_Pin_0);
//		Delay_ms(500);
//		GPIO_SetBits(GPIOA, GPIO_Pin_0);
//		Delay_ms(500);
		
//		GPIO_WriteBit(GPIOA, GPIO_Pin_0, Bit_RESET);
//		Delay_ms(500);
//		GPIO_WriteBit(GPIOA, GPIO_Pin_0, Bit_SET);
//		Delay_ms(500);
		
		//如果想通过0和1进行闪烁需要把0和1用BitAction进行强制枚举类型转换
//		GPIO_WriteBit(GPIOA, GPIO_Pin_0, (BitAction)0);
//		Delay_ms(500);
//		GPIO_WriteBit(GPIOA, GPIO_Pin_0, (BitAction)1);
//		Delay_ms(500);
	}
}
