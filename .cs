using System;

class Program
{
    static int SumOfMatrix(int[,] A)
    {
        int summ = 0;
        int rows = A.GetLength(0);
        int cols = A.GetLength(1);

        for (int i = 0; i < rows; ++i)
        {
            for (int j = 0; j < cols; ++j)
            {
                summ += A[i, j];
            }
        }

        return summ;
    }

    static void Main()
    {
        int[,] A = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };

        int summ = SumOfMatrix(A);
        Console.WriteLine(summ);
    }
}