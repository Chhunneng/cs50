#include <cs50.h>
#include <stdio.h>

long get_credit_card_number(void);
int calculate_checksum(long card_number);
bool is_valid_amex(long card_number);
bool is_valid_mastercard(long card_number);
bool is_valid_visa(long card_number);

int main(void)
{
    long card_number = get_credit_card_number();
    int checksum = calculate_checksum(card_number);
    if (checksum % 10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }
    if (is_valid_amex(card_number))
    {
        printf("AMEX\n");
    }
    else if (is_valid_mastercard(card_number))
    {
        printf("MASTERCARD\n");
    }
    else if (is_valid_visa(card_number))
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }

    return 0;
}

long get_credit_card_number(void)
{
    long card_number;
    do
    {
        card_number = get_long("Number: ");
    }
    while (card_number <= 0);

    return card_number;
}

int calculate_checksum(long card_number)
{
    int sum = 0;
    int digit_count = 0;

    while (card_number > 0)
    {
        int digit = card_number % 10;

        if (digit_count % 2 == 1)
        {
            digit *= 2;

            while (digit > 0)
            {
                sum += digit % 10;
                digit /= 10;
            }
        }
        else
        {
            sum += digit;
        }

        card_number /= 10;
        digit_count++;
    }

    return sum;
}

bool is_valid_amex(long card_number)
{
    int num_digits = 0;
    long temp_card_number = card_number;

    while (temp_card_number > 0)
    {
        temp_card_number /= 10;
        num_digits++;
    }

    return num_digits == 15 && (card_number / 10000000000000 == 34 || card_number / 10000000000000 == 37);
}

bool is_valid_mastercard(long card_number)
{
    return (card_number >= 1000000000000000 && card_number < 10000000000000000) &&
           (card_number / 100000000000000 == 51 || card_number / 100000000000000 == 52 || card_number / 100000000000000 == 53 ||
            card_number / 100000000000000 == 54 || card_number / 100000000000000 == 55);
}

bool is_valid_visa(long card_number)
{
    int num_digits = 0;
    long temp_card_number = card_number;

    while (temp_card_number > 0)
    {
        temp_card_number /= 10;
        num_digits++;
    }
    return (num_digits == 13 || num_digits == 16) && (card_number / 1000000000000 == 4 || card_number / 1000000000000000 == 4);
}
