## Basic Syntax
```c#
using System;

namespace GettingInput
{
  class Program
  {
    static void Main()
    {
      Console.WriteLine("How old are you?");
      string input = Console.ReadLine(); // By default only accept input as strings
      Console.WriteLine($"You are {input} years old!");
    }
  }
}
```
## Data Types

![[datatypes.png]]

**Examples**
```c#
using System;

namespace Form
{
  class Program
  {
    static void Main(string[] args)
    {
      // Create Variables
      string name;
      name = "Shadow";
      string breed;
       breed = "Golden Retriever";
      // Print variables to the console
      int age = 5;
      double weight = 65.22;
      bool spayed = true;
      Console.WriteLine(name);
      Console.WriteLine(breed);
      Console.WriteLine(age);
      Console.WriteLine(weight);
      Console.WriteLine(spayed);
      }
  }
}
```
## Changing data types
**Explicit conversion**
```c#
using System;

namespace FavoriteNumber
{
  class Program
  {
    static void Main(string[] args)
    {
      // Ask user for fave number

      Console.Write("Enter your favorite number!: ");

      // Turn that answer into an int

      int faveNumber = Convert.ToInt32(Console.ReadLine());
      Console.WriteLine(faveNumber);
    }
  }
}
```

```c#
using System;

namespace conversion
{
  class Program
  {
    static void Main(string[] args)
    {
      double doubleNumber = 10.2;
      Console.WriteLine(doubleNumber);
      int integer = (int)doubleNumber;
      Console.WriteLine(integer);
    }
  }
}
```