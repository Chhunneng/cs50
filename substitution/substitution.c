#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

bool is_valid_key(string key);
void encrypt(string plaintext, string key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];
    if (!is_valid_key(key))
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    string plaintext = get_string("plaintext: ");

    printf("ciphertext: ");
    encrypt(plaintext, key);
    printf("\n");

    return 0;
}

bool is_valid_key(string key)
{
    if (strlen(key) != 26)
    {
        return false;
    }

    bool seen[26] = {false};
    for (int i = 0, n = strlen(key); i < n; i++)
    {
        if (!isalpha(key[i]))
        {
            return false;
        }

        int index = tolower(key[i]) - 'a';
        if (seen[index])
        {
            return false;
        }

        seen[index] = true;
    }

    return true;
}

void encrypt(string plaintext, string key)
{
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        if (isalpha(plaintext[i]))
        {
            char original_case = isupper(plaintext[i]) ? 'A' : 'a';
            int index = plaintext[i] - original_case;
            printf("%c", isupper(plaintext[i]) ? toupper(key[index]) : tolower(key[index]));
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    }
}
