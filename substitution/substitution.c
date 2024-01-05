#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Function prototypes
bool is_valid_key(string key);
void encrypt(string plaintext, string key);

int main(int argc, string argv[])
{
    // Check for correct number of command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    // Check if the key is valid
    string key = argv[1];
    if (!is_valid_key(key))
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    // Get plaintext input from the user
    string plaintext = get_string("plaintext: ");

    // Encrypt and print the ciphertext
    printf("ciphertext: ");
    encrypt(plaintext, key);
    printf("\n");

    return 0;
}

// Function to check if the key is valid
bool is_valid_key(string key)
{
    // Check if the key has exactly 26 characters
    if (strlen(key) != 26)
    {
        return false;
    }

    // Check if each character is alphabetic and unique
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

// Function to encrypt plaintext using the substitution key
void encrypt(string plaintext, string key)
{
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        if (isalpha(plaintext[i]))
        {
            char original_case = isupper(plaintext[i]) ? 'A' : 'a';
            int index = tolower(plaintext[i]) - original_case;
            printf("%c", isupper(plaintext[i]) ? toupper(key[index]) : tolower(key[index]));
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    }
}
